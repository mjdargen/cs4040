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
import importlib
import io
import os
import re
import shutil
import site
import ssl
import subprocess
import sys
import sysconfig
import tempfile
import urllib.request
import zipfile
from pathlib import Path

CS4040_ZIP = "https://github.com/mjdargen/cs4040/archive/refs/heads/main.zip"
# One file from the CS4040 repository, without downloading all of it
CS4040_FILE = "https://raw.githubusercontent.com/mjdargen/cs4040/main/{path}"
# Where this script lives in the CS4040 repository, for self-update
SCRIPT_IN_REPO = "utils/update.py"

# Pygame Zero Plus at any branch, tag or commit, for pygame-dev
PGZERO_ZIP = "https://github.com/mjdargen/pgzero/archive/{version}.zip"
PGZERO_DIR = Path.home() / "pgzero"

ASSET_FOLDERS = ["images", "music", "sounds", "sprites", "maps", "fonts"]
EXAMPLE = re.compile(r"e(\d\d).*\.py$")

# pygame-dev's pgzrun command contains this, so `pygame` knows to remove it
DEV_MARKER = "pygame-dev"
# pygame-dev puts this file in its copy of Pygame Zero Plus, so `pygame` knows
# the folder is safe to delete
DEV_MARKER_FILE = ".installed-by-update-py"

MODES = """\
modes:
  pygame               install the latest Pygame Zero Plus release, and remove
                       pygame-dev if it was used
  pygame-dev [VERSION] use Pygame Zero Plus straight from GitHub, to test before a release;
                       VERSION is a branch, tag or commit (default: main)
  assets               copy the images, music, sounds, sprites, maps and fonts folders
  images               copy the images folder
  examples [N]         copy all examples, or only e00 through eN
  examples START END   copy examples eSTART through eEND (inclusive)
  all [N]              copy assets and all examples, or only e00 through eN
  all START END        copy assets and examples eSTART through eEND (inclusive)
  self-update          replace this script with the latest one from the CS4040 repository

Copying never deletes anything: files from the repository replace files with
the same name, and your own files (new images, your games, ...) are kept.
"""


