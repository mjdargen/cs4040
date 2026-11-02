"""Turn rendered modules into Codio assignment folders (and zips).

Usage (from the repo root, after `quarto render`):
    python course/tools/build_codio.py                      # every module with codio/assignment.toml
    python course/tools/build_codio.py course/u3m1

A module is only built when its assignment.toml has `build = true` under
[assignment]; otherwise it is skipped. Its lesson pages must also be listed
under `render:` in _quarto.yml so Quarto makes the Markdown this script copies.

Needs only Python 3.11+ (tomllib is in the standard library).

For each module it:
  1. checks that every .py in the module compiles and every Check-It id exists,
  2. copies the Markdown pages Quarto rendered into .guides/content/ with the
     page .json files Codio expects (title, id, layout, which file opens),
  3. copies only the images/videos those pages use into .guides/img/,
  4. copies examples (snippet markers removed), lab starters, sprites,
     assessments, lab solutions (into .guides/secure/) and Codio config,
  5. zips the folder so it can be imported into Codio.
"""

import json
import py_compile
import re
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # repo root (this file is course/tools/)
PRIVATE = ROOT / "_private"  # never pushed: Codio answers
SITE = ROOT / "_build" / "site"
OUT = ROOT / "_build" / "codio"

MARKER = re.compile(r"^\s*#\s*(start|end) snippet \S+\s*$")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
CHECKIT = re.compile(r"\{Check It!\|assessment\}\(([\w-]+)\)")
VIDEO_EXT = {".mp4", ".webm", ".mov"}


def root_path(p, base):
    """Paths starting with / are relative to the repo root, others to base."""
    return ROOT / p.lstrip("/") if p.startswith("/") else (base / p).resolve()


def codio_name(title, page_id):
    """Codio's file naming rule: non-alphanumerics become '-', then '-' + id[:4]."""
    return re.sub(r"[^A-Za-z0-9]", "-", title) + "-" + page_id[:4]


def strip_markers(src, dst):
    lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
    dst.write_text("".join(l for l in lines if not MARKER.match(l)), encoding="utf-8")


def check_python(module):
    bad = []
    for f in module.rglob("*.py"):
        try:
            py_compile.compile(str(f), doraise=True, cfile=str(OUT / "_pycache_check.pyc"))
        except py_compile.PyCompileError as e:
            bad.append(str(e))
    (OUT / "_pycache_check.pyc").unlink(missing_ok=True)
    return bad


def page_json(page, title):
    files = [{"path": "#tabs", "action": "close"}]
    layout = "1-panel-tree"
    if page.get("open"):
        layout = "2-panels-tree"
        files += [
            {"path": "#preview: https://{{domain3050}}/", "panel": 0, "action": "open"},
            {"path": page["open"], "panel": 0, "action": "open"},
        ]
    if page.get("terminal"):
        layout = "2-panels-tree"
        files.append({"path": "#terminal: ", "panel": 0, "action": "open"})
    return {
        "id": page["id"],
        "title": title,
        "files": files,
        "layout": layout,
        "path": [],
        "type": "page",
        "contentType": "markdown",
        "teacherOnly": False,
        "closeTerminalSession": False,
        "learningObjectives": "",
    }


