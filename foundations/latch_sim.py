# latch_sim.py  —  Phase 2: Latches
#
# A latch is two gates wired in a FEEDBACK LOOP — the output of gate A
# feeds back as an input to gate B, and vice versa. This circular path
# gives the circuit memory: it can hold a value without a clock.
#
# IMPORTANT — why we iterate:
#   In real silicon, signals propagate through gates in nanoseconds.
#   After inputs change, the latch "ripples" through a few gate delays
#   before settling to a stable output. Our simulation models this by
#   re-evaluating both gates in a loop until nothing changes anymore.
#   A single evaluation gets the wrong answer because it uses stale state.
#
# Three latches here:
#   1. SR latch  (NOR-based)   — two NOR gates in a feedback loop
#   2. SR latch  (NAND-based)  — active-low version (used inside D latches)
#   3. D latch                 — adds enable, eliminates the forbidden state
#
# Run:  python latch_sim.py


# ── Primitives ────────────────────────────────────────────────────────────

def nor(a, b):
    return int(not (a or b))

def nand(a, b):
    return int(not (a and b))


# ── 1. NOR SR Latch ───────────────────────────────────────────────────────
#
# Circuit (two NOR gates forming a loop):
#   Q     = NOR(R, Q_bar)
#   Q_bar = NOR(S, Q)
#
# Input table:
#   S=0, R=0  →  HOLD       Q keeps its last value
#   S=1, R=0  →  SET        Q → 1
#   S=0, R=1  →  RESET      Q → 0
#   S=1, R=1  →  FORBIDDEN  forces Q=Q_bar=0  (contradiction: Q_bar should = NOT Q)

class NorSRLatch:
    def __init__(self, q_init=0):
        self.q     = q_init
        self.q_bar = 1 - q_init

    def _settle(self, s, r, max_iters=20):
        for _ in range(max_iters):
            new_q     = nor(r, self.q_bar)
            new_q_bar = nor(s, self.q)
            if new_q == self.q and new_q_bar == self.q_bar:
                return True   # stable
            self.q, self.q_bar = new_q, new_q_bar
        return False  # did not converge (only happens for forbidden)

    def apply(self, s, r):
        self._settle(s, r)
        forbidden = (self.q == self.q_bar)
        return self.q, self.q_bar, forbidden


# ── 2. NAND SR Latch  (active-low inputs) ────────────────────────────────
#
# Circuit:
#   Q     = NAND(S_bar, Q_bar)
#   Q_bar = NAND(R_bar, Q)
#
# "Active-low" means: the input that DOES something is 0, not 1.
#   S_bar=0, R_bar=1  →  SET    Q → 1
#   S_bar=1, R_bar=0  →  RESET  Q → 0
#   S_bar=1, R_bar=1  →  HOLD
#   S_bar=0, R_bar=0  →  FORBIDDEN (Q = Q_bar = 1)

class NandSRLatch:
    def __init__(self, q_init=0):
        self.q     = q_init
        self.q_bar = 1 - q_init

    def _settle(self, s_bar, r_bar, max_iters=20):
        for _ in range(max_iters):
            new_q     = nand(s_bar, self.q_bar)
            new_q_bar = nand(r_bar, self.q)
            if new_q == self.q and new_q_bar == self.q_bar:
                return True
            self.q, self.q_bar = new_q, new_q_bar
        return False

    def apply(self, s_bar, r_bar):
        self._settle(s_bar, r_bar)
        forbidden = (self.q == self.q_bar)
        return self.q, self.q_bar, forbidden


# ── 3. D Latch ────────────────────────────────────────────────────────────
#
# Built from a NAND SR latch + two gating NAND gates at the inputs.
#
# Circuit:
#   S_bar = NAND(D, EN)
#   R_bar = NAND(NOT(D), EN)    where NOT(D) = NAND(D, D)
#   then feed into NAND SR latch
#
# When EN=1:
#   D=1 → S_bar=0, R_bar=1 → SR sees SET   → Q=1
#   D=0 → S_bar=1, R_bar=0 → SR sees RESET → Q=0
#   → Q follows D  ("transparent")
#
# When EN=0:
#   Whatever D is: S_bar=1, R_bar=1 → SR sees HOLD → Q unchanged
#
# The glitch problem with latches:
#   While EN=1, any noise spike on D corrupts Q immediately.
#   Flip-flops (Phase 3) fix this by only sampling on a clock EDGE.

