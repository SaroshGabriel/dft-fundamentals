# fsm.py  —  Phase 4: Finite State Machines
#
# A state machine has "memory" — its output depends not just on the current
# input but on what STATE it is currently in. States are stored in FFs.
#
# Two FSMs here:
#   1. Moore FSM  — output depends only on current state  (output inside circle)
#   2. Sequence detector — a practical Mealy-style FSM
#
# MOORE FSM EXAMPLE: Traffic Light Controller
#   3 states: RED → GREEN → YELLOW → RED → ...
#   Each state lasts one "tick" (in real life: timers, but we simplify)
#   Output = which light is ON (just the state name)
#
# WHY this matters for DFT:
#   The JTAG TAP controller (Phase 8) is a 16-state Moore FSM.
#   If you understand traffic lights, you understand TAP.
#
# Run:  python fsm.py


# ── Traffic Light Moore FSM ───────────────────────────────────────────────
#
# State diagram (Moore — output is the state itself):
#
#   ┌──────┐  tick   ┌───────┐  tick   ┌────────┐
#   │  RED │ ──────► │ GREEN │ ──────► │ YELLOW │
#   └──────┘         └───────┘         └────────┘
#      ▲                                    │
#      └────────────────────────────────────┘ tick
#
# In real chips the "tick" would come from a timer — here it's just a
# function call to step().

TRAFFIC_TRANSITIONS = {
    "RED":    "GREEN",
    "GREEN":  "YELLOW",
    "YELLOW": "RED",
}

class TrafficLightFSM:
    def __init__(self):
        self.state = "RED"          # start state

    def step(self):
        """Advance by one tick. Returns (previous_state, new_state)."""
        old = self.state
        self.state = TRAFFIC_TRANSITIONS[self.state]
        return old, self.state

    def output(self):
        """Moore: output = current state (the active light)."""
        return self.state


# ── Sequence Detector FSM ─────────────────────────────────────────────────
#
# Detects the pattern "101" in a serial bitstream.
# Outputs 1 (detected!) when the last 3 bits seen were 1,0,1.
#
# State diagram (Moore — output is 1 in state DETECTED, else 0):
#
#   IDLE ──1──► S1 ──0──► S10 ──1──► DETECTED ──► back to S1
#     │          │                                  (overlap: end 1 is new start)
#     └──0──────►IDLE◄──0──────────────────────────►
#
# States:
#   IDLE     : no useful prefix seen
#   S1       : last bit was 1
#   S10      : last two bits were 1,0
#   DETECTED : last three bits were 1,0,1  → output = 1

SEQ_TRANSITIONS = {
    #  state      input   next_state
    ("IDLE",      0):  "IDLE",
    ("IDLE",      1):  "S1",
    ("S1",        0):  "S10",
    ("S1",        1):  "S1",       # another 1 — still have a valid start
    ("S10",       0):  "IDLE",
    ("S10",       1):  "DETECTED",
    ("DETECTED",  0):  "S10",      # the last 1 of "101" is new start of "10..."
    ("DETECTED",  1):  "S1",
}

class SequenceDetector101:
    def __init__(self):
        self.state = "IDLE"

    def feed(self, bit):
        """Feed one bit. Returns 1 if '101' just completed, else 0."""
        self.state = SEQ_TRANSITIONS[(self.state, bit)]
        return 1 if self.state == "DETECTED" else 0


# ── Demos ─────────────────────────────────────────────────────────────────

def sep(title):
    print(f"\n── {title} {'─'*(48-len(title))}")


if __name__ == "__main__":
    print("=" * 52)
    print(" Finite State Machine Simulation")
    print("=" * 52)

    # 1 ── Traffic light: 9 ticks
    sep("Traffic Light Moore FSM  (9 ticks)")
    print(f"  {'tick':>4}  {'state':>7}  output (which light is ON)")
    print(f"  {'─'*4}  {'─'*7}  {'─'*26}")

    tl = TrafficLightFSM()
    print(f"  {'0':>4}  {tl.output():>7}  {tl.output()} ← initial state")
    for tick in range(1, 10):
        old, new = tl.step()
        arrow = f"{old} → {new}"
        print(f"  {tick:>4}  {new:>7}  {tl.output()}")

    # 2 ── Sequence detector
    sep("Sequence Detector  (pattern: '101')")
    bitstream = [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1]
    print(f"  Bitstream: {bitstream}")
    print()
    print(f"  {'i':>2}  {'bit':>3}  {'state':>8}  {'detect':>6}")
    print(f"  {'─'*2}  {'─'*3}  {'─'*8}  {'─'*6}")

    det = SequenceDetector101()
    for i, bit in enumerate(bitstream):
        found = det.feed(bit)
        flag = "  ← DETECTED" if found else ""
        print(f"  {i:>2}  {'→'+str(bit):>3}  {det.state:>8}  {found:>6}{flag}")

    print()
    print("Key takeaway:")
    print("  Moore FSM: output depends ONLY on state — stable, glitch-free.")
    print("  The TAP controller in JTAG (Phase 8) follows the same pattern:")
    print("  16 states, TMS input drives transitions, TCK clocks each step.")
