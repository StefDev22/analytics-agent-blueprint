#!/usr/bin/env python3
"""Grade a candidate result against a gold result. Standard library only.

  python3 evals/grade.py --gold gold.csv --candidate candidate.csv --keys k1,k2 --measures m1,m2 [--tolerance 0.02]
  python3 evals/grade.py --self-test

Rows align on the key columns; with no keys each file must hold one row. Measures compare within a
relative tolerance, absolute when the gold value is 0. Column names match case-insensitively; other
columns are ignored. Exit 0 PASS, 1 FAIL, 2 usage or input error.
"""
import argparse
import csv
import io
import sys


class InputError(Exception):
    pass


def number(cell):
    try:
        return float(cell)
    except ValueError:
        return None


def read_rows(text, label, columns):
    """Rows as dicts keyed by lowercased column name."""
    reader = csv.reader(io.StringIO(text))
    header = [name.strip().lower() for name in next(reader, [])]
    if not header:
        raise InputError(f"{label}: the file has no header row")
    missing = [col for col in columns if col not in header]
    if missing:
        raise InputError(f"{label}: missing column(s): {', '.join(missing)}")
    return [dict(zip(header, (c.strip() for c in row))) for row in reader if any(c.strip() for c in row)]


def index(rows, keys, label):
    """Map each row's key to the row. A key cell that reads as a number matches as one: 2026 equals 2026.0."""
    out = {}
    for row in rows:
        key = tuple(row.get(k, "") if number(row.get(k, "")) is None else repr(number(row[k])) for k in keys)
        if key in out:
            raise InputError(f"{label}: duplicate key ({where(row, keys) if keys else 'no keys, so one row only'})")
        out[key] = row
    return out


def where(row, keys):
    return ", ".join(f"{k}={row.get(k, '')}" for k in keys) or "the single row"


def close(gold, candidate, tolerance):
    if gold == 0:
        return abs(candidate) <= tolerance
    return abs(candidate - gold) <= tolerance * abs(gold)


def grade(gold_text, candidate_text, keys, measures, tolerance):
    """Return (problems, gold row count). Each problem is (kind, text); no problems is a pass."""
    gold = index(read_rows(gold_text, "gold", keys + measures), keys, "gold")
    candidate = index(read_rows(candidate_text, "candidate", keys + measures), keys, "candidate")
    problems = []
    for key, g in gold.items():
        c = candidate.get(key)
        if c is None:
            problems.append(("missing", f"missing row: {where(g, keys)}"))
            continue
        for m in measures:
            gv, cv = g.get(m, ""), c.get(m, "")
            if gv != "" and number(gv) is None:
                raise InputError(f"gold: {m} is not a number at {where(g, keys)}: {gv}")
            if (gv or cv) and (gv == "" or number(cv) is None or not close(number(gv), number(cv), tolerance)):
                problems.append(("mismatch", f"mismatch: {where(g, keys)}, {m}: gold {gv or '(blank)'}, candidate {cv or '(blank)'}"))
    problems += [("extra", f"extra row: {where(c, keys)}") for key, c in candidate.items() if key not in gold]
    return problems, len(gold)


def self_test():
    gold = "region,orders\nA,100\nB,0\n"

    def kinds(candidate, keys=["region"], measures=["orders"], gold_text=gold):
        return [kind for kind, _ in grade(gold_text, candidate, keys, measures, 0.02)[0]]

    assert kinds(gold) == []                                       # identical
    assert kinds("REGION,Orders\nB,0\nA,101\n") == []              # within tolerance, any row order and case
    assert kinds("region,orders\nA,110\nB,0\n") == ["mismatch"]    # outside tolerance
    assert kinds("region,orders\nA,100\n") == ["missing"]          # missing row
    assert kinds(gold + "C,5\n") == ["extra"]                      # extra row
    assert kinds("region,orders\nA,100\nB,0.01\n") == []           # zero gold: absolute tolerance
    assert kinds("region,orders\nA,100\nB,0.5\n") == ["mismatch"]
    assert kinds("total\n42.5\n", keys=[], measures=["total"], gold_text="total\n42\n") == []  # no keys
    for bad in ("region,orders\nA,100\nA,100\n", "region\nA\n"):    # duplicate key, missing column
        try:
            kinds(bad)
            raise AssertionError(f"expected an input error for {bad!r}")
        except InputError:
            pass
    print("self-test ok")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Grade a candidate CSV result against a gold CSV result.")
    parser.add_argument("--gold")
    parser.add_argument("--candidate")
    parser.add_argument("--keys", default="", help="comma-separated; none means a single-row comparison")
    parser.add_argument("--measures", default="", help="comma-separated columns compared numerically")
    parser.add_argument("--tolerance", type=float, default=0.02, help="relative; absolute when the gold value is 0")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    keys = [k.strip().lower() for k in args.keys.split(",") if k.strip()]
    measures = [m.strip().lower() for m in args.measures.split(",") if m.strip()]
    if not args.gold or not args.candidate or not (keys or measures) or args.tolerance < 0:
        parser.error("need --gold, --candidate, at least one key or measure, and a tolerance of 0 or more")
    try:
        texts = []
        for path in (args.gold, args.candidate):
            with open(path, newline="", encoding="utf-8-sig") as fh:
                texts.append(fh.read())
        problems, gold_rows = grade(texts[0], texts[1], keys, measures, args.tolerance)
    except (OSError, UnicodeDecodeError, InputError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 2
    for _, text in problems:
        print(text)
    if not problems:
        print(f"PASS: {gold_rows} row(s), {len(measures)} measure(s) compared")
        return 0
    count = {kind: sum(1 for k, _ in problems if k == kind) for kind in ("mismatch", "missing", "extra")}
    print(f"FAIL: {count['mismatch']} mismatching cell(s), {count['missing']} missing row(s), "
          f"{count['extra']} extra row(s), out of {gold_rows} gold row(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
