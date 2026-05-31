# boolean_simplify.py  —  Phase 01: Boolean Algebra & K-Maps
#
# What this covers:
#   1. Evaluate any Boolean function defined by its truth table
#   2. Generate the canonical SOP (Sum of Products) expression
#   3. Verify De Morgan's theorem for all input combinations
#   4. Display K-maps for 2, 3, and 4 variable functions
#      (K-maps use Gray code column order so adjacent cells differ by 1 bit)
#
# How to use:
#   - Read the output section by section
#   - For each K-map: circle the groups of 1s yourself on paper
#   - Larger groups → simpler final expression
#
# Run:  python boolean_simplify.py


# ── Variable naming ───────────────────────────────────────────────────────

def var_names(n):
    return list('ABCDEFGH'[:n])


# ── Minterm → product term string ─────────────────────────────────────────
#
# A minterm is one row of the truth table where F=1.
# It maps to a product (AND) of all variables — complemented if 0, plain if 1.
#   minterm 5  =  binary 101  (n=3)
#   → A=1, B=0, C=1  →  "AB'C"

def minterm_str(idx, n):
    names = var_names(n)
    bits  = [(idx >> (n - 1 - i)) & 1 for i in range(n)]
    return ''.join(f"{names[i]}'" if bits[i] == 0 else names[i]
                   for i in range(n))


# ── Canonical SOP expression ──────────────────────────────────────────────
#
# SOP = Sum of Products = OR of all minterms where F=1.
# This is the "raw" unoptimized expression before K-map simplification.

def canonical_sop(ones, n):
    if not ones:
        return "F = 0  (always false)"
    if len(ones) == 2**n:
        return "F = 1  (always true)"
    terms = [minterm_str(i, n) for i in sorted(ones)]
    return "F = " + " + ".join(terms)


# ── Truth table display ───────────────────────────────────────────────────

def print_truth_table(name, n, truth_table):
    names  = var_names(n)
    header = "  " + "  ".join(names) + "  │  F"
    sep    = "  " + "──" * n + "──┼───"
    print(f"\n  {name}  —  truth table")
    print(header)
    print(sep)
    ones = []
    for i, val in enumerate(truth_table):
        bits = [(i >> (n - 1 - k)) & 1 for k in range(n)]
        row  = "  " + "  ".join(str(b) for b in bits)
        mark = "  ← minterm " + str(i) if val else ""
        print(f"{row}  │  {val}{mark}")
        if val:
            ones.append(i)
    return ones


# ── De Morgan's theorem verification ─────────────────────────────────────
#
# De Morgan #1:  (A AND B)' = A' OR B'
# De Morgan #2:  (A OR B)'  = A' AND B'
#
# "Break the bar, change the operation" — this is how NAND and NOR connect.

def verify_demorgan():
    print("\n" + "=" * 56)
    print(" De Morgan's Theorem — verified by truth table")
    print("=" * 56)

    print("\n  Theorem 1:  (A · B)' = A' + B'")
    print("  In hardware: a NAND gate = two NOTs feeding into an OR gate")
    print()
    print(f"  {'A':>2}  {'B':>2}  │  {'(AB)\'':>6}  {'A\'+B\'':>6}  {'match':>6}")
    print(f"  {'─'*2}  {'─'*2}  ┼  {'─'*6}  {'─'*6}  {'─'*6}")
    for a in (0, 1):
        for b in (0, 1):
            lhs = int(not (a and b))          # (A AND B)'
            rhs = int((not a) or (not b))     # A' OR B'
            ok  = "✓" if lhs == rhs else "✗ WRONG"
            print(f"  {a:>2}  {b:>2}  │  {lhs:>6}  {rhs:>6}  {ok:>6}")

    print()
    print(f"  Theorem 2:  (A + B)' = A' · B'")
    print("  In hardware: a NOR gate = two NOTs feeding into an AND gate")
    print()
    print(f"  {'A':>2}  {'B':>2}  │  {'(A+B)\'':>6}  {'A\'·B\'':>6}  {'match':>6}")
    print(f"  {'─'*2}  {'─'*2}  ┼  {'─'*6}  {'─'*6}  {'─'*6}")
    for a in (0, 1):
        for b in (0, 1):
            lhs = int(not (a or b))           # (A OR B)'
            rhs = int((not a) and (not b))    # A' AND B'
            ok  = "✓" if lhs == rhs else "✗ WRONG"
            print(f"  {a:>2}  {b:>2}  │  {lhs:>6}  {rhs:>6}  {ok:>6}")

    print()
    print("  Key insight: this is WHY OR-from-NAND works (Phase 02).")
    print("  NAND(A,B) = (AB)' = A'+B' = OR(NOT A, NOT B)")


# ── K-map: 2 variables ────────────────────────────────────────────────────
#
# Layout (standard, no Gray code needed for 2 vars — all cells adjacent):
#
#       B=0   B=1
# A=0  │ m0  │ m1  │
# A=1  │ m2  │ m3  │
#
# Adjacent cells: every cell is adjacent to its row/column neighbors.
# Wrapping: left↔right and top↔bottom also count as adjacent.

