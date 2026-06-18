# Sailing Planner

An interactive dashboard for ocean-freight routing options, booking deadlines, and ML arrival predictions. It reads the standardized lane JSON files (one file per origin→destination lane) and turns them into something you can actually reason about.

> ⚠️ **Internal use.** `shipment-dashboard.html` has the lane data embedded directly in the file. Keep this repository **private** — anyone who can read the repo or the rendered page can see the freight data.

## Open it

It's a single self-contained HTML file — no build step, no server, no dependencies.

- **Just open `shipment-dashboard.html`** in any browser (double-click, or `file://`). It loads pre-populated with the embedded lanes.
- Or serve the folder over any static host and open the file.

Everything runs locally in the browser. Nothing is uploaded.

## The three views

| View | Purpose |
|------|---------|
| **▦ Portfolio** | Compare all lanes at once — risk split, recommended sailing, likely arrival, fastest transit, next cutoff per lane. Includes a short explainer of how to read the predictions. Click a lane to drill in. |
| **🚢 Lane detail** | One lane: KPIs, a shared **timeline** (scheduled voyage, transshipment hubs, booking cutoffs, and the p10–p90 prediction band), a sortable options table, and a port map. Click any sailing for a full detail panel. |
| **⏱ Deadlines** | Every booking cutoff across all lanes, urgency-sorted, counting down from the live clock. Filter by lane and time window. |

### Reading the timeline
- **Solid bar** = scheduled voyage (shaded per leg; amber dots = transshipment hubs)
- **Amber tick** = booking cutoff (container gate-in)
- **Purple band** = predicted arrival window (p10–p90); **green mark** = most likely (p50)
- **White tick** = scheduled arrival · **red dashed line** = today

### Reading the predictions
- **Schedule vs. prediction** — carriers publish a *scheduled* arrival; the model predicts a *likely* range (p10 optimistic → p50 most likely → p90 pessimistic).
- **Journey risk** — Green = expected on time; Red = elevated delay risk (usually a tight transshipment connection).
- **Transshipment risk** — *connection %* = chance the box makes the onward vessel; *roll risk* = chance it's bumped to a later sailing.
- **On-time probability** — chance of arriving by the scheduled date.

All countdowns use the viewer's local clock.

## Adding or refreshing data

**At runtime (no rebuild):** drag-and-drop any lane JSON files onto the page, or use **Load JSON files**. Loaded lanes are added/merged on the fly.

**To re-bake the embedded set** (so the file opens pre-populated with new data), run the build script and commit the updated HTML:

```bash
python3 embed-data.py                 # auto-finds lane files in ~/Downloads
python3 embed-data.py a.json b.json   # or pass specific files
```

The script inlines the JSON into `shipment-dashboard.html` (replacing whatever was embedded before). Re-run it any time the source files change.

## Files

- `shipment-dashboard.html` — the dashboard (data embedded)
- `embed-data.py` — rebuilds the embedded data set from lane JSON files

## Input format

Each lane file is `{ "data": [ ...sailings... ] }`. Each sailing carries its carrier, legs (vessels/ports/dates), booking `deadlines`, and a `prediction` block (p10/p50/p90 transit + arrival, `journey_risk`, `on_time_probability`, and per-hub connection odds). Missing `prediction`, `score`, or `arrival_date` are handled gracefully.
