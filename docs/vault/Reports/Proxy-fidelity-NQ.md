---
type: report
kind: proxy-fidelity
symbol: NQ
generated: 2026-09-25
---
# Proxy fidelity: NQ

The Dukascopy index CFD (mid of bid/ask) compared with real CME futures from Yahoo, on
overlapping bar-open timestamps. Futures roll gaps are excluded as outliers and counted.
A timeframe is **usable** only if every one of these holds (fixed before the run):
`ret_corr >= 0.95`, `range_corr >= 0.85`, `up_exc_corr >= 0.85`, `down_exc_corr >= 0.85`.

## Bar-level fidelity
| timeframe | n | excluded_outliers | ret_corr | beta | sign_agree | range_corr | up_exc_corr | down_exc_corr | tracking_err_bps | fut_ret_std_bps | usable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1m | 8191 | 6 | 0.9920 | 0.9856 | 0.9562 | 0.9918 | 0.9879 | 0.9864 | 0.2697 | 2.1188 | yes |
| 5m | 12893 | 19 | 0.9983 | 0.9943 | 0.9793 | 0.9958 | 0.9923 | 0.9910 | 0.3993 | 6.7619 | yes |
| 1h | 12429 | 80 | 0.9996 | 0.9970 | 0.9894 | 0.9882 | 0.9911 | 0.9834 | 0.8008 | 27.2 | yes |

## Timing fidelity (1m, regular session 09:30-16:00 ET)
- Sessions compared: **6**
- Session high at the same time (±5 min): **100.0%**
- Session low at the same time (±5 min): **100.0%**
- Within 15m bars, same high-before-low order: **98.7%**
  (545 bars)

## Evidence
![[proxy-fidelity-NQ-scatter.png]]
![[proxy-fidelity-NQ-rolling.png]]
![[proxy-fidelity-NQ-overlay.png]]

## Known differences
- The proxy tracks the cash index, futures carry a basis, so price levels differ. Only returns
  and shapes are compared.
- The 16:00 ET hourly bar is excluded from the 1h comparison (futures cover the full hour,
  the proxy 16:00-16:15). Remaining exclusions are Yahoo's continuous-contract roll glitches
  (e.g. 2025-09-16, alternating +/-100 bps) and after-hours news.
- The proxy has no bars 16:15-17:00 ET (the futures still trade). Strategies can't use that window.
- Proxy volume is a tick-activity count, not contracts. Volume-based rules need care.

Reproduce: `uv run propquant data tracking --symbol NQ`
