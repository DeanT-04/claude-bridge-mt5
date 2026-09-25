/* Prop Quant Lab dashboard. Data: window.PQ (built by `uv run propquant dashboard build`). */
(() => {
  "use strict";
  const PQ = window.PQ;
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pct = (x) => (x == null ? "—" : `${(x * 100).toFixed(0)}%`);
  const num = (x, d = 2) => (x == null ? "—" : Number(x).toFixed(d));
  const usd = (x) => (x == null ? "—" : `${x < 0 ? "−" : ""}$${Math.abs(x).toLocaleString(undefined, { maximumFractionDigits: 0 })}`);
  const TIERS = ["champion", "elite", "contender", "graveyard"];
  const tip = $("#tooltip");

  if (!PQ) {
    document.querySelector("main").innerHTML = '<section class="panel">No data yet. Run <code>uv run propquant dashboard build</code>.</section>';
    return;
  }

  // ---------- theme (per-viewer convenience only) ----------
  const root = document.documentElement;
  try { const t = localStorage.getItem("pq-theme"); if (t) root.dataset.theme = t; } catch (_) { /* storage blocked */ }
  $("#theme").addEventListener("click", () => {
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("pq-theme", root.dataset.theme); } catch (_) { /* ignore */ }
  });

  // ---------- summary ----------
  const S = PQ.summary;
  $("#generated").textContent = `Data built ${PQ.generated} UTC · ${S.trials.toLocaleString()} recorded trials`;
  const tiles = [
    [S.strategies, "strategies tested"], [S.runs, "gauntlet runs"],
    [S.tiers.champion, "champion"], [S.tiers.elite, "elite"],
    [S.tiers.contender, "contender"], [S.tiers.graveyard, "graveyard"],
    [S.trials.toLocaleString(), "configs tried (trials)"], [S.holdout_accesses, "holdout openings"],
  ];
  $("#tiles").innerHTML = tiles.map(([v, l]) => `<div class="tile"><div class="v">${esc(v)}</div><div class="l">${esc(l)}</div></div>`).join("");
  const done = S.catalogue_tested / Math.max(1, S.catalogue_total);
  $("#progress-bar").style.width = `${(done * 100).toFixed(1)}%`;
  $("#progress-label").textContent = `${S.catalogue_tested} of ${S.catalogue_total} planned tests done (${(done * 100).toFixed(1)}%)`;
  $("#catalogue").innerHTML = PQ.catalogue.map((c) => `<span class="${c.tested ? "done" : ""}" title="${esc(c.stage)}">${esc(c.key)}</span>`).join("");

  // ---------- table ----------
  const state = { q: "", tiers: new Set(), family: "", symbol: "", sort: "rank", asc: true, sel: null };
  PQ.strategies.forEach((s, i) => { s.rank = i + 1; });
  const families = [...new Set(PQ.strategies.map((s) => s.family).filter(Boolean))].sort();
  const symbols = [...new Set(PQ.strategies.map((s) => s.symbol))].sort();
  $("#family").insertAdjacentHTML("beforeend", families.map((f) => `<option>${esc(f)}</option>`).join(""));
  $("#symbol").insertAdjacentHTML("beforeend", symbols.map((f) => `<option>${esc(f)}</option>`).join(""));
  $("#tier-chips").innerHTML = TIERS.map((t) => `<button class="chip" type="button" data-t="${t}" aria-pressed="false">${t} (${S.tiers[t]})</button>`).join("");
  $("#tier-chips").addEventListener("click", (e) => {
    const b = e.target.closest(".chip"); if (!b) return;
    const t = b.dataset.t;
    state.tiers.has(t) ? state.tiers.delete(t) : state.tiers.add(t);
    b.setAttribute("aria-pressed", state.tiers.has(t));
    render();
  });
  $("#search").addEventListener("input", (e) => { state.q = e.target.value.toLowerCase(); render(); });
  $("#family").addEventListener("change", (e) => { state.family = e.target.value; render(); });
  $("#symbol").addEventListener("change", (e) => { state.symbol = e.target.value; render(); });
  document.querySelectorAll("#table th").forEach((th) => th.addEventListener("click", () => {
    const k = th.dataset.k;
    state.asc = state.sort === k ? !state.asc : ["key", "family", "verdict", "plan", "rank"].includes(k);
    state.sort = k; render();
  }));

  function rows() {
    let r = PQ.strategies.filter((s) =>
      (!state.q || s.key.toLowerCase().includes(state.q) || (s.family || "").includes(state.q)) &&
      (!state.tiers.size || state.tiers.has(s.verdict)) &&
      (!state.family || s.family === state.family) &&
      (!state.symbol || s.symbol === state.symbol));
    const k = state.sort, dir = state.asc ? 1 : -1;
    r.sort((a, b) => {
      const x = k === "verdict" ? TIERS.indexOf(a.verdict) : a[k], y = k === "verdict" ? TIERS.indexOf(b.verdict) : b[k];
      return (x > y ? 1 : x < y ? -1 : 0) * dir;
    });
    return r;
  }

  function render() {
    const r = rows();
    document.querySelectorAll("#table th").forEach((th) => {
      th.classList.toggle("sorted", th.dataset.k === state.sort);
      th.classList.toggle("asc", th.dataset.k === state.sort && state.asc);
    });
    $("#table tbody").innerHTML = r.map((s) => `
      <tr data-key="${esc(s.key)}" class="${s.key === state.sel ? "sel" : ""}">
        <td>${s.rank}</td><td>${esc(s.key)}</td><td>${esc(s.family)}</td>
        <td><span class="badge t-${s.verdict}">${esc(s.verdict)}</span></td><td>${esc(s.plan)}</td>
        <td class="num">${pct(s.e2e)}</td><td class="num">${pct(s.eval_pass)}</td>
        <td class="num">${usd(s.ev)}</td><td class="num">${num(s.dsr)}</td>
        <td class="num">${pct(s.re_pct)}</td><td class="num">${(s.oos_trades ?? 0).toLocaleString()}</td>
        <td class="num">${s.runs}</td>
      </tr>`).join("");
    $("#count").textContent = `${r.length} of ${PQ.strategies.length} strategies shown`;
  }
  $("#table tbody").addEventListener("click", (e) => {
    const tr = e.target.closest("tr"); if (!tr) return;
    state.sel = tr.dataset.key; render(); showDetail(state.sel);
  });

  // ---------- charts (inline SVG) ----------
  function lineChart(series, { height = 220, yfmt = (v) => v.toFixed(0) } = {}) {
    const W = 760, H = height, P = { l: 56, r: 12, t: 10, b: 24 };
    const pts = series.flatMap((s) => s.points);
    if (!pts.length) return "<p class='muted small'>No data.</p>";
    const xs = pts.map((p) => p.x), ys = pts.map((p) => p.y).concat([0]);
    const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    const sx = (x) => P.l + ((x - x0) / Math.max(1, x1 - x0)) * (W - P.l - P.r);
    const sy = (y) => P.t + (1 - (y - y0) / Math.max(1e-9, y1 - y0)) * (H - P.t - P.b);
    const ticks = 4, grid = [];
    for (let i = 0; i <= ticks; i++) {
      const v = y0 + ((y1 - y0) * i) / ticks;
      grid.push(`<line class="axis" x1="${P.l}" x2="${W - P.r}" y1="${sy(v)}" y2="${sy(v)}"/><text class="lbl" x="${P.l - 6}" y="${sy(v) + 4}" text-anchor="end">${esc(yfmt(v))}</text>`);
    }
    const first = new Date(x0), last = new Date(x1);
    const paths = series.map((s) => `<path d="${s.points.map((p, i) => `${i ? "L" : "M"}${sx(p.x).toFixed(1)},${sy(p.y).toFixed(1)}`).join("")}" fill="none" stroke="${s.color}" stroke-width="2" stroke-linejoin="round"/>`).join("");
    const id = `c${Math.random().toString(36).slice(2)}`;
    setTimeout(() => attachHover(id, series, sx, sy, yfmt), 0);
    return `<svg class="chart" id="${id}" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="Equity chart">
      ${grid.join("")}<line class="axis" x1="${P.l}" x2="${W - P.r}" y1="${sy(0)}" y2="${sy(0)}" stroke-dasharray="3 3"/>
      <text class="lbl" x="${P.l}" y="${H - 6}">${first.toISOString().slice(0, 10)}</text>
      <text class="lbl" x="${W - P.r}" y="${H - 6}" text-anchor="end">${last.toISOString().slice(0, 10)}</text>
      ${paths}<circle class="dot" r="4" fill="none" stroke="currentColor" opacity="0"/></svg>
      <div class="legend">${series.map((s) => `<span style="--c:${s.color}">${esc(s.name)}</span>`).join("")}</div>`;
  }

  function attachHover(id, series, sx, sy, yfmt) {
    const svg = document.getElementById(id); if (!svg) return;
    const dot = svg.querySelector(".dot");
    const all = series.flatMap((s) => s.points.map((p) => ({ ...p, name: s.name, color: s.color })));
    svg.addEventListener("mousemove", (e) => {
      const r = svg.getBoundingClientRect();
      const vx = ((e.clientX - r.left) / r.width) * 760;
      let best = null, bd = Infinity;
      for (const p of all) { const d = Math.abs(sx(p.x) - vx); if (d < bd) { bd = d; best = p; } }
      if (!best) return;
      dot.setAttribute("cx", sx(best.x)); dot.setAttribute("cy", sy(best.y)); dot.setAttribute("opacity", 1);
      dot.setAttribute("stroke", best.color);
      tip.innerHTML = `${esc(best.name)}<br>${new Date(best.x).toISOString().slice(0, 10)}: ${esc(yfmt(best.y))}`;
      tip.style.left = `${e.clientX + 12}px`; tip.style.top = `${e.clientY + 12}px`; tip.style.opacity = 1;
    });
    svg.addEventListener("mouseleave", () => { tip.style.opacity = 0; dot.setAttribute("opacity", 0); });
  }

  const css = (v) => getComputedStyle(root).getPropertyValue(v).trim();

  // ---------- detail ----------
  function showDetail(key) {
    const s = PQ.strategies.find((x) => x.key === key);
    const run = PQ.runs[s.latest_run];
    const d = $("#detail");
    d.classList.remove("hidden");
    if (!run) {
      d.innerHTML = `<div class="detail-head"><h2>${esc(key)}</h2><button class="close" type="button">Close</button></div>
        <p class="muted">This run predates detailed run records (only its summary was stored). Re-running it would re-count trials and the holdout is already used.</p>${historyTable(s)}`;
      d.querySelector(".close").onclick = () => d.classList.add("hidden");
      d.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    const oos = run.oos_equity, ho = run.holdout_equity;
    const toPts = (e) => e ? e.dates.map((t, i) => ({ x: Date.parse(t), y: e.equity[i] })) : [];
    const hoPts = ho ? ho.dates.map((t, i) => ({ x: Date.parse(t), y: (oos.equity.at(-1) || 0) + ho.equity[i] })) : [];
    const plans = Object.keys(run.oos_challenge);
    const chRows = ["eval_pass", "eval_fail", "eval_expired", "median_sessions_to_pass", "first_payout_given_pass", "end_to_end_payout", "ev_per_attempt", "ev_p05", "starts"];
    const fmt = (k, v) => (k.startsWith("ev_") ? usd(v) : ["starts", "median_sessions_to_pass"].includes(k) ? num(v, 0) : pct(v));
    const chosen = new Set(run.folds.map((f) => JSON.stringify(f.params)));
    const finalKey = JSON.stringify(run.final_params);
    const gridSorted = [...run.grid].sort((a, b) => (b.dev_sharpe_ann ?? -99) - (a.dev_sharpe_ann ?? -99));
    const pkeys = Object.keys(run.grid[0]?.params || {});

    d.innerHTML = `
      <div class="detail-head">
        <h2>${esc(s.key)} <span class="badge t-${run.verdict}">${esc(run.verdict)}</span></h2>
        <button class="close" type="button">Close</button>
      </div>
      <p class="muted small">Run <code>${esc(run.run_id)}</code> · ${esc(run.created)} · commit <code>${esc(run.commit)}</code> · data <code>${esc(run.data_hash)}</code> · best plan <b>Apex ${esc(run.best_plan)} 50K</b></p>
      <div class="grid2">
        <div>
          <h3>Gates</h3>
          <table><thead><tr><th>Gate</th><th class="num">Value</th><th>Needs</th><th>Result</th></tr></thead><tbody>
          ${run.checks.map((c) => `<tr><td>${esc(c.gate)}</td><td class="num">${num(c.value, 3)}</td><td>${esc(c.needs)}</td><td class="${c.result === "PASS" ? "pass" : "fail"}">${c.result}</td></tr>`).join("")}
          </tbody></table>
        </div>
        <div>
          <h3>Challenge Monte Carlo (out-of-sample)</h3>
          <table><thead><tr><th>Metric</th>${plans.map((p) => `<th class="num">${esc(p)}</th>`).join("")}</tr></thead><tbody>
          ${chRows.map((k) => `<tr><td>${esc(k.replaceAll("_", " "))}</td>${plans.map((p) => `<td class="num">${fmt(k, run.oos_challenge[p][k])}</td>`).join("")}</tr>`).join("")}
          </tbody></table>
          <h3>Statistics</h3>
          <dl class="kv">
            <dt>OOS Sharpe (ann.)</dt><dd>${num(run.stats.oos_sharpe_ann)}</dd>
            <dt>Deflated Sharpe</dt><dd>${num(run.stats.dsr, 3)} over ${run.stats.n_trials} trials</dd>
            <dt>Beats random entry</dt><dd>${pct(run.stats.re_percentile)}</dd>
            <dt>OOS trades / P&amp;L per micro</dt><dd>${run.stats.oos_trades.toLocaleString()} / ${usd(run.stats.oos_total)}</dd>
            <dt>Holdout</dt><dd>${esc(run.holdout_note)}</dd>
            <dt>Final sizes (micros)</dt><dd>${esc(JSON.stringify(run.final_sizes))}</dd>
          </dl>
        </div>
      </div>
      <h3>Equity per micro, after costs</h3>
      ${lineChart([{ name: "walk-forward out-of-sample", color: css("--s1"), points: toPts(oos) },
                   { name: "locked holdout", color: css("--s2"), points: hoPts }], { yfmt: (v) => usd(v) })}
      <h3>Optimisation: every configuration tried (${run.grid.length}), dev period 2016 → holdout</h3>
      <p class="muted small">Highlighted rows were picked by at least one walk-forward fold on its training years. ★ = final pick for the holdout.</p>
      <div class="table-wrap"><table><thead><tr>${pkeys.map((k) => `<th>${esc(k)}</th>`).join("")}<th class="num">Sharpe (ann.)</th><th class="num">Trades</th><th class="num">Win rate</th><th class="num">Net P&amp;L / micro</th></tr></thead><tbody>
      ${gridSorted.map((g) => { const k = JSON.stringify(g.params); return `<tr class="${chosen.has(k) ? "chosen" : ""}">${pkeys.map((p) => `<td>${esc(JSON.stringify(g.params[p]))}${p === pkeys[0] && k === finalKey ? " ★" : ""}</td>`).join("")}<td class="num">${num(g.dev_sharpe_ann)}</td><td class="num">${g.trades.toLocaleString()}</td><td class="num">${pct(g.win_rate)}</td><td class="num">${usd(g.net_pnl)}</td></tr>`; }).join("")}
      </tbody></table></div>
      <h3>Walk-forward folds</h3>
      <div class="table-wrap"><table><thead><tr><th>Test year</th><th>Params (chosen on training years)</th><th class="num">Train Sharpe (daily)</th><th>Sizes</th><th>Sizing policy (α, β, μ)</th></tr></thead><tbody>
      ${run.folds.map((f) => `<tr><td>${f.test_year}</td><td><code>${esc(JSON.stringify(f.params))}</code></td><td class="num">${num(f.train_sharpe, 3)}</td><td>${esc(JSON.stringify(f.sizes))}</td><td>${esc(JSON.stringify(f.policies))}</td></tr>`).join("")}
      </tbody></table></div>
      ${historyTable(s)}
      <h3>Evidence charts</h3>
      <div class="imgs">${run.charts.map((c) => `<img loading="lazy" alt="${esc(c)}" src="../docs/vault/attachments/${encodeURIComponent(c)}">`).join("")}</div>`;
    d.querySelector(".close").onclick = () => { d.classList.add("hidden"); state.sel = null; render(); };
    d.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function historyTable(s) {
    return `<h3>Run history (${s.history.length})</h3>
      <table><thead><tr><th>When (UTC)</th><th>Run</th><th>Tier</th><th class="num">Reach payout</th><th class="num">Eval pass</th><th class="num">DSR</th></tr></thead><tbody>
      ${[...s.history].reverse().map((h) => `<tr><td>${esc(h.ts)}</td><td><code>${esc(h.run_id)}</code>${h.detail ? "" : " <span class='muted small'>(summary only)</span>"}</td><td><span class="badge t-${h.verdict}">${esc(h.verdict)}</span></td><td class="num">${pct(h.e2e)}</td><td class="num">${pct(h.eval_pass)}</td><td class="num">${num(h.dsr)}</td></tr>`).join("")}
      </tbody></table>`;
  }

  render();
})();
