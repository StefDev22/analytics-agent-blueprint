#!/usr/bin/env python3
"""Grade a candidate result against a gold result. Standard library only.

  python3 evals/grade.py --gold gold.csv --candidate candidate.csv --keys k1,k2 --measures m1,m2 [--tolerance 0.02]
  python3 evals/grade.py --self-test

Rows align on the key columns; with no keys each file must hold exactly one data row. Measures compare
within a relative tolerance, absolute when the gold value is 0. Column names match case-insensitively;
other columns are ignored. Exit 0 PASS, 1 FAIL, 2 not gradable: a usage error, a file missing or not
readable as CSV, or a gold file with duplicate keys or headers, a missing column, a ragged row, the wrong
row count with no keys, or a measure that is not a finite number. The same shape problems in the
candidate are a FAIL, and so is a blank or non-numeric candidate measure.
"""
import argparse
import contextlib
import csv
import io
import math
import os
import sys
import tempfile


class InputError(Exception):
    pass


def number(cell):
    try:
        return float(cell)
    except ValueError:
        return None


def where(row, keys):
    return ", ".join(f"{k}={row.get(k, '')}" for k in keys) or "the single row"


def load(text, label, keys, measures):
    """Return (rows by key, problems with the file's shape). Rows are dicts keyed by lowercased column name."""
    reader = csv.reader(io.StringIO(text))
    header = [name.strip().lower() for name in next(reader, [])]
    rows = [(reader.line_num, row) for row in reader if any(c.strip() for c in row)]
    problems = [f"{label}: duplicate column: {h}" for h in sorted({h for h in header if header.count(h) > 1})]
    missing = [col for col in keys + measures if col not in header]
    if missing:
        problems.append(f"{label}: missing column(s): {', '.join(missing)}")
    ragged = [line for line, row in rows if len(row) != len(header)]
    if ragged:
        problems.append(f"{label}: {len(ragged)} row(s) not {len(header)} cells wide, first at line {ragged[0]}")
    if not keys and len(rows) != 1:
        problems.append(f"{label}: with no keys the file must hold exactly one data row, not {len(rows)}")
    if problems:
        return {}, problems
    out = {}
    for _, row in rows:
        record = dict(zip(header, (c.strip() for c in row)))
        # A key cell that reads as a number matches as one: 2026 equals 2026.0.
        key = tuple(record[k] if number(record[k]) is None else repr(number(record[k])) for k in keys)
        if key in out:
            problems.append(f"{label}: duplicate key: {where(record, keys)}")
        out[key] = record
    return out, problems


def close(gold, candidate, tolerance):
    if gold == 0:
        return abs(candidate) <= tolerance
    return abs(candidate - gold) <= tolerance * abs(gold)


def grade(gold_text, candidate_text, keys, measures, tolerance):
    """Return (problems, gold row count). Each problem is (kind, text); no problems is a pass.
    A problem in the gold file raises InputError; a problem in the candidate file is a FAIL."""
    gold, problems = load(gold_text, "gold", keys, measures)
    for g in gold.values():
        for m in measures:
            if number(g[m]) is None or not math.isfinite(number(g[m])):
                problems.append(f"gold: {m} is not a finite number at {where(g, keys)}: {g[m] or '(blank)'}")
    if problems:
        raise InputError("; ".join(problems))
    candidate, problems = load(candidate_text, "candidate", keys, measures)
    if problems:
        return [("candidate", p) for p in problems], len(gold)
    for key, g in gold.items():
        c = candidate.get(key)
        if c is None:
            problems.append(("missing", f"missing row: {where(g, keys)}"))
            continue
        for m in measures:
            cv = number(c[m])
            if cv is None or not close(number(g[m]), cv, tolerance):
                problems.append(("mismatch", f"mismatch: {where(g, keys)}, {m}: gold {g[m]}, candidate {c[m] or '(blank)'}"))
    problems += [("extra", f"extra row: {where(c, keys)}") for key, c in candidate.items() if key not in gold]
    return problems, len(gold)


