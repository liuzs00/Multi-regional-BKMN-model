"""
Mutation test: inject a plausible bug, see whether the gate suites catch it.

A validation suite is only worth what it rejects.  This deliberately breaks the
model in ways a real implementation could plausibly be wrong -- a flipped sign,
a transposed matrix, a mean reversion with the wrong sign -- then runs every
gate.  A mutant that SURVIVES is a hole in the suite, not a bug in the model.
See docs/CHAPTER_VALIDATION.md §7.

Two of these have already earned their place: the spot sign flip and
`forward = spot - points` both survived an earlier version of the suite, because
symmetry testing is blind to a sign convention applied consistently.  Group F of
tests/test_validation.py exists because of them.

SAFETY.  This edits files under bkmn/ in place, so a run that dies between the
write and the restore leaves the model silently wrong -- a transposed technical
matrix corrupts every number in the project without raising anything.  An
interrupted run did exactly that.  So:

  * each source is copied to `<file>.mutation-backup` BEFORE it is touched
  * a leftover backup found at startup means the previous run died; it is
    restored and reported, and nothing else happens until the tree is clean
  * every file is verified byte-identical to its backup at the end

Usage: py -3 tools/mutation_test.py     (exit 1 if any mutant survives)
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FX = os.path.join(ROOT, "bkmn", "fx.py")
RATES = os.path.join(ROOT, "bkmn", "rates.py")
TR = os.path.join(ROOT, "bkmn", "transition.py")
SUFFIX = ".mutation-backup"

MUTANTS = [
    ("spot sign flipped", FX,
     "return cum_infl_region - cum_infl_base",
     "return cum_infl_base - cum_infl_region"),
    ("forward-points sign flipped", FX,
     "return float(hw_B(tau, a)) * (dr_region - dr_base)",
     "return float(hw_B(tau, a)) * (dr_base - dr_region)"),
    ("forward = spot MINUS points", FX,
     "return (spot_ppp(cum_infl_region, cum_infl_base)\n            + forward_points(dr_region, dr_base, tau, a))",
     "return (spot_ppp(cum_infl_region, cum_infl_base)\n            - forward_points(dr_region, dr_base, tau, a))"),
    ("Hull-White B uses +a not -a", RATES,
     "(1.0 - np.exp(-a * tau)) / a",
     "(1.0 - np.exp(a * tau)) / a"),
    ("technical matrix transposed", TR,
     "return m.Z / np.where(m.x == 0, 1.0, m.x)[None, :]",
     "return (m.Z / np.where(m.x == 0, 1.0, m.x)[None, :]).T"),
    ("A normalised by row not column", TR,
     "return m.Z / np.where(m.x == 0, 1.0, m.x)[None, :]",
     "return m.Z / np.where(m.x == 0, 1.0, m.x)[:, None]"),
    ("charge uses + instead of - in Eq 10", TR,
     "return (I - AT) @ Ltil - I + phi * I",
     "return (I - AT) @ Ltil + I + phi * I"),
]

SUITES = ["test_fx.py", "test_extensions.py", "test_validation.py"]
TOUCHED = sorted({path for _, path, _, _ in MUTANTS})


def read(p):
    """Raw bytes: backup and restore must be byte-exact.

    Reading as text and writing it back rewrites CRLF as LF on this repo, which
    leaves every touched file showing as modified in git after a clean run --
    a restore that changes the file is not a restore.
    """
    with open(p, "rb") as f:
        return f.read()


def write(p, b):
    with open(p, "wb") as f:
        f.write(b)


def mutate(raw, old, new):
    """Apply a mutation to raw bytes, preserving the file's line endings.

    The patterns are written with "\\n" because that is how the source reads;
    the file on disk may use "\\r\\n".  Normalise, substitute, restore.
    """
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8").replace("\r\n", "\n")
    if old not in text:
        return None
    text = text.replace(old, new, 1)
    if crlf:
        text = text.replace("\n", "\r\n")
    return text.encode("utf-8")


def recover():
    """Restore anything a previous run left mutated, before doing anything else."""
    found = []
    for path in TOUCHED:
        bak = path + SUFFIX
        if os.path.exists(bak):
            write(path, read(bak))
            os.remove(bak)
            found.append(os.path.relpath(path, ROOT))
    if found:
        print(f"recovered {len(found)} file(s) left mutated by an interrupted "
              f"run: {', '.join(found)}\n")
    return found


def run(suite):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tests", suite)],
                       capture_output=True, text=True, cwd=ROOT,
                       encoding="utf-8", errors="replace")
    return p.returncode == 0


def main():
    recover()
    for path in TOUCHED:                       # snapshot before touching anything
        write(path + SUFFIX, read(path))

    survivors, skipped = [], []
    try:
        print(f"{'mutant':<38}{'fx':>6}{'ext':>6}{'valid':>7}   verdict")
        for name, path, old, new in MUTANTS:
            src = read(path + SUFFIX)          # always mutate the pristine bytes
            bad = mutate(src, old, new)
            if bad is None:
                print(f"{name:<38}  -- pattern not found, skipped")
                skipped.append(name)
                continue
            try:
                write(path, bad)
                res = {s: run(s) for s in SUITES}
            finally:
                write(path, src)
            caught = not all(res.values())
            marks = "".join(f"{'ok' if res[s] else 'FAIL':>6}" for s in SUITES)
            print(f"{name:<38}{marks}   "
                  f"{'caught' if caught else '*** SURVIVES ***'}")
            if not caught:
                survivors.append(name)
    finally:
        dirty = []
        for path in TOUCHED:
            bak = path + SUFFIX
            if read(path) != read(bak):
                write(path, read(bak))
                dirty.append(os.path.relpath(path, ROOT))
            os.remove(bak)
        if dirty:
            print(f"\nrestored {', '.join(dirty)} on the way out")

    print()
    if skipped:
        print(f"{len(skipped)} mutant(s) skipped -- the code they target has "
              f"changed shape, so they test nothing:")
        for s in skipped:
            print(f"   - {s}")
    if survivors:
        print(f"{len(survivors)} mutant(s) survive -- the suite cannot detect:")
        for s in survivors:
            print(f"   - {s}")
    else:
        print("every mutant caught")
    return 1 if (survivors or skipped) else 0


if __name__ == "__main__":
    sys.exit(main())
