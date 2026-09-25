# PANIC STOP - works without Python, the bridge or Claude.
# Rewrites portfolio_<target>.cfg with enabled=0; QB_Host notices within a second, closes every
# QB position and stops trading. Re-enabling needs a new approved proposal.
#
#   powershell -ExecutionPolicy Bypass -File scripts\kill_switch.ps1 live
#   powershell -ExecutionPolicy Bypass -File scripts\kill_switch.ps1 demo
param([ValidateSet("demo", "live")][string]$Target = "live")

$cfg = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files\QB\portfolio_$Target.cfg"
if (-not (Test-Path $cfg)) { Write-Host "No $Target config at $cfg - nothing is deployed."; exit 0 }

$lines = Get-Content $cfg
$found = $false
$out = foreach ($l in $lines) {
    if ($l -match '^enabled=') { $found = $true; 'enabled=0' }
    elseif ($l -match '^version=(\d+)$') { "version=$([int]$Matches[1] + 1)" }
    else { $l }
}
if (-not $found) { $out = @('enabled=0') + $out }
$tmp = "$cfg.tmp"
Set-Content -Path $tmp -Value $out -Encoding Ascii
Move-Item -Force $tmp $cfg
Write-Host "KILLED: $Target portfolio disabled ($cfg). QB_Host will close all QB positions."
Write-Host "Tell Claude so the registry records it (or run: python -c ""from bridge import deploy; deploy.kill('$Target','panic script')"")."
