# universal_gates.py  —  Phase 1: NAND & NOR as universal gates
#
# A "universal gate" means: using only that one gate type, you can build
# every other logic gate. NAND and NOR are both universal.
#
# Why this matters for DFT:
#   - SR latches (the building block of flip-flops) ARE just NOR or NAND
#     gates in a feedback loop. You cannot understand latches without this.
#   - Real chip libraries are NAND-heavy — fewer transistors per gate.
#
# Run:  python universal_gates.py


# ── The one primitive ─────────────────────────────────────────────────────

def nand(a, b):
    """NAND: output is 0 only when BOTH inputs are 1. Otherwise 1."""
    return int(not (a and b))

def nor(a, b):
    """NOR: output is 1 only when BOTH inputs are 0. Otherwise 0."""
    return int(not (a or b))


# ── Everything built from NAND only ──────────────────────────────────────
#
# Key insight: NAND(a, a) = NOT(a)
#   When both inputs are the same, NAND becomes NOT.
#   NAND(0,0) = NOT(0 AND 0) = NOT(0) = 1
#   NAND(1,1) = NOT(1 AND 1) = NOT(1) = 0

def not_g(a):
    # 1 NAND gate, both inputs tied together
    return nand(a, a)

def and_g(a, b):
    # AND = NOT(NAND(a,b))  — 2 NAND gates
    # NAND already gives us AND-then-NOT, so invert it
    return not_g(nand(a, b))

def or_g(a, b):
    # OR = NAND(NOT a, NOT b)  — 3 NAND gates
    # De Morgan: NOT(NOT a AND NOT b) = NOT NOT(a OR b) = a OR b
    return nand(not_g(a), not_g(b))

def xor_g(a, b):
    # XOR = NAND(NAND(a, G1), NAND(b, G1))  where G1 = NAND(a,b)  — 4 gates
    # Derivation: XOR(a,b) = (a AND NOT b) OR (NOT a AND b)
    #             Which collapses to the 4-NAND form above.
    g1 = nand(a, b)
    return nand(nand(a, g1), nand(b, g1))


# ── Everything built from NOR only ────────────────────────────────────────
#
# Same idea: NOR(a, a) = NOT(a)

def not_nor(a):
    return nor(a, a)

def or_nor(a, b):
    # OR = NOT(NOR(a,b))  — 2 NOR gates
    return not_nor(nor(a, b))

def and_nor(a, b):
    # AND = NOR(NOT a, NOT b)  — 3 NOR gates (De Morgan, same structure as OR-from-NAND)
    return nor(not_nor(a), not_nor(b))


# ── Truth table helpers ───────────────────────────────────────────────────

def table1(name, fn, ref):
    """Print truth table for a 1-input gate with reference check."""
    print(f"\n  {name}")
    print(f"   A | Y  check")
    print(f"   --+--------")
    ok = True
    for a in (0, 1):
        y = fn(a)
        expected = ref(a)
        mark = "✓" if y == expected else "✗ WRONG"
        if y != expected:
            ok = False
        print(f"   {a} | {y}  {mark}")
    return ok

def table2(name, fn, ref):
    """Print truth table for a 2-input gate with reference check."""
    print(f"\n  {name}")
    print(f"   A  B | Y  check")
    print(f"   -----+--------")
    ok = True
    for a in (0, 1):
        for b in (0, 1):
            y = fn(a, b)
            expected = ref(a, b)
            mark = "✓" if y == expected else "✗ WRONG"
            if y != expected:
                ok = False
            print(f"   {a}  {b} | {y}  {mark}")
    return ok


if __name__ == "__main__":
    print("=" * 44)
    print(" Universal Gates  —  NAND only")
    print("=" * 44)

    results = []
    results.append(table1("NOT  from NAND", not_g,  lambda a:   int(not a)))
    results.append(table2("AND  from NAND", and_g,  lambda a,b: int(a and b)))
    results.append(table2("OR   from NAND", or_g,   lambda a,b: int(a or b)))
    results.append(table2("XOR  from NAND", xor_g,  lambda a,b: int(a ^ b)))

    print("\n" + "=" * 44)
    print(" Universal Gates  —  NOR only")
    print("=" * 44)

    results.append(table1("NOT  from NOR",  not_nor, lambda a:   int(not a)))
    results.append(table2("OR   from NOR",  or_nor,  lambda a,b: int(a or b)))
    results.append(table2("AND  from NOR",  and_nor, lambda a,b: int(a and b)))

    print()
    if all(results):
        print("All implementations correct — every ✓ matches the Python built-in.")
    else:
        print("Something is wrong — check the ✗ rows.")

    print()
    print("Gate count summary (NAND-only path):")
    print("  NOT  = 1 NAND gate")
    print("  AND  = 2 NAND gates")
    print("  OR   = 3 NAND gates")
    print("  XOR  = 4 NAND gates")
    print()
    print("This is why silicon fabs love NAND — every function maps to it.")
