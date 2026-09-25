"""Create a portable terminal copy for a target: a prop account from settings.terminals, or 'tester'.

python scripts/setup_terminal.py ftmo_50k
python scripts/setup_terminal.py tester

The copy runs with /portable, so its data (MQL5, history, logins) lives inside its own folder.
For a prop account, install the FIRM's MT5 terminal build if it provides one (its server list),
or add the firm's server in this copy. Launch it once and log in yourself (Claude never types
passwords), then run the MCP tool install_host(target=...) and attach QB_Host with
InpConfig=portfolio_<target>.cfg.
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bridge import config  # noqa: E402

SKIP = {"uninstall.exe"}


def main(target: str) -> None:
    src = config.path(config.settings()["terminal"]["install_dir"])
    if target == "tester":
        dst = config.tester_dir()
    else:
        t = config.settings()["terminals"][target]
        if not t.get("portable"):
            raise SystemExit(f"terminals.{target} is not a portable copy; nothing to set up")
        dst = config.path(t["install_dir"])
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in SKIP:
            continue
        target_path = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target_path, dirs_exist_ok=True)
        elif not target_path.exists() or item.stat().st_mtime > target_path.stat().st_mtime:
            shutil.copy2(item, target_path)
    print(f"{target} terminal ready at {dst}")
    print(f'next: run  "{dst / "terminal64.exe"}" /portable  and log into the {target} account yourself')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python scripts/setup_terminal.py <target|tester>")
    main(sys.argv[1])