def main():
    parser = argparse.ArgumentParser(
        description="Set up a CS4040 workspace.",
        epilog=MODES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("mode", nargs="?")
    parser.add_argument("extra", nargs="*", help="N or START END for examples/all, VERSION for pygame-dev")
    args = parser.parse_args()

    first, last = 0, None
    if args.mode in ("examples", "all"):
        first, last = example_range(args.extra)
    elif args.mode == "pygame-dev":
        if len(args.extra) > 1:
            parser.error("pygame-dev takes at most one VERSION")
    elif args.extra:
        parser.error("{} does not take additional arguments".format(args.mode))

    modes = {
        "pygame": update_pygame,
        "pygame-dev": lambda: update_pygame_dev(args.extra[0] if args.extra else "main"),
        "assets": lambda: copy_from_cs4040(assets=True),
        "images": lambda: copy_from_cs4040(assets=True, only_images=True),
        "examples": lambda: copy_from_cs4040(examples=True, first=first, last=last),
        "all": lambda: copy_from_cs4040(assets=True, examples=True, first=first, last=last),
        "self-update": self_update,
        "moo": moo,
    }
    if args.mode not in modes:
        parser.print_help()
        sys.exit(1)
    if args.mode in ("assets", "images", "examples", "all"):
        check_not_the_repository()
    modes[args.mode]()
    print("Done.")


def example_range(values):
    if len(values) > 2 or any(not value.isdigit() for value in values):
        sys.exit("Error: use a whole number N, or START END, e.g. 3 13.")
    if not values:
        return 0, None
    if len(values) == 1:
        return 0, int(values[0])
    first, last = int(values[0]), int(values[1])
    if first > last:
        sys.exit("Error: START must be less than or equal to END.")
    return first, last


def check_not_the_repository():
    """Refuse to overwrite the files of the CS4040 repository itself."""
    here = Path.cwd()
    if (here / ".git").exists() and (here / SCRIPT_IN_REPO).exists():
        sys.exit(
            "Error: this is the CS4040 repository itself, so its examples and assets "
            "would be overwritten. Run this from a separate workspace folder."
        )


# Downloading


# The certificate check that worked, once Python's own check has failed
_ssl_context = None


def download(url):
    """Return the contents of url as bytes."""
    global _ssl_context
    print("Downloading {}...".format(url))
    try:
        return fetch(url, _ssl_context)
    except OSError as error:
        if _ssl_context is not None or not is_certificate_error(error):
            sys.exit(download_error(url, error))
        first_error = error

    # Python checks certificates with its own list, not the computer's. Some
    # networks send certificates that browsers accept but Python doesn't (e.g.
    # with a link in the chain missing), so try the computer's check instead.
    print("Python couldn't verify the connection, so trying your computer's own certificate check...")
    for context in fallback_ssl_contexts():
        try:
            data = fetch(url, context)
        except OSError as error:
            if not is_certificate_error(error):
                sys.exit(download_error(url, error))
            continue
        _ssl_context = context
        return data
    sys.exit(download_error(url, first_error))


def fetch(url, context=None):
    with urllib.request.urlopen(url, timeout=60, context=context) as response:
        return response.read()


def fallback_ssl_contexts():
    """Other ways to check certificates. Each still checks them; none skips it."""
    if sys.version_info >= (3, 10):
        truststore = import_or_install("truststore")
        if truststore:
            # Asks Windows or macOS, like a web browser does
            yield truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # Up-to-date list of certificates, for Pythons that have none (e.g. from
    # python.org on macOS, before running Install Certificates.command)
    certifi = import_or_install("certifi")
    if certifi:
        yield ssl.create_default_context(cafile=certifi.where())


def import_or_install(package):
    """Import package, installing it with pip first if needed. None if that fails."""
    try:
        return importlib.import_module(package)
    except ImportError:
        pass
    print("Installing {}...".format(package))
    if not pip("install", "--quiet", package, check=False):
        return None
    importlib.invalidate_caches()
    # Python only looks in the folder pip installs to if it existed at startup
    if str(site_packages()) not in sys.path:
        site.addsitedir(str(site_packages()))
    try:
        return importlib.import_module(package)
    except ImportError:
        return None


def is_certificate_error(error):
    reason = getattr(error, "reason", error)  # urllib wraps the SSL error
    if isinstance(reason, getattr(ssl, "SSLCertVerificationError", ())):
        return True
    return isinstance(reason, ssl.SSLError) and "CERTIFICATE_VERIFY_FAILED" in str(reason)  # Python 3.6


def download_error(url, error):
    message = "Error: couldn't download {}: {}".format(url, error)
    if is_certificate_error(error):
        message += (
            "\nPython couldn't confirm it was really talking to GitHub. The network may be "
            "interfering with secure connections: try another network, e.g. a phone hotspot."
        )
        if sys.platform == "darwin":
            message += (
                " If you installed Python from python.org, also run Install Certificates.command "
                "in the Python folder in Applications."
            )
    return message


def download_zip(url, into):
    """Download a GitHub zip archive and unpack it into the folder `into`.

    Return the folder inside it with the repository's files, and the commit
    they come from.
    """
    data = download(url)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        archive.extractall(str(into))
        # GitHub stores the commit in the archive's comment
        commit = archive.comment.decode("ascii", "replace")[:7]
    (top,) = [p for p in into.iterdir() if p.is_dir()]
    return top, commit


def copy_from_cs4040(assets=False, examples=False, first=0, last=None, only_images=False):
    with tempfile.TemporaryDirectory() as tmp:
        repo, _ = download_zip(CS4040_ZIP, Path(tmp))
        if assets:
            copy_assets(repo, ["images"] if only_images else ASSET_FOLDERS)
        if examples:
            copy_examples(repo, first, last)


def copy_assets(repo, folders):
    print("Copying asset folders...")
    for folder in folders:
        if (repo / folder).is_dir():
            new, updated = copy_into(repo / folder, Path(folder))
            print("  {}: {} new, {} updated".format(folder, new, updated))


def copy_into(source, destination):
    """Copy every file in the folder source into the folder destination,
    replacing files with the same name. Files that are only in destination
    (e.g. a student's own images) are kept. Return how many files were new
    and how many replaced an existing file.
    """
    new = updated = 0
    for folder, _, files in os.walk(str(source)):
        target = destination / Path(folder).relative_to(source)
        if target.exists() and not target.is_dir():
            print("  Skipping {}: a file has the folder's name".format(target))
            continue
        target.mkdir(parents=True, exist_ok=True)
        for name in files:
            target_file = target / name
            if target_file.is_dir():
                print("  Skipping {}: a folder has the file's name".format(target_file))
                continue
            if target_file.exists():
                updated += 1
            else:
                new += 1
            shutil.copy2(os.path.join(folder, name), str(target_file))
    return new, updated


def example_files(folder):
    return [p for p in folder.iterdir() if p.is_file() and EXAMPLE.match(p.name)]


def copy_examples(repo, first, last):
    print("Copying example files...")
    if last is not None:
        print("Copying examples e{:02d} through e{:02d}...".format(first, last))
    new = updated = 0
    for path in example_files(repo):
        number = int(EXAMPLE.match(path.name).group(1))
        if number >= first and (last is None or number <= last):
            if Path(path.name).exists():
                updated += 1
            else:
                new += 1
            shutil.copy2(str(path), path.name)
    print("  {} new, {} updated".format(new, updated))


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


def is_dev_copy(folder, pth):
    """True if `folder` is a copy of Pygame Zero Plus that pygame-dev made.

    A git clone someone made there themselves never counts, so it's never
    deleted. Copies made before the marker file existed are recognized by the
    .pth file pointing at them, or by being a GitHub download of pgzero-plus
    (which has no .git folder).
    """
    if not folder.is_dir() or (folder / ".git").exists():
        return False
    if (folder / DEV_MARKER_FILE).exists():
        return True
    if pth.exists() and str(folder) in pth.read_text():
        return True
    pyproject = folder / "pyproject.toml"
    return (
        (folder / "src" / "pgzero").is_dir() and pyproject.is_file() and 'name = "pgzero-plus"' in pyproject.read_text()
    )


def stop_using_pgzero_dev():
    """Undo pygame-dev, so that the installed release is used: remove its
    .pth file, its pgzrun command and its copy of Pygame Zero Plus."""
    pth = pth_file()
    remove_copy = is_dev_copy(PGZERO_DIR, pth)
    remove(pth)
    command = pgzrun_command()
    if command.exists() and DEV_MARKER in command.read_text():
        command.unlink()
    if remove_copy:
        print("Removing the pygame-dev copy of Pygame Zero Plus in {}...".format(PGZERO_DIR))
        remove(PGZERO_DIR)


# pgzero-plus installs pygame-ce on Python 3.10 and newer, and pygame before
# that. Each group of packages here installs the same files (pygame's, or
# pgzero's and pgzrun's), so having more than one of a group installed breaks
# them. The first package in each group is the one pgzero-plus wants.
WANTED_PYGAME = "pygame-ce" if sys.version_info >= (3, 10) else "pygame"
CLASHING_GROUPS = [
    [WANTED_PYGAME, "pygame" if WANTED_PYGAME == "pygame-ce" else "pygame-ce"],
    ["pgzero-plus", "pgzero", "pgzero-mjd"],
]


def update_pygame():
    # Old copies of the framework in this folder would be used instead
    remove(Path("pgzero"))
    remove(Path("pgzrun.py"))
    stop_using_pgzero_dev()

    pip("install", "--upgrade", "pip", check=False)

    # Only uninstall when something clashes. Otherwise the working install is
    # left alone until the new one has downloaded, so a failed download can't
    # leave the computer without pygame.
    for group in CLASHING_GROUPS:
        installed = [package for package in group if is_installed(package)]
        unwanted = [package for package in installed if package != group[0]]
        if unwanted:
            print("Removing {}, which clash with each other...".format(" and ".join(installed)))
            # They share files, so remove all of them; installing pgzero-plus
            # below brings back the right one.
            for package in installed:
                uninstall(package)

    print("Installing latest Pygame Zero Plus from PyPI...")
    pip("install", "--no-cache-dir", "--upgrade", "--index-url", "https://pypi.org/simple", "pgzero-plus")

    print("Verifying installation...")
    check = [sys.executable, "-c", "import pgzero, pygame; print(pgzero.__version__, pygame.version.ver)"]
    result = subprocess.run(check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if result.returncode != 0:
        sys.exit("Error: Pygame Zero Plus didn't install correctly:\n{}".format(result.stderr))
    if result.stderr.strip():
        print(result.stderr.strip())  # e.g. Pygame Zero Plus's own warnings
    pgzero_version, pygame_version = result.stdout.split()[-2:]
    print("Pygame Zero Plus {} with {} {} is ready.".format(pgzero_version, WANTED_PYGAME, pygame_version))

    # pip check looks at every package on this computer, so a problem it finds
    # may have nothing to do with Pygame Zero Plus. Show it, but don't fail.
    if not pip("check", check=False):
        print("Note: pip found the problems above in other installed packages. "
              "They don't affect Pygame Zero Plus.")


def update_pygame_dev(version):
    # pip can't build Pygame Zero Plus from GitHub on older Pythons (e.g.
    # 3.6), so instead of installing it, point Python at a copy of its files.

    # Don't overwrite a folder someone made there themselves
    if PGZERO_DIR.exists() and not is_dev_copy(PGZERO_DIR, pth_file()):
        sys.exit(
            "Error: {} already exists and wasn't made by this script (it may be your own "
            "copy of the code). Move or rename it, then run this again.".format(PGZERO_DIR)
        )

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
    (PGZERO_DIR / DEV_MARKER_FILE).write_text(
        "Made by update.py pygame-dev. Running update.py pygame deletes this folder.\n"
    )

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
    # Only this one file is needed, so fetch it instead of the whole repository
    new = download(CS4040_FILE.format(path=SCRIPT_IN_REPO))
    try:
        compile(new, SCRIPT_IN_REPO, "exec")
    except SyntaxError as error:
        sys.exit("Error: the downloaded {} isn't valid Python ({}), so it wasn't used.".format(SCRIPT_IN_REPO, error))
    # Write the new copy alongside, then swap it in, so a failed write can't
    # leave a broken script behind
    temporary = script.with_name(script.name + ".new")
    temporary.write_bytes(new)
    os.replace(str(temporary), str(script))
    print("Updated {}.".format(script))


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
