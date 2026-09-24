"""Create the portable Strategy Tester copy of the BlackBull terminal.

The copy runs with /portable so its data (MQL5\\, history, tester cache) lives inside
runtime\\tester and never collides with the open demo/live terminal.
After running this, launch the copy once by hand and log it into the demo account:
    runtime\\tester\\terminal64.exe /portable
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bridge import config  # noqa: E402

SKIP = {"uninstall.exe"}


def main() -> None:
    src = config.path(config.settings()["terminal"]["install_dir"])
    dst = config.tester_dir()
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in SKIP:
            continue
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        elif not target.exists() or item.stat().st_mtime > target.stat().st_mtime:
            shutil.copy2(item, target)
    print(f"tester copy ready at {dst}")
    print(f"next: run  \"{dst / 'terminal64.exe'}\" /portable  and log into the demo account once")


if __name__ == "__main__":
    main()
