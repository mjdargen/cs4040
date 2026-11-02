"""Course filter for Quarto (plain Python, standard library only).

Quarto runs this on every page while rendering (see `filters:` in _quarto.yml).
It does two jobs:

1. Pull code from .py files into code blocks, so code is never pasted:

       ```{.python include="code/actor_basics.py" snippet="move" dedent=4}
       ```

   include  path to the file, relative to the page, or to the repo root if it
            starts with "/" (e.g. include="/e04bouncing.py")
   Pick part of the file with ONE of these (otherwise the whole file is shown):
   def="update"                      the whole function update()
   from="# check rightmost"          from the first line containing that text to
                                     the end of the block it sits in
   from="..." to="..."               from one line containing text to the next
                                     line containing other text
   snippet="move"                    lines between "# start snippet move" and
                                     "# end snippet move" (used in course/*/code/;
                                     example files students run have no markers)
   start-line=5 end-line=9           a line range (breaks when the file changes)
   Indentation is removed automatically. If the text or function is not found,
   the page shows "!! code not found" and the render prints a WARNING.
   file-line-numbers="true"   number the block with the line numbers students
            see in the file (snippet marker lines are not counted, because the
            Codio build removes them)
   Snippet marker lines are never shown.

2. Codio-only markup. On Codio pages (Markdown output) it becomes Codio's own
   syntax; on the website it becomes a readable preview:

       [Check It!]{.checkit id=multiple-choice-365928436}
       [Update Images]{.codio-button run="python3 update.py images"}
       [Pygame Zero Basics slides]{.codio-embed href="../u3m1-slides.qmd"}

Pandoc passes the page as JSON on stdin and the output format as the first
argument; the filter prints the changed JSON.
"""

import ast
import json
import os
import re
import sys
import textwrap
from pathlib import Path

FORMAT = sys.argv[1] if len(sys.argv) > 1 else "html"
CODIO = FORMAT in ("gfm", "commonmark", "markdown")  # Codio pages are rendered as Markdown
HERE = Path.cwd()  # Quarto runs filters from the page's folder
MARKER = re.compile(r"^\s*\S+\s+(start|end) snippet \S+\s*$")


def project_root():
    env = os.environ.get("QUARTO_PROJECT_DIR")
    if env and (Path(env) / "_quarto.yml").exists():
        return Path(env)
    for folder in [HERE, *HERE.parents]:
        if (folder / "_quarto.yml").exists():
            return folder
    return HERE


ROOT = project_root()


# ---------- small helpers for pandoc's JSON format ----------

def text_inlines(text):
    """Plain text with `code` spans -> pandoc inline elements."""
    out = []
    for i, part in enumerate(re.split(r"`([^`]*)`", text)):
        if i % 2:
            out.append({"t": "Code", "c": [["", [], []], part]})
            continue
        for j, word in enumerate(part.split(" ")):
            if j:
                out.append({"t": "Space"})
            if word:
                out.append({"t": "Str", "c": word})
    return out


def stringify(inlines):
    s = ""
    for x in inlines:
        t = x.get("t")
        if t == "Str":
            s += x["c"]
        elif t in ("Space", "SoftBreak"):
            s += " "
        elif t == "Code":
            s += x["c"][1]
        elif isinstance(x.get("c"), list):
            s += stringify(x["c"][-1] if t in ("Span", "Link") else x["c"])
    return s


def md_blocks(text):
    """Question text from Codio: paragraphs and ```fenced``` code -> pandoc blocks."""
    blocks = []
    for i, part in enumerate(re.split(r"```(\w*)\n(.*?)```", text, flags=re.S)):
        if i % 3 == 1:
            lang = part
        elif i % 3 == 2:
            blocks.append({"t": "CodeBlock", "c": [["", [lang] if lang else [], []], part.rstrip("\n")]})
        else:
            for chunk in re.split(r"\n\s*\n", part.strip()):
                if chunk.strip():
                    blocks.append(para(text_inlines(" ".join(chunk.split()))))
    return blocks


def para(inlines):
    return {"t": "Para", "c": inlines}


def raw_block(text):
    return {"t": "RawBlock", "c": ["markdown", text]}


