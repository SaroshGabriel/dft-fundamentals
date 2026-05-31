# flip_flop.py  —  Phase 3: Flip-Flops
#
# Flip-flops fix the latch glitch problem: instead of "transparent while
# enabled", they only capture data on a clock EDGE (the instant CLK goes
# from 0→1). Between edges, Q is frozen regardless of what D does.
#
# This file covers:
#   1. D flip-flop  — the workhorse of digital design (already here)
#   2. JK flip-flop — like SR latch but no forbidden state; J=K=1 toggles
#
# What a D flip-flop does:
#   - It has one data input D, one clock input CLK, and one output Q.
#   - When CLK goes from 0 -> 1 (a "rising edge"), it copies D into Q.
#   - At all other times, Q does not change. Q "remembers".
#
# We model one tick of time at a time. To detect a rising edge we
# need to remember what CLK was on the previous tick.


# These two variables are the "state" of the flip-flop.
# In Python, module-level variables are fine for now -- think of them
# as the FF's "memory cells".
q_state = 0            # current Q output
prev_clk = 0           # what CLK was on the previous tick


def flip_flop_tick(d, clk):
    """Advance the FF by one tick of time.

    d   = the value on the D input right now (0 or 1)
    clk = the value on the CLK input right now (0 or 1)

    Returns the new Q.
    """
    global q_state, prev_clk

    # A rising edge happens when CLK *was* 0 last tick and *is* 1 this tick.
    rising_edge = (prev_clk == 0) and (clk == 1)

    if rising_edge:
        q_state = d        # capture D into Q
    # else: do nothing -- Q holds its old value. That's the "memory".

    prev_clk = clk             # remember CLK for the next call
    return q_state


# --- demo --------------------------------------------------------------
# We feed in a sequence of (D, CLK) values that look like this:
#
#   tick:    0  1  2  3  4  5  6  7  8
#   D:       1  1  0  0  1  1  1  0  0
#   CLK:     0  1  1  0  0  1  0  1  1
#                ^         ^     ^
#                rising    rising rising
#
# Q should change only on the marked rising edges.

# ── JK Flip-Flop ─────────────────────────────────────────────────────────
#
# JK is like an SR latch but the forbidden state is replaced with TOGGLE:
#   J=0, K=0  →  HOLD    (Q unchanged)
#   J=1, K=0  →  SET     (Q → 1)
#   J=0, K=1  →  RESET   (Q → 0)
#   J=1, K=1  →  TOGGLE  (Q flips to opposite)
#
# Still edge-triggered: only acts on rising CLK edge.

jk_q     = 0    # separate state from D-FF above
jk_prev  = 0


def jk_ff_tick(j, k, clk):
    global jk_q, jk_prev
    rising_edge = (jk_prev == 0) and (clk == 1)
    if rising_edge:
        if   j == 0 and k == 0:  pass              # hold
        elif j == 1 and k == 0:  jk_q = 1          # set
        elif j == 0 and k == 1:  jk_q = 0          # reset
        else:                    jk_q = 1 - jk_q   # toggle  (j=1, k=1)
    jk_prev = clk
    return jk_q


if __name__ == "__main__":
    # ── D flip-flop demo ──────────────────────────────────────────────────
    print("D Flip-Flop")
    print(f"{'tick':>4} {'D':>2} {'CLK':>3} {'edge?':>6} {'Q':>2}")
    waveform = [
        (1, 0),
        (1, 1),   # rising edge → Q=1
        (0, 1),
        (0, 0),
        (1, 0),
        (1, 1),   # rising edge → Q stays 1
        (1, 0),
        (0, 1),   # rising edge → Q=0
        (0, 1),
    ]
    for tick, (d, clk) in enumerate(waveform):
        edge = (prev_clk == 0) and (clk == 1)
        q = flip_flop_tick(d, clk)
        print(f"{tick:>4} {d:>2} {clk:>3} {str(edge):>6} {q:>2}")

    # ── JK flip-flop demo ─────────────────────────────────────────────────
    print()
    print("JK Flip-Flop  (J=K=1 → toggle on every rising edge)")
    print(f"{'tick':>4} {'J':>2} {'K':>2} {'CLK':>3} {'edge?':>6} {'Q':>2}  note")
    jk_waveform = [
        # (J, K, CLK)
        (0, 0, 0),
        (1, 0, 1),  # rising, J=1 K=0 → SET   → Q=1
        (1, 0, 0),
        (0, 1, 1),  # rising, J=0 K=1 → RESET → Q=0
        (0, 1, 0),
        (1, 1, 1),  # rising, J=1 K=1 → TOGGLE → Q=1
        (1, 1, 0),
        (1, 1, 1),  # rising, J=1 K=1 → TOGGLE → Q=0
        (1, 1, 0),
        (1, 1, 1),  # rising, J=1 K=1 → TOGGLE → Q=1
    ]
    notes = ["","SET","","RESET","","TOGGLE","","TOGGLE","","TOGGLE"]
    for tick, ((j, k, clk), note) in enumerate(zip(jk_waveform, notes)):
        edge = (jk_prev == 0) and (clk == 1)
        q = jk_ff_tick(j, k, clk)
        print(f"{tick:>4} {j:>2} {k:>2} {clk:>3} {str(edge):>6} {q:>2}  {note}")
