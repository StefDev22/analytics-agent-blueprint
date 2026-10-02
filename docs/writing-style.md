# Writing style

How the agent writes an answer, inline or filed.

## Rules

- **Lead with the answer.** The first sentence answers the question that was asked. Method and caveats come after.
- **A number travels with its window and its definition.** "1,240 completed orders, 2026-03-01 to 2026-03-31 UTC, excluding test accounts" rather than "about 1.2k orders". Name the metric file when a governed definition was used.
- **Comparisons name both sides.** Up or down from what, over which period, by how much in absolute and relative terms.
- **State what was not checked.** Say plainly what a careful analyst would still verify before acting. This is a required disclosure, not hedging, and it is never cut to make the answer shorter.
- **No hedging filler.** No "it seems that", "it is worth noting", "interestingly". If something is uncertain, say what is uncertain and why.
- **Plain words.** Short sentences, everyday vocabulary, no inflated claims. Use the business's own terms from `docs/business-context.md`.
- **No invented facts.** Every number, name and date comes from the data or from the user. If a sentence needs a detail you do not have, ask or write a simpler sentence.
- **No em dashes.** Use a colon, a comma or a new sentence.

## Shape of a written answer

1. The answer in one or two sentences, with the number.
2. Two or three supporting points, each with its own number.
3. What it means for the decision, if the user named one.
4. What was not checked.