def box(title, blocks):
    """A simple framed box on the website (Bootstrap alert, follows light/dark theme)."""
    head = para([{"t": "Strong", "c": text_inlines(title)}])
    return {"t": "Div", "c": [["", ["alert", "alert-secondary"], []], [head, *blocks]]}


# ---------- 1. code includes ----------

def resolve(path):
    return ROOT / path.lstrip("/") if path.startswith("/") else HERE / path


def select_lines(lines, a, path):
    """Return (first, last) line numbers (1-based, inclusive) to show, or None."""
    n = len(lines)
    if "snippet" in a:  # "# start snippet NAME" ... "# end snippet NAME"
        name = a.pop("snippet")
        begin = re.compile(rf"^\s*\S+\s+start snippet {re.escape(name)}\s*$")
        stop = re.compile(rf"^\s*\S+\s+end snippet {re.escape(name)}\s*$")
        starts = [i for i, l in enumerate(lines, 1) if begin.match(l)]
        ends = [i for i, l in enumerate(lines, 1) if stop.match(l)]
        return (starts[0] + 1, ends[0] - 1) if starts and ends else None
    if "def" in a:  # a whole function, found by name
        name = a.pop("def")
        try:
            tree = ast.parse("\n".join(lines))
        except SyntaxError:
            return None
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == name:
                first = min([node.lineno] + [d.lineno for d in node.decorator_list])
                return first, node.end_lineno
        return None
    if "from" in a:  # from a line containing this text...
        text_from, text_to = a.pop("from"), a.pop("to", None)
        first = next((i for i, l in enumerate(lines, 1) if text_from in l), None)
        if first is None:
            return None
        if text_to is not None:  # ...to the next line containing this text
            last = next((i for i in range(first, n + 1) if text_to in lines[i - 1]), None)
            return (first, last) if last else None
        # ...to the end of the block it is in
        indent = len(lines[first - 1]) - len(lines[first - 1].lstrip())
        last = first
        for i in range(first + 1, n + 1):
            line = lines[i - 1]
            if line.strip() and len(line) - len(line.lstrip()) < indent:
                break
            if line.strip():
                last = i
        return first, last
    first = int(a.pop("start-line", 1))
    return first, int(a.pop("end-line", n))


def include_code(block):
    (ident, classes, attrs), _ = block["c"]
    a = dict(attrs)
    if "include" not in a:
        return block
    target = a.pop("include")
    path = resolve(target)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        sys.stderr.write(f"course_filter: WARNING cannot open {path}\n")
        return {"t": "CodeBlock", "c": [[ident, classes, list(a.items())], f"!! file not found: {target}"]}
    wanted = {k: a[k] for k in ("snippet", "def", "from", "to") if k in a}
    found = select_lines(lines, a, path)
    a.pop("dedent", None)  # code is always dedented automatically now
    if not found:
        sys.stderr.write(f"course_filter: WARNING {wanted} not found in {target}\n")
        return {"t": "CodeBlock", "c": [[ident, classes, list(a.items())], f"!! code not found in {target}: {wanted}"]}
    start, end = found
    keep = [l for l in lines[start - 1:end] if not MARKER.match(l)]
    code = textwrap.dedent("\n".join(keep)).strip("\n")
    if a.pop("file-line-numbers", "") == "true":
        markers_before = sum(1 for l in lines[:start - 1] if MARKER.match(l))
        a["startFrom"] = str(start - markers_before)
        classes = classes + ["number-lines"]
    return {"t": "CodeBlock", "c": [[ident, classes, list(a.items())], code]}


# ---------- 2. Codio markup ----------

def site_url():
    try:
        text = (ROOT / "_variables.yml").read_text(encoding="utf-8")
        m = re.search(r"^\s+site:\s*(\S+)", text, re.M)
        return m.group(1).rstrip("/") if m else ""
    except OSError:
        return ""


def find_assessment(aid):
    """Codio questions hold the answers, so they live in _private/ (never pushed)."""
    for f in (ROOT / "_private" / "codio-assessments").glob(f"*/{aid}.json"):
        return json.loads(f.read_text(encoding="utf-8"))
    return None


