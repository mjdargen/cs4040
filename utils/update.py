"""Set up a workspace for CS4040: install Pygame Zero Plus, and copy in the
examples and assets from the CS4040 repository.

Works on Windows, macOS and Linux, with Python 3.6 or newer. Run it from your
workspace folder, with the Python you use for your games:

    python update.py pygame          (Windows)
    python3 update.py pygame         (macOS and Linux)

Run it with no mode to see everything it can do. It downloads from GitHub, so
git doesn't need to be installed.
"""
import argparse
import io
import os
import re
import shutil
import site
import subprocess
import sys
import sysconfig
import tempfile
import urllib.request
import zipfile
from pathlib import Path

CS4040_ZIP = "https://github.com/mjdargen/cs4040/archive/refs/heads/main.zip"
# Where this script lives in the CS4040 repository, for self-update
SCRIPT_IN_REPO = "utils/update.py"

# Pygame Zero Plus at any branch, tag or commit, for pygame-dev
PGZERO_ZIP = "https://github.com/mjdargen/pgzero/archive/{version}.zip"
PGZERO_DIR = Path.home() / "pgzero"

ASSET_FOLDERS = ["images", "music", "sounds", "sprites"]
EXAMPLE = re.compile(r"e(\d\d).*\.py$")

# pygame-dev's pgzrun command contains this, so `pygame` knows to remove it
DEV_MARKER = "pygame-dev"

MODES = """\
modes:
  pygame               install the latest Pygame Zero Plus release (including alphas/betas)
  pygame-dev [VERSION] use Pygame Zero Plus straight from GitHub, to test before a release;
                       VERSION is a branch, tag or commit (default: main)
  assets               copy the images, music, sounds and sprites folders
  images               copy the images folder, and remove the other asset folders
  examples [N]         copy the example games, or only e00 to eN
  all [N]              copy the assets and the examples
  clean-examples       remove the example games
  clean-assets         remove the asset folders
  clean-all            remove the asset folders and the example games
  self-update          replace this script with the latest one from the CS4040 repository
"""