class DLatch:
    def __init__(self, q_init=0):
        self._sr = NandSRLatch(q_init)

    def apply(self, d, en):
        d_bar = nand(d, d)          # NOT(D) from NAND(D,D)
        s_bar = nand(d,    en)
        r_bar = nand(d_bar, en)
        self._sr.apply(s_bar, r_bar)
        return self._sr.q

    @property
    def q(self):
        return self._sr.q


# ── Demo runs ─────────────────────────────────────────────────────────────

def sep(title, width=50):
    pad = width - len(title) - 4
    print(f"\n── {title} {'─' * pad}")


if __name__ == "__main__":
    print("=" * 50)
    print(" Latch Simulation")
    print("=" * 50)

    # 1 ── NOR SR latch
    sep("NOR SR Latch  (start Q=0)")
    print(f"  {'S':>2}  {'R':>2}  │  {'Q':>2}  {'Q_bar':>5}  note")
    print(f"  {'─'*2}  {'─'*2}  ┼  {'─'*2}  {'─'*5}  {'─'*32}")
    latch1 = NorSRLatch(q_init=0)
    steps1 = [
        (0, 0, "HOLD         Q stays 0"),
        (1, 0, "SET       →  Q=1"),
        (0, 0, "HOLD         Q stays 1  ← memory!"),
        (0, 1, "RESET     →  Q=0"),
        (0, 0, "HOLD         Q stays 0"),
        (1, 1, "FORBIDDEN ⚠  Q_bar equals Q"),
    ]
    for s, r, note in steps1:
        q, qb, bad = latch1.apply(s, r)
        warn = "  ← both 0!" if bad else ""
        print(f"  {s:>2}  {r:>2}  │  {q:>2}  {qb:>5}  {note}{warn}")

    # 2 ── NAND SR latch (active-low)
    sep("NAND SR Latch  (active-low, start Q=0)")
    print(f"  {'Sb':>3}  {'Rb':>3}  │  {'Q':>2}  {'Q_bar':>5}  note")
    print(f"  {'─'*3}  {'─'*3}  ┼  {'─'*2}  {'─'*5}  {'─'*32}")
    latch2 = NandSRLatch(q_init=0)
    steps2 = [
        (1, 1, "HOLD         Q stays 0"),
        (0, 1, "SET       →  Q=1  (Sb=0 is active-low)"),
        (1, 1, "HOLD         Q stays 1  ← memory!"),
        (1, 0, "RESET     →  Q=0  (Rb=0 is active-low)"),
        (0, 0, "FORBIDDEN ⚠  Q=Q_bar=1"),
    ]
    for sb, rb, note in steps2:
        q, qb, bad = latch2.apply(sb, rb)
        warn = "  ← both 1!" if bad else ""
        print(f"  {sb:>3}  {rb:>3}  │  {q:>2}  {qb:>5}  {note}{warn}")

    # 3 ── D latch
    sep("D Latch  (start Q=0)")
    print(f"  {'D':>2}  {'EN':>3}  │  {'Q':>2}  note")
    print(f"  {'─'*2}  {'─'*3}  ┼  {'─'*2}  {'─'*40}")
    latch3 = DLatch(q_init=0)
    steps3 = [
        (1, 1, "EN=1, D=1  → Q follows D → Q=1"),
        (0, 1, "EN=1, D=0  → Q follows D → Q=0"),
        (1, 0, "EN=0, D=1  → Q HOLDS     → Q=0  (D ignored)"),
        (0, 0, "EN=0, D=0  → Q HOLDS     → Q=0"),
        (1, 1, "EN=1, D=1  → Q follows D → Q=1"),
        (0, 0, "EN=0, D=0  → Q HOLDS     → Q=1  (D still ignored)"),
    ]
    for d, en, note in steps3:
        q = latch3.apply(d, en)
        print(f"  {d:>2}  {en:>3}  │  {q:>2}  {note}")

    print()
    print("Key takeaway:")
    print("  The latch needs a few gate-delay iterations to settle — that is")
    print("  why we loop until stable. In silicon it happens in nanoseconds.")
    print("  Latches are transparent (D→Q) while EN=1: glitches pass through.")
    print("  Flip-flops (Phase 3) fix this: they only sample on a clock EDGE.")
