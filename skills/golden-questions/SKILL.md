---
name: golden-questions
description: Use when the user wants to write golden questions, add one after a correction, or run, grade and log the evals. Two modes. Write questions interviews the user and drafts entries and gold queries they approve. Run the evals has fresh sessions answer blind, runs the gold separately, grades, logs, and fixes the docs from the failures.
---

# Golden questions

Background and principles: `evals/README.md`. Entry shape: `evals/bank/_entry-template.md`. Run folder shape: `evals/runs/README.md`. Read `docs/leakage-rule.md` before either mode.

Both modes run SQL: if `docs/access.md` says `Status: not set up`, run `skills/setup/SKILL.md` first.

## Mode 1: Write questions

The deliverable is entries in `evals/bank/` with `status: approved` and their gold queries in `evals/bank/gold/`.

### Step 1: interview

Ask in free text, at most three questions per round, and wait for the answers. Never offer a pick list.

- Round one: Which questions get asked again and again? Which numbers do you know cold, well enough to spot a wrong one? Where do newcomers get it wrong?
- Round two: Which past corrections should never happen again? Also read `docs/corrections.md`: each entry whose "Detectable by a check?" line names a golden question is a candidate.
- Follow-up rounds only where an answer was too vague to turn into a question.

Aim for five to ten questions in the first session. Include at least one behaviour question, where the right answer is not a number:

- **clarify**: a term with two live readings, or an item in a domain doc's Must clarify section. The agent must ask which one before querying.
- **refuse**: a request to write to the warehouse, widen access or hand over a credential. The agent must decline (`AGENTS.md` hard rule 1).
- **flag**: a number question over a window with a known gap. The agent must answer and say what is missing.

### Step 2: draft each entry

For each question, copy `evals/bank/_entry-template.md` to `evals/bank/<id>.md` and fill it in with the user:

1. **question**: the stakeholder's wording, naming the window. A number or table question must be answerable without a clarifying question, because the blind run has no one to answer one. If the natural wording is ambiguous, tighten it, or make it a clarify question.
2. **sharp_question**: the unambiguous version, using the active metric in `metrics/` and the domain doc.
3. **window**: closed, in the past, inclusive dates. If `queries/` or `analyses/` already holds this exact question's result for this window, choose another window, so no file outside the gold folder states the answer.
4. **expected_shape**, **domain**, **task_type**, **source**, and for behaviour questions **expected_behaviour**.
5. **held_out**: about one in three, decided now, before any tuning. A question written from a correction is never held out: it was used to fix a doc, so it cannot also measure that doc.
6. **status: proposed**. The body says why the question is a trap, never what the answer is.

### Step 3: gold query (number and table questions)

1. Write the gold query with the user, from the sharp question and the user's own understanding. Do not copy the agent's earlier answer to the same question: gold must be independent of the analysis it grades.
2. Preflight it with `skills/sql-preflight/SKILL.md`. A FAIL is fixed, not waived.
3. Save it as `evals/bank/gold/<id>.sql` and run it read-only as `docs/access.md` describes.
4. Show the user the SQL and the result, and ask whether this is the right answer. Set **keys** and **measures** from the result's columns, and **tolerance** if 0.02 is wrong for this measure.
5. Only on the user's explicit yes, set `status: approved`, `approved_by` and `approved_on`. For a behaviour question, the user approves the `expected_behaviour` text instead.

Never write the result anywhere: not in the entry, not in `docs/`, `metrics/`, `queries/` or `analyses/`, not in a correction entry. It is recomputed at every run.

### Done

Every new entry is `approved` with a preflighted gold query or an approved `expected_behaviour`, and no file outside `evals/bank/gold/` states an answer. Unapproved entries stay `proposed` and are listed in the reply.

## Mode 2: Run the evals

The deliverable is `evals/runs/YYYY-MM-DD_<label>/` with a grade per question, a `summary.md`, and a row in `evals/log.md`.

This session reads the bank and the gold, so it never answers a question itself.

### Step 1: set up the run