def build(module):
    cfg = tomllib.loads((module / "codio" / "assignment.toml").read_text(encoding="utf-8"))
    rel = module.relative_to(ROOT)
    dest = OUT / cfg["assignment"]["folder"]
    shutil.rmtree(dest, ignore_errors=True)
    content, img = dest / ".guides" / "content", dest / ".guides" / "img"
    content.mkdir(parents=True)
    img.mkdir()
    problems = check_python(module)

    # 1. pages
    order, used_ids, student_files = [], set(), set()
    for page in cfg["page"]:
        source = module / page["source"]
        rendered = SITE / rel / Path(page["source"]).with_suffix(".md")
        if not rendered.exists():
            problems.append(f"{rendered} missing: run `quarto render` first")
            continue
        text = rendered.read_text(encoding="utf-8")
        title_match = re.match(r"\s*# (.+)\n", text)
        title = title_match.group(1).strip() if title_match else source.stem
        text = text[title_match.end() :] if title_match else text
        text = re.sub(r"<!--.*?-->\s*", "", text, flags=re.S).strip() + "\n"

        def media(m):
            alt, link = m.group(1), m.group(2)
            if "://" in link:
                return m.group(0)
            f = root_path(link, source.parent)
            if not f.exists():
                problems.append(f"{page['source']}: image {link} not found")
                return m.group(0)
            name = f.name if f.parent.name == "media" else f"{f.parent.name}-{f.name}"
            shutil.copy2(f, img / name)
            if f.suffix.lower() in VIDEO_EXT:
                return (
                    f'<div><iframe src=".guides/img/{name}" width="400" height="400" '
                    'frameborder="0" allowfullscreen></iframe></div>'
                )
            return f"![{alt}](.guides/img/{name})"

        text = IMAGE.sub(media, text)
        used_ids.update(CHECKIT.findall(text))
        name = codio_name(title, page["id"])
        (content / f"{name}.md").write_text(text, encoding="utf-8")
        (content / f"{name}.json").write_text(json.dumps(page_json(page, title), indent=2), encoding="utf-8")
        order.append(name)
        if page.get("open"):
            student_files.add(page["open"])

    settings = json.loads((root_path(cfg["files"]["codio_config"], module) / "guide-settings.json").read_text())
    index = {"title": cfg["assignment"]["title"], **settings, "order": order}
    (content / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

    # 2. assessments actually used by the pages
    (dest / ".guides" / "assessments").mkdir()
    for aid in sorted(used_ids):
        f = PRIVATE / "codio-assessments" / module.name / f"{aid}.json"
        if f.exists():
            shutil.copy2(f, dest / ".guides" / "assessments" / f.name)
        else:
            problems.append(f"Check It! {aid}: no _private/codio-assessments/{module.name}/{aid}.json")

    # 3. student files
    files = cfg["files"]
    for ex in sorted(ROOT.glob(files["examples"].lstrip("/"))):
        strip_markers(ex, dest / ex.name)
    starter = root_path(files["starter"], module)
    for name in files.get("starter_copies", []):
        shutil.copy2(starter, dest / name)
    for name, src in files.get("extra", {}).items():
        shutil.copy2(root_path(src, module), dest / name)
    shutil.copytree(root_path(files["images"], module), dest / "images")
    for f in student_files:
        if not (dest / f).exists():
            problems.append(f"a page opens {f}, but it is not in the assignment")

    # 4. teacher-only files and Codio config
    secure = dest / ".guides" / "secure"
    secure.mkdir()
    for name in files.get("solutions", []):  # private, local only
        sol = root_path(name, module)
        if sol.exists():
            shutil.copy2(sol, secure / sol.name)
        else:
            problems.append(f"solution {name} not found (it is private, so it only exists on your computer)")
    cc = root_path(files["codio_config"], module)
    shutil.copy2(cc / "codio.json", dest / ".codio")
    shutil.copy2(cc / "settings.ini", dest / ".settings")
    (dest / ".guides" / "install").mkdir()

    zip_path = shutil.make_archive(str(dest), "zip", dest)
    return dest, zip_path, len(order), len(used_ids), problems


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    targets = [ROOT / a for a in sys.argv[1:]] or [
        p.parent.parent for p in ROOT.glob("course/u*m*/codio/assignment.toml")
    ]
    if not targets:
        print("No modules have course/<module>/codio/assignment.toml yet; nothing to build.")
    failed = False
    for module in targets:
        cfg = tomllib.loads((module / "codio" / "assignment.toml").read_text(encoding="utf-8"))
        if not cfg["assignment"].get("build", False):
            print(f"{module.relative_to(ROOT)}: skipped (build = false in codio/assignment.toml)")
            continue
        dest, zip_path, pages, checks, problems = build(module)
        print(
            f"{module.relative_to(ROOT)} -> {Path(zip_path).relative_to(ROOT)}  ({pages} pages, {checks} assessments)"
        )
        for p in problems:
            print("  PROBLEM:", p)
        failed |= bool(problems)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