def self_test():
    gold = "region,orders\nA,100\nB,0\n"

    def kinds(candidate, keys=["region"], measures=["orders"], gold_text=gold):
        return [kind for kind, _ in grade(gold_text, candidate, keys, measures, 0.02)[0]]

    def gold_rejected(gold_text, candidate="total\n1\n", keys=[], measures=["total"]):
        try:
            kinds(candidate, keys, measures, gold_text)
        except InputError:
            return True
        return False

    assert kinds(gold) == []                                       # identical
    assert kinds("REGION,Orders\nB,0\nA,101\n") == []              # within tolerance, any row order and case
    assert kinds("region,orders\nA,110\nB,0\n") == ["mismatch"]    # outside tolerance
    assert kinds("region,orders\nA,100\n") == ["missing"]          # missing row
    assert kinds(gold + "C,5\n") == ["extra"]                      # extra row
    assert kinds("region,orders\nA,100\nB,0.01\n") == []           # zero gold: absolute tolerance
    assert kinds("region,orders\nA,100\nB,0.5\n") == ["mismatch"]
    assert kinds("region,orders\nA,100\nB,\n") == ["mismatch"]     # blank candidate measure
    assert kinds("region,orders\nA,n/a\nB,0\n") == ["mismatch"]    # non-numeric candidate measure
    assert kinds("total\n42.5\n", keys=[], measures=["total"], gold_text="total\n42\n") == []  # no keys
    for bad in ("region,orders\nA,100\nA,100\n",          # duplicate key
                "region\nA\n",                            # missing measure column
                "region,orders,Orders\nA,100,1\nB,0,0\n", # duplicate header after normalising
                "region,orders\nA,100\nB\n"):             # row narrower than the header
        assert kinds(bad) == ["candidate"], bad           # in the candidate: a FAIL
        assert gold_rejected(bad, gold, ["region"], ["orders"]), bad  # in the gold: an input error
    for rows in ("total\n", "total\n1\n2\n"):             # no keys: exactly one data row
        assert kinds(rows, keys=[], measures=["total"], gold_text="total\n1\n") == ["candidate"]
    for bad in ("total\n", "total\n1\n2\n", "total,note\n,x\n", "total\nnan\n", "total\ninf\n", "total\nx\n"):
        assert gold_rejected(bad), bad                    # gold: one row, every measure a finite number

    with tempfile.TemporaryDirectory() as tmp:
        def cli(gold_text, candidate_text, *flags):
            """Exit code of the real entry point on two temp files; later flags override the defaults."""
            paths = [os.path.join(tmp, "gold.csv"), os.path.join(tmp, "candidate.csv")]
            for path, text in zip(paths, (gold_text, candidate_text)):
                with open(path, "wb") as fh:
                    fh.write(text if isinstance(text, bytes) else text.encode())
            argv = ["--gold", paths[0], "--candidate", paths[1], "--keys", "region", "--measures", "orders", *flags]
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                try:
                    return main(argv)
                except SystemExit as stop:
                    return stop.code

        assert cli(gold, gold) == 0
        assert cli(gold, "region,orders\nA,110\nB,0\n") == 1
        assert cli(gold, "region,orders\nA,100\nA,100\nB,0\n") == 1                 # candidate duplicate key
        assert cli(gold, "region,orders,ORDERS\nA,100,1\nB,0,0\n") == 1             # candidate duplicate header
        assert cli(gold, "region\nA\nB\n") == 1                                     # candidate missing measure
        assert cli("region,orders\nA,100\nA,100\n", gold) == 2                      # gold duplicate key
        assert cli("region,orders\nA,100\nB\n", gold) == 2                          # gold ragged row
        assert cli("total\n", "total\n", "--keys", "", "--measures", "total") == 2  # header-only gold, no keys
        assert cli("total\n7\n", "total\n", "--keys", "", "--measures", "total") == 1
        for tolerance in ("inf", "nan", "-0.1"):
            assert cli(gold, gold, "--tolerance", tolerance) == 2, tolerance
        assert cli(gold, gold, "--candidate", os.path.join(tmp, "absent.csv")) == 2  # candidate file missing
        assert cli(gold, b"region,orders\n\xff\xfe,1\n") == 2                       # candidate not readable
    print("self-test ok")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Grade a candidate CSV result against a gold CSV result.")
    parser.add_argument("--gold")
    parser.add_argument("--candidate")
    parser.add_argument("--keys", default="", help="comma-separated; none means a single-row comparison")
    parser.add_argument("--measures", default="", help="comma-separated columns compared numerically")
    parser.add_argument("--tolerance", type=float, default=0.02, help="relative; absolute when the gold value is 0")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    keys = [k.strip().lower() for k in args.keys.split(",") if k.strip()]
    measures = [m.strip().lower() for m in args.measures.split(",") if m.strip()]
    if not args.gold or not args.candidate or not (keys or measures) or not 0 <= args.tolerance < math.inf:
        parser.error("need --gold, --candidate, at least one key or measure, and a finite tolerance of 0 or more")
    try:
        texts = []
        for path in (args.gold, args.candidate):
            with open(path, newline="", encoding="utf-8-sig") as fh:
                texts.append(fh.read())
        problems, gold_rows = grade(texts[0], texts[1], keys, measures, args.tolerance)
    except (OSError, UnicodeDecodeError, csv.Error, InputError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 2
    for _, text in problems:
        print(text)
    if not problems:
        print(f"PASS: {gold_rows} row(s), {len(measures)} measure(s) compared")
        return 0
    count = {kind: sum(1 for k, _ in problems if k == kind) for kind in ("candidate", "mismatch", "missing", "extra")}
    if count["candidate"]:
        print(f"FAIL: the candidate file has {count['candidate']} problem(s), so no row was compared")
        return 1
    print(f"FAIL: {count['mismatch']} mismatching cell(s), {count['missing']} missing row(s), "
          f"{count['extra']} extra row(s), out of {gold_rows} gold row(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
