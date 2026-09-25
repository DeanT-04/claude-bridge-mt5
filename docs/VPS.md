# Running prop accounts on a Windows VPS

Everything is path-driven (`config/settings.yaml`) and `QB_Host` enforces each firm's rules
itself, so the same repo runs unchanged on a VPS. Research can stay on the PC; only the
prop-account terminals must run 24/5.

## 1. Choose the VPS
- Windows Server 2019+ (MT5 is Windows-native). 2 vCPU / 4 GB RAM runs several terminals;
  research needs more (or keep research on the PC).
- Low latency to the firms' MT5 servers (most are hosted in London/Equinix LD4 or New York NY4).
- Check each firm's terms: some restrict VPS providers or IP sharing across accounts.

## 2. Install
1. Python 3.12 (on PATH), Git, and each firm's MT5 terminal (or the BlackBull terminal plus the
   firm's server added at login).
2. `git clone https://github.com/DeanT-04/claude-bridge-mt5` and `pip install -r requirements.txt`.
3. Edit `config/settings.yaml`: `terminal.*` paths and one `terminals.<name>` entry per prop
   account (`profile`, `size`, `account_mode`).
4. `python scripts/setup_terminal.py <name>`, launch `runtime\<name>\terminal64.exe /portable`
   and **log in yourself** (save the password).
5. Copy `runtime/registry.sqlite` from the PC (gauntlets, genomes, ML specs, deployments) and
   `%APPDATA%\MetaQuotes\Terminal\Common\Files\QB\models\*.onnx` for any ML sleeves.

## 3. Start trading a challenge
1. MCP `install_host(target='<name>')`, then attach `QB_Host` to one chart with
   `InpConfig=portfolio_<name>.cfg`, Algo Trading on.
2. Add `<name>` to `account.enabled_targets` yourself.
3. `prop_preflight('<name>')` must be all OK.
4. `promote([...], target='<name>')` → review the diff → approve → `apply_deployment`.

## 4. Keep it running
- **Auto-start after reboots:** Task Scheduler "At log on" →
  `runtime\<name>\terminal64.exe /portable`, plus auto-logon for the VPS user (terminals need a
  desktop session). Charts, including QB_Host, are restored from the last profile.
- **Windows Update:** set active hours and defer reboots to the weekend.
- **Heartbeat:** `QB_Host` rewrites `host_status_portfolio_<name>.json` every 5 s, and
  `prop_preflight` flags it when it's more than 60 s old.
- **Time:** leave Windows time sync on; the daily loss limit uses broker server time.

## 5. Emergency stop
`powershell -ExecutionPolicy Bypass -File scripts\kill_switch.ps1 <name>` disables a portfolio
without Python or Claude: QB_Host closes all QB positions within a second. Keep a shortcut on
the VPS desktop.
