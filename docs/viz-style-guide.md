# Visualization style guide

Rules for any chart the agent makes, in any charting tool.

## When a chart earns its place

Make a chart only when it shows something a sentence or a small table cannot:

- a trend of six or more points,
- a comparison of five or more segments,
- or when the user asks for one.

Otherwise, give the number in a sentence or a short table. A chart that repeats one number is noise.

## How it is drawn

- **The title states the finding**, not the topic: "Weekend orders fell for three weeks", not "Orders by week".
- **Label both axes, with units.** Format numbers for reading (thousands separators, percentages as percentages).
- **Bars start at zero.** A line chart may use a tighter axis when the change is the point, and says so.
- **A handful of series at most.** More than about five, and the chart becomes a puzzle: split it or highlight one series and grey the rest.
- **Use a colour-blind-safe palette**, and never let colour carry meaning on its own: label the series directly where possible.
- **The caption names the source and the date window**, for example "Source: `<orders_table>`, 2026-01-01 to 2026-03-31, UTC".
- No 3D, no dual axes unless the user asks, no decoration that carries no data.

## Where it is saved

Save the chart image next to the data it was drawn from, in the same dated folder, with a file name that says what it shows. A filed chart can always be redrawn from the data beside it.
