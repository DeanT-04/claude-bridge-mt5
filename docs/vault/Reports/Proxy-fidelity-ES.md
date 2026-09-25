---
type: report
kind: proxy-fidelity
symbol: ES
generated: 2026-09-25
---
# Proxy fidelity: ES

The Dukascopy index CFD (mid of bid/ask) compared with real CME futures from Yahoo, on
overlapping bar-open timestamps. Futures roll gaps are excluded as outliers and counted.
A timeframe is **usable** only if every one of these holds (fixed before the run):
`ret_corr >= 0.95`, `range_corr >= 0.85`, `up_exc_corr >= 0.85`, `down_exc_corr >= 0.85`.

## Bar-level fidelity
| timeframe | n | excluded_outliers | ret_corr | beta | sign_agree | range_corr | up_exc_corr | down_exc_corr | tracking_err_bps | fut_ret_std_bps | usable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1m | 8158 | 2 | 0.9854 | 0.9861 | 0.9629 | 0.9767 | 0.9587 | 0.9629 | 0.2508 | 1.4667 | yes |
| 5m | 12900 | 11 | 0.9973 | 0.9972 | 0.9856 | 0.9951 | 0.9911 | 0.9922 | 0.2860 | 3.8825 | yes |
| 1h | 12461 | 52 | 0.9994 | 0.9987 | 0.9910 | 0.9885 | 0.9885 | 0.9844 | 0.6867 | 20.3 | yes |

## Timing fidelity (1m, regular session 09:30-16:00 ET)
- Sessions compared: **6**
- Session high at the same time (±5 min): **100.0%**
- Session low at the same time (±5 min): **100.0%**
- Within 15m bars, same high-before-low order: **96.1%**
  (545 bars)

## Evidence
![[proxy-fidelity-ES-scatter.png]]
![[proxy-fidelity-ES-rolling.png]]
![[proxy-fidelity-ES-overlay.png]]

## Known differences
- The proxy tracks the cash index, futures carry a basis, so price levels differ. Only returns
  and shapes are compared.
- The 16:00 ET hourly bar is excluded from the 1h comparison (futures cover the full hour,
  the proxy 16:00-16:15). Remaining exclusions are Yahoo's continuous-contract roll glitches
  (e.g. 2025-09-16, alternating +/-100 bps) and after-hours news.
- The proxy has no bars 16:15-17:00 ET (the futures still trade). Strategies can't use that window.
- Proxy volume is a tick-activity count, not contracts. Volume-based rules need care.

Reproduce: `uv run propquant data tracking --symbol ES`