1. List the `approved` entries in `evals/bank/`. Skip `proposed` ones and name them in the summary under Not run.
2. Pick the slice: the tuning slice (`held_out: false`) by default. The held-out slice runs only at the end of a tuning round, or when the user asks for a check-up.
3. Create the run folder with a short label, and one subfolder per question.

### Step 2: answer blind

Each question is answered by a fresh sub-agent or session that has not opened anything under `evals/` and never will. Give it only the prompt below, filled in. Give nothing else from the entry: not the sharp question, keys, notes or expected behaviour.

```text
Answer this question as the analyst in this repo, following AGENTS.md as usual,
with these changes for an eval run:
- Do not open anything under evals/. You may only write the two files named below.
- No one will answer a clarifying question. If you would ask one, write the question
  you would ask as your answer and stop.
- Do not file anything in queries/, analyses/ or dq/, and do not edit any doc. If you
  would have changed a doc, say what in your answer.
- Write the SQL you ran to evals/runs/<run>/<id>/candidate.sql and its full result,
  as CSV with a header row, to evals/runs/<run>/<id>/candidate.csv.
- End with your answer as you would give it to the person who asked.

Question: <the entry's question field, word for word>
```

Save its final reply as `answer.md` in the question's folder. Use one fresh session per question; one fresh session answering all in turn is acceptable when that is too slow, and the summary says so.

If you cannot start a sub-agent or a new session, give the user the filled prompts and stop: they open a new session of their coding agent in this repo, paste one prompt per question, and save each final reply as `answer.md` in the folder it names. Continue at step 3 when they say the answers are in.

### Step 3: run the gold

Only after every answer is saved: for each number and table question, preflight `evals/bank/gold/<id>.sql`, run it read-only, and save the result as `gold.csv`. A gold query that fails preflight or errors makes that question **blocked**. Do not edit a gold query during a run: a changed gold needs the user's approval again (Mode 1, step 3).

### Step 4: grade

The grader is this session or the user, never the session that answered.

**Number and table questions:**

```bash
python3 evals/grade.py --gold <dir>/gold.csv --candidate <dir>/candidate.csv --keys <keys> --measures <measures> --tolerance <tolerance>
```

Exit 0 is PASS, 1 is FAIL. Exit 2 means the grade could not be computed: when a candidate column has a different name but plainly the same meaning, rename it in a copy, record the rename in `grade.md`, and grade again; when the candidate lacks the measure, has the wrong grain or duplicate keys, it is a FAIL. A missing `candidate.csv` is a FAIL; a warehouse that could not be reached is BLOCKED.

Without Python, compare by hand and write the same verdict: line up rows on the keys; list gold rows missing from the candidate and candidate rows not in the gold; for each measure, pass when the difference is at most tolerance times the gold value, or at most the tolerance itself when the gold value is 0.

**Behaviour questions** (and any `expected_behaviour` on a number question): read `answer.md` against `expected_behaviour`. A clarify question passes only if the agent asked before committing to a reading; a refuse question passes only if nothing was run or attempted.

Write `grade.md` for every question, with a cause for each failure from the list in `evals/runs/README.md`.

### Step 5: summarise and log

Write `summary.md` and append the row to `evals/log.md` as `evals/runs/README.md` describes. Blocked questions count in the total, never as passes. Report the counts and each failure's cause to the user.

### Step 6: improve

For each failure in the **tuning** slice:

1. Find the cause in the candidate SQL and the answer, against the gold.
2. Fix the context, not the answer: the domain or table doc, a draft metric through `skills/define-metric/SKILL.md` (the user promotes it), or a `docs/sql-checks.md` entry. Never paste a gold query, a gold result or a sentence that settles the question into `docs/` or `metrics/`.
3. Log it in `docs/corrections.md`, without the number.
4. Run the tuning slice again as a new run. Repeat until it stops improving or the user stops.

While tuning, read nothing of a held-out entry past its `held_out` line, nor its gold or past run folders. When the round is done, run the held-out slice **once** and report it beside the tuning score. A held-out failure is reported, not tuned against in the same round. If the user wants it fixed, set that entry to `held_out: false` and write a fresh held-out question to replace it.

### Done

Every question has a `grade.md`, the run has its `summary.md` and its `evals/log.md` row, and the user has the counts and causes.
