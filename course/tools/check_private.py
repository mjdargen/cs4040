"""Safety net run by git before every commit (.githooks/pre-commit).

.gitignore already keeps private files out of `git add .`. This catches the
two ways one can still slip through:
  1. a new private file added on purpose or by accident with `git add -f`
     (anything matching .gitignore: activity*.py, _private/, _*.py, ...)
  2. any file containing a line that starts with "# PRIVATE"

If it finds one, the commit is stopped and nothing is published.
Turn it on once in each clone:  git config core.hooksPath .githooks
"""

import subprocess
import sys


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def staged_bytes(path):
    return subprocess.run(["git", "show", f":{path}"], capture_output=True).stdout


staged = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").stdout.split("\0")
new = set(git("diff", "--cached", "--name-only", "--diff-filter=A", "-z").stdout.split("\0"))
problems = []
for path in filter(None, staged):
    # only NEW files are checked against .gitignore, so files that were already
    # published on purpose (like README.md) can still be edited
    if path in new and git("check-ignore", "-q", "--no-index", path).returncode == 0:
        problems.append(f"{path}  (matches a private pattern in .gitignore)")
        continue
    data = staged_bytes(path)
    if b"\0" in data[:8000]:  # images, sounds and other binary files
        continue
    content = data.decode("utf-8", errors="replace")
    if any(line.startswith("# PRIVATE") for line in content.splitlines()):
        problems.append(f"{path}  (contains a '# PRIVATE' line)")

if problems:
    print("Commit stopped: these files are private and would be published to GitHub:")
    for p in problems:
        print("   ", p)
    print("Unstage them with:  git restore --staged <file>")
    sys.exit(1)