def main():
    parser = argparse.ArgumentParser(
        description="Set up a CS4040 workspace.",
        epilog=MODES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("mode", nargs="?")
    parser.add_argument("extra", nargs="?", help="N for examples/all, VERSION for pygame-dev")
    args = parser.parse_args()

    modes = {
        "pygame": update_pygame,
        "pygame-dev": lambda: update_pygame_dev(args.extra or "main"),
        "assets": lambda: copy_from_cs4040(assets=True),
        "images": lambda: copy_from_cs4040(assets=True, only_images=True),
        "examples": lambda: copy_from_cs4040(examples=True, last=example_number(args.extra)),
        "all": lambda: copy_from_cs4040(assets=True, examples=True, last=example_number(args.extra)),
        "clean-examples": clean_examples,
        "clean-assets": clean_assets,
        "clean-all": lambda: (clean_assets(), clean_examples()),
        "self-update": self_update,
        "moo": moo,
    }
    if args.mode not in modes:
        parser.print_help()
        sys.exit(1)
    if args.mode in ("assets", "images", "examples", "all", "clean-examples", "clean-assets", "clean-all"):
        check_not_the_repository()
    modes[args.mode]()
    print("Done.")


def example_number(text):
    if text is None:
        return None
    if not text.isdigit():
        sys.exit("Error: the last example must be a whole number, e.g. 13.")
    return int(text)


def check_not_the_repository():
    """Refuse to overwrite the files of the CS4040 repository itself."""
    here = Path.cwd()
    if (here / ".git").exists() and (here / SCRIPT_IN_REPO).exists():
        sys.exit(
            "Error: this is the CS4040 repository itself, so its examples and assets "
            "would be overwritten. Run this from a separate workspace folder."
        )


# Downloading


def download_zip(url, into):
    """Download a GitHub zip archive and unpack it into the folder `into`.

    Return the folder inside it with the repository's files, and the commit
    they come from.
    """
    print("Downloading {}...".format(url))
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
    except OSError as error:
        sys.exit("Error: couldn't download {}: {}".format(url, error))
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        archive.extractall(str(into))
        # GitHub stores the commit in the archive's comment
        commit = archive.comment.decode("ascii", "replace")[:7]
    (top,) = [p for p in into.iterdir() if p.is_dir()]
    return top, commit


def copy_from_cs4040(assets=False, examples=False, last=None, only_images=False):
    with tempfile.TemporaryDirectory() as tmp:
        repo, _ = download_zip(CS4040_ZIP, Path(tmp))
        if assets:
            copy_assets(repo, ["images"] if only_images else ASSET_FOLDERS)
        if examples:
            copy_examples(repo, last)


def copy_assets(repo, folders):
    print("Copying asset folders...")
    for folder in ASSET_FOLDERS:
        remove(Path(folder))
        if folder in folders and (repo / folder).is_dir():
            shutil.copytree(str(repo / folder), folder)


def example_files(folder):
    return [p for p in folder.iterdir() if p.is_file() and EXAMPLE.match(p.name)]


def copy_examples(repo, last):
    print("Copying example files...")
    clean_examples(quiet=True)
    if last is not None:
        print("Keeping examples e00 through e{:02d}...".format(last))
    for path in example_files(repo):
        if last is None or int(EXAMPLE.match(path.name).group(1)) <= last:
            shutil.copy(str(path), path.name)


def clean_examples(quiet=False):
    if not quiet:
        print("Removing all example files...")
    for path in example_files(Path.cwd()):
        path.unlink()


def clean_assets():
    print("Removing all asset folders...")
    for folder in ASSET_FOLDERS:
        remove(Path(folder))


def remove(path):
    if path.is_dir():
        shutil.rmtree(str(path))
    elif path.exists():
        path.unlink()


# Installing Pygame Zero Plus


def pip(*args, check=True):
    """Run pip with this Python, so packages go where this Python looks."""
    command = [sys.executable, "-m", "pip"] + list(args)
    result = subprocess.run(command)
    if check and result.returncode != 0:
        sys.exit("Error: '{}' failed.".format(" ".join(command)))
    return result.returncode == 0


def is_installed(package):
    command = [sys.executable, "-m", "pip", "show", package]
    return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def uninstall(package):
    print("Uninstalling {}...".format(package))
    if pip("uninstall", "-y", package, check=False):
        return
    # Packages installed for the whole system (e.g. on a shared Linux server)
    # need administrator rights to remove
    if os.name == "posix" and shutil.which("sudo"):
        command = ["sudo", sys.executable, "-m", "pip", "uninstall", "-y", package]
        if subprocess.run(command).returncode == 0:
            return
    sys.exit("Error: couldn't uninstall {}.".format(package))


def site_packages():
    """The folder where pip installs packages for this Python."""
    if site.ENABLE_USER_SITE and sys.prefix == sys.base_prefix:
        return Path(site.getusersitepackages())
    return Path(sysconfig.get_paths()["purelib"])  # e.g. in a virtual environment


def scripts_folder():
    """The folder where pip puts commands like pgzrun for this Python."""
    if site.ENABLE_USER_SITE and sys.prefix == sys.base_prefix:
        return Path(sysconfig.get_path("scripts", os.name + "_user"))
    return Path(sysconfig.get_path("scripts"))


def pth_file():
    return site_packages() / "pgzero-dev.pth"


def pgzrun_command():
    return scripts_folder() / ("pgzrun.cmd" if os.name == "nt" else "pgzrun")


def stop_using_pgzero_dev():
    """Undo pygame-dev, so that the installed release is used."""
    remove(pth_file())
    command = pgzrun_command()
    if command.exists() and DEV_MARKER in command.read_text():
        command.unlink()


def update_pygame():
    print("Removing old Pygame and Pygame Zero installations...")
    # Old copies of the framework in this folder would be used instead
    remove(Path("pgzero"))
    remove(Path("pgzrun.py"))
    stop_using_pgzero_dev()

    pip("install", "--upgrade", "pip")

    # These packages can install overlapping `pygame` or `pgzero` imports
    for package in ["pygame", "pygame-ce", "pgzero", "pgzero-mjd", "pgzero-plus"]:
        if is_installed(package):
            uninstall(package)
        else:
            print("Skipping {} (not installed)".format(package))

    print("Installing latest Pygame Zero Plus from PyPI (including alphas/betas)...")
    pip("install", "--no-cache-dir", "--pre", "--upgrade", "--index-url", "https://pypi.org/simple", "pgzero-plus")

    print("Verifying installation...")
    pip("check")


def update_pygame_dev(version):
    # pip can't build Pygame Zero Plus from GitHub on older Pythons (e.g.
    # 3.6), so instead of installing it, point Python at a copy of its files.

    # Install the release first, to get pygame, numpy etc., then remove it so
    # the copy from GitHub is used instead.
    update_pygame()
    print("Removing the release, to use Pygame Zero Plus from GitHub instead...")
    uninstall("pgzero-plus")

    with tempfile.TemporaryDirectory() as tmp:
        repo, commit = download_zip(PGZERO_ZIP.format(version=version), Path(tmp))
        print("Putting it in {}...".format(PGZERO_DIR))
        remove(PGZERO_DIR)
        shutil.move(str(repo), str(PGZERO_DIR))

    # A .pth file adds a folder to Python's path
    pth = pth_file()
    pth.parent.mkdir(parents=True, exist_ok=True)
    pth.write_text(str(PGZERO_DIR / "src") + "\n")

    # Uninstalling the release removed the pgzrun command, so make one that
    # runs the copy from GitHub
    command = pgzrun_command()
    command.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        command.write_text('@rem {}\n@"{}" -m pgzero %*\n'.format(DEV_MARKER, sys.executable))
    else:
        command.write_text('#!/bin/sh\n# {}\nexec "{}" -m pgzero "$@"\n'.format(DEV_MARKER, sys.executable))
        command.chmod(0o755)

    print("Verifying installation...")
    check = [sys.executable, "-c", "import pgzero, os; print(os.path.dirname(pgzero.__file__))"]
    result = subprocess.run(check, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    if result.returncode != 0:
        sys.exit("Error: Python can't import pgzero from {}:\n{}".format(PGZERO_DIR, result.stdout))
    print("pgzero now comes from: {}".format(result.stdout.strip()))
    print("Version: {} (commit {})".format(version, commit))
    print("To go back to the release, run this script with: pygame")


def self_update():
    script = Path(__file__).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        repo, commit = download_zip(CS4040_ZIP, Path(tmp))
        new = repo / SCRIPT_IN_REPO
        if not new.is_file():
            sys.exit("Error: {} isn't in the CS4040 repository.".format(SCRIPT_IN_REPO))
        # Write the new copy alongside, then swap it in, so a failed copy
        # can't leave a broken script behind
        temporary = script.with_name(script.name + ".new")
        shutil.copy(str(new), str(temporary))
        os.replace(str(temporary), str(script))
    print("Updated {} (commit {}).".format(script, commit))


def moo():
    print(r"""
 __________________________________
< I told you never hit this button >
 ----------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||""")


if __name__ == "__main__":
    main()