def kmap_2var(name, truth_table):
    print(f"\n  {name}  —  K-map (2 variables: A, B)")
    print()
    print("         B=0    B=1")
    print("       ┌──────┬──────┐")
    for a in (0, 1):
        cells = []
        for b in (0, 1):
            idx = 2 * a + b
            v   = truth_table[idx]
            cells.append(f" m{idx}:{v} ")
        print(f"  A={a}  │{'│'.join(cells)}│")
        if a == 0:
            print("       ├──────┼──────┤")
    print("       └──────┴──────┘")
    print()
    print("  Adjacency: every cell is adjacent to all 3 neighbours")
    print("  (top↔bottom and left↔right both wrap around)")


# ── K-map: 3 variables ────────────────────────────────────────────────────
#
# Layout (row = A, columns = BC in GRAY CODE order: 00, 01, 11, 10):
#
#        BC=00  BC=01  BC=11  BC=10
# A=0   │  m0  │  m1  │  m3  │  m2  │
# A=1   │  m4  │  m5  │  m7  │  m6  │
#
# WHY Gray code? Adjacent columns differ by exactly 1 bit.
# 00→01: C flips. 01→11: B flips. 11→10: C flips. 10→00 (wrap): B flips.
# This guarantees that a rectangle of cells always represents a valid group.

GRAY3_BC = [0b00, 0b01, 0b11, 0b10]   # BC column order (Gray code)

def kmap_3var(name, truth_table):
    print(f"\n  {name}  —  K-map (3 variables: A, B, C)")
    print()
    print("           BC=00  BC=01  BC=11  BC=10")
    print("         ┌──────┬──────┬──────┬──────┐")
    for a in (0, 1):
        cells = []
        for bc in GRAY3_BC:
            b   = (bc >> 1) & 1
            c   = bc & 1
            idx = 4 * a + 2 * b + c
            v   = truth_table[idx]
            cells.append(f" m{idx}:{v}")
        row = "│".join(f"{c:<6}" for c in cells)
        print(f"  A={a}   │{row}│")
        if a == 0:
            print("         ├──────┼──────┼──────┼──────┤")
    print("         └──────┴──────┴──────┴──────┘")
    print()
    print("  Wrap-around adjacency:")
    print("  • BC=00 col and BC=10 col are adjacent (left edge ↔ right edge)")
    print("  • A=0 row and A=1 row are adjacent (top ↔ bottom)")


# ── K-map: 4 variables ────────────────────────────────────────────────────
#
# Layout (rows = AB in Gray code, cols = CD in Gray code):
#
#           CD=00  CD=01  CD=11  CD=10
# AB=00   │  m0  │  m1  │  m3  │  m2  │
# AB=01   │  m4  │  m5  │  m7  │  m6  │
# AB=11   │ m12  │ m13  │ m15  │ m14  │
# AB=10   │  m8  │  m9  │ m11  │ m10  │

GRAY4 = [0b00, 0b01, 0b11, 0b10]

def kmap_4var(name, truth_table):
    print(f"\n  {name}  —  K-map (4 variables: A, B, C, D)")
    print()
    ab_labels = ["AB=00", "AB=01", "AB=11", "AB=10"]
    print("              CD=00  CD=01  CD=11  CD=10")
    print("            ┌──────┬──────┬──────┬──────┐")
    for row_i, ab in enumerate(GRAY4):
        a = (ab >> 1) & 1
        b =  ab       & 1
        cells = []
        for cd in GRAY4:
            c   = (cd >> 1) & 1
            d   =  cd       & 1
            idx = 8 * a + 4 * b + 2 * c + d
            v   = truth_table[idx]
            cells.append(f" m{idx:02d}:{v}")
        row = "│".join(f"{c:<6}" for c in cells)
        print(f"  {ab_labels[row_i]}   │{row}│")
        if row_i < 3:
            print("            ├──────┼──────┼──────┼──────┤")
    print("            └──────┴──────┴──────┴──────┘")
    print()
    print("  Wrap-around: top row (AB=00) adjacent to bottom row (AB=10).")
    print("  Left col (CD=00) adjacent to right col (CD=10).")


# ── Full analysis ─────────────────────────────────────────────────────────

def analyze(name, truth_table):
    n    = {2: 1, 4: 2, 8: 3, 16: 4}[len(truth_table)]
    ones = print_truth_table(name, n, truth_table)
    print()
    print(f"  Minterms (where F=1): {ones}")
    print(f"  Canonical SOP       : {canonical_sop(ones, n)}")
    print()
    if n == 2: kmap_2var(name, truth_table)
    if n == 3: kmap_3var(name, truth_table)
    if n == 4: kmap_4var(name, truth_table)


