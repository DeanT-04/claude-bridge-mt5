# Moving to a Windows VPS

Everything is path-driven (`config/settings.yaml`) and `QB_Host` enforces its own risk limits, so
the same repo runs unchanged on a VPS. Research can stay on the PC; only the trading terminals
must run 24/5.

## 1. Choose the VPS
- Windows Server 2019+ (MT5 is Windows-native). 2 vCPU / 4 GB RAM is plenty for trading terminals
  alone; research needs more (or keep research on the PC).
- Low latency to BlackBull's servers (London / New York / Equinix LD4 or NY4 regions).
- Alternative: MetaQuotes' built-in **MQL5 VPS** (rent from inside the terminal). It runs the EA
  and its chart but **not Python**, so config changes then mean re-migrating; the self-managed
  VPS keeps the full bridge.

## 2. Install
1. Install MT5 from BlackBull, and Python 3.12 (add it to PATH), then Git.
2. `git clone https://github.com/DeanT-04/claude-bridge-mt5` and `pip install -r requirements.txt`.
3. Edit `config/settings.yaml`: `terminal.install_dir`, `terminal.data_dir`, `terminals.demo`,
   `terminals.live` for the VPS paths.
4. `python scripts/setup_terminal.py live`, launch `runtime\live\terminal64.exe /portable` and
   **log in yourself** (save the password).
5. Copy `runtime/registry.sqlite` from the PC (deployment history, gauntlets, genomes, ML specs)
   and `%APPDATA%\MetaQuotes\Terminal\Common\Files\QB\models\*.onnx` for any ML sleeves.

## 3. Start trading
1. MCP `install_host(target='live')`, then attach `QB_Host` to one chart with
   `InpConfig=portfolio_live.cfg`, Algo Trading on.
2. `live_preflight()` must be all OK.
3. `promote_to_live(...)` → review the diff → approve → `apply_deployment`.

## 4. Keep it running
- **Auto-start after reboots:** Task Scheduler → "At log on" →
  `runtime\live\terminal64.exe /portable`, plus enable auto-logon for the VPS user (the terminal
  needs a desktop session). Charts, including QB_Host, are restored from the last profile.
- **Windows Update:** set active hours / defer reboots to the weekend when markets are closed.
- **Heartbeat:** `QB_Host` rewrites `host_status_portfolio_live.json` every 5 s. `live_preflight`
  flags it if it's more than 60 s old. A scheduled check that emails/notifies on a stale file is
  a planned addition.
- **Time:** leave Windows time sync on; the EA uses broker server time for its daily loss limit.

## 5. Emergency stop
`powershell -ExecutionPolicy Bypass -File scripts\kill_switch.ps1 live` disables the portfolio
without Python or Claude: QB_Host closes all QB positions within a second. Keep a shortcut to it
on the VPS desktop.