def checkit(aid):
    if CODIO:
        return raw_block(f"{{Check It!|assessment}}({aid})")
    a = find_assessment(aid)
    if not a:
        return box("Check It! (answered in Codio)", [])
    src = a.get("source", {})
    if a.get("type") == "multiple-choice":
        choices = [[{"t": "Plain", "c": text_inlines(x["answer"].strip())}] for x in src.get("answers", [])]
        return box("Check It! (answered in Codio)", [*md_blocks(src.get("instructions", "")), {"t": "BulletList", "c": choices}])
    if a.get("type") == "fill-in-the-blanks":
        return box("Check It! (answered in Codio)", [para(text_inlines(re.sub(r"<<<.*?>>>", "_____", src.get("text", ""))))])
    if a.get("type") == "grade-book":
        return box("Graded in Codio", [para(text_inlines(f"{src.get('name', '')} ({src.get('points', '')} points)"))])
    return box("Check It!", [para(text_inlines(aid))])


def embed(label, href):
    if not CODIO:
        return para([{"t": "Link", "c": [["", [], []], text_inlines(label), [href, ""]]}])
    target = (HERE / href).resolve()
    try:
        rel = target.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        rel = href
    url = f"{site_url()}/{re.sub(r'[.]qmd$', '.html', rel)}"
    return raw_block(
        f'<p><a href="{url}" target="_blank" rel="noopener">{label} (opens in a new tab)</a></p>\n'
        f'<p><iframe style="width: 800px; height: 540px;" title="{label}" src="{url}" loading="lazy" allowfullscreen></iframe></p>'
    )


def span_info(x):
    if x.get("t") != "Span":
        return None
    (ident, classes, attrs), content = x["c"]
    attrs = dict(attrs)
    if ident:  # pandoc stores id=... as the element's identifier
        attrs.setdefault("id", ident)
    return classes, attrs, content


def codio_block(block):
    """A paragraph that holds only a .checkit or .codio-embed span."""
    items = [x for x in block["c"] if x.get("t") not in ("Space", "SoftBreak")]
    if len(items) != 1:
        return None
    info = span_info(items[0])
    if not info:
        return None
    classes, attrs, content = info
    if "checkit" in classes:
        return checkit(attrs.get("id", ""))
    if "codio-embed" in classes:
        return embed(stringify(content), attrs.get("href", ""))
    return None


def codio_inline(x):
    info = span_info(x)
    if not info or "codio-button" not in info[0]:
        return [x]
    label, command = stringify(info[2]), info[1].get("run", "")
    if CODIO:
        return [{"t": "RawInline", "c": ["markdown", f"{{{label}}}({command})"]}]
    return [{"t": "Strong", "c": text_inlines(f"[{label}]")}, {"t": "Space"}, {"t": "Str", "c": "runs"},
            {"t": "Space"}, {"t": "Code", "c": [["", [], []], command]}]


# ---------- walk the document ----------

def walk_blocks(blocks):
    out = []
    for b in blocks:
        t = b.get("t")
        if t == "CodeBlock":
            out.append(include_code(b))
            continue
        if t == "Para":
            replaced = codio_block(b)
            if replaced:
                out.append(replaced)
                continue
            b = {"t": "Para", "c": walk_inlines(b["c"])}
        elif t == "Plain":
            b = {"t": "Plain", "c": walk_inlines(b["c"])}
        elif t in ("Div", "BlockQuote"):
            if t == "Div":
                b = {"t": "Div", "c": [b["c"][0], walk_blocks(b["c"][1])]}
            else:
                b = {"t": t, "c": walk_blocks(b["c"])}
        elif t in ("BulletList",):
            b = {"t": t, "c": [walk_blocks(item) for item in b["c"]]}
        elif t == "OrderedList":
            b = {"t": t, "c": [b["c"][0], [walk_blocks(item) for item in b["c"][1]]]}
        out.append(b)
    return out


def walk_inlines(inlines):
    out = []
    for x in inlines:
        out.extend(codio_inline(x))
    return out


def main():
    # Read and write raw UTF-8 bytes. Windows Python would otherwise decode the
    # page as cp1252 and turn characters like "·" into "Â·".
    doc = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    doc["blocks"] = walk_blocks(doc["blocks"])
    sys.stdout.buffer.write(json.dumps(doc, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    main()