# ── Demo ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 56)
    print(" Boolean Algebra & K-Maps")
    print("=" * 56)

    # ── Example 1: XOR(A,B) — 2 variables ────────────────────────────────
    # F = A'B + AB' — no simplification possible (already minimal)
    print("\n" + "─" * 56)
    print(" Example 1: XOR  (F = A'B + AB')")
    print("─" * 56)
    xor_table = [0, 1, 1, 0]   # indexed: 00→0, 01→1, 10→1, 11→0
    analyze("XOR(A,B)", xor_table)
    print("  K-map hint: the two 1-cells (m1 and m2) are NOT adjacent")
    print("  (they differ in BOTH A and B). Cannot group them.")
    print("  → F = A'B + AB' — this is already the minimum SOP.")

    # ── Example 2: F = A'B + AB' + AB — 2 variables ──────────────────────
    # Three minterms: should simplify to F = A + B  (just an OR gate)
    print("\n" + "─" * 56)
    print(" Example 2: F = A'B + AB' + AB")
    print("─" * 56)
    f2_table = [0, 1, 1, 1]    # m0=0, m1=1, m2=1, m3=1
    analyze("F2(A,B)", f2_table)
    print("  K-map hint: three 1-cells — m1,m2,m3 are all 1.")
    print("  Group m1+m3 (same column B=1) → term = B")
    print("  Group m2+m3 (same row A=1)    → term = A")
    print("  → F = A + B  (just an OR gate!)")
    print()
    print("  Verify algebraically:")
    print("  A'B + AB' + AB")
    print("  = A'B + AB' + AB + AB    (idempotent: AB = AB + AB)")
    print("  = (A'B + AB) + (AB' + AB)")
    print("  = B(A'+A) + A(B'+B)")
    print("  = B·1    + A·1")
    print("  = A + B  ✓")

    # ── Example 3: 3-variable, simplifies to C' ───────────────────────────
    # F = A'B'C' + A'BC' + AB'C' + ABC'   (all combos where C=0)
    print("\n" + "─" * 56)
    print(" Example 3: F = A'B'C' + A'BC' + AB'C' + ABC'")
    print("─" * 56)
    f3_table = [1, 0, 1, 0, 1, 0, 1, 0]
    #           m0  m1  m2  m3  m4  m5  m6  m7
    analyze("F3(A,B,C)", f3_table)
    print("  K-map hint: the four 1-cells are m0,m2,m4,m6 — all in")
    print("  columns BC=00 and BC=10. These 4 cells form one big group.")
    print("  Both A and B change within the group → both eliminated.")
    print("  Only C is constant (C=0 in all cells).")
    print("  → F = C'  (just a NOT gate on C!)")
    print()
    print("  This is the power of K-maps: what looks like 4 terms")
    print("  collapses to a single literal.")

    # ── Example 4: 4-variable K-map ──────────────────────────────────────
    print("\n" + "─" * 56)
    print(" Example 4: F = 1 when (A=0 AND D=0), 4-variable")
    print("─" * 56)
    # F = A'D' — true when A=0 and D=0 regardless of B and C
    f4_table = [
        1, 0, 1, 0,   # AB=00: m0,m1,m2,m3  (D alternates: 0,1,0,1 via CD gray code 00,01,11,10)
        1, 0, 1, 0,   # AB=01: m4,m5,m6,m7
        0, 0, 0, 0,   # AB=11: m12-m15
        0, 0, 0, 0,   # AB=10: m8-m11
    ]
    # Actually let me construct this properly
    # F = A'D' means A=0 and D=0
    f4_table = []
    for i in range(16):
        a = (i >> 3) & 1
        b = (i >> 2) & 1
        c = (i >> 1) & 1
        d =  i       & 1
        f4_table.append(int(a == 0 and d == 0))
    analyze("F4(A,B,C,D) = A'D'", f4_table)
    print("  K-map hint: the 1-cells form a 4-cell group in the AB=00")
    print("  and AB=01 rows, CD=00 and CD=10 columns.")
    print("  B and C vary → eliminated. A=0 constant → A'.")
    print("  In CD cols: CD=00 and CD=10 both have D=0 → D' constant.")
    print("  → F = A'D' ✓  (confirmed by K-map)")

    # ── De Morgan's theorem ───────────────────────────────────────────────
    verify_demorgan()

    print()
    print("=" * 56)
    print(" Summary: what to take away")
    print("=" * 56)
    print()
    print("  1. K-maps work because Gray code makes adjacency = 1-bit change.")
    print("     A rectangle of 2^k ones = one simplified product term.")
    print("     Variables that change within the group are ELIMINATED.")
    print()
    print("  2. De Morgan is not magic — it is a truth table fact.")
    print("     NAND(A,B) = NOT(A AND B) = NOT(A) OR NOT(B)")
    print("     NOR(A,B)  = NOT(A OR B)  = NOT(A) AND NOT(B)")
    print("     This is why OR-from-NAND (Phase 02) works.")
    print()
    print("  3. Canonical SOP is always correct but never minimal.")
    print("     K-map grouping finds the minimal expression.")
    print("     Bigger groups = fewer literals = simpler circuit.")
