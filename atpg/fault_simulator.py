# fault_simulator.py  —  Phase 7: ATPG & Fault Coverage
#
# This is your atpg-python-tool GitHub repo content.
#
# What this demonstrates:
#   - Stuck-at-0 (SA0) and stuck-at-1 (SA1) fault models
#   - How to detect a fault: drive the node to the opposite value,
#     propagate the difference to a primary output
#   - Fault coverage = (faults detected / total faults) × 100%
#
# Circuit under test (CUT):
#
#   a ──┐
#       ├── AND ─── z1 ──┐
#   b ──┘                ├── OR ─── z_out
#   c ──────────── c ────┘
#
#   z1     = AND(a, b)
#   z_out  = OR(z1, c)
#
# Nodes: a, b, c, z1, z_out  →  10 possible stuck-at faults (SA0 + SA1 each)
#
# Run:  python fault_simulator.py


# ── Fault-free circuit ────────────────────────────────────────────────────

def circuit(a, b, c):
    """Evaluate the circuit with no faults. Returns all node values."""
    z1    = int(a and b)
    z_out = int(z1 or c)
    return {"a": a, "b": b, "c": c, "z1": z1, "z_out": z_out}


# ── Faulty circuit ────────────────────────────────────────────────────────
# A stuck-at fault forces one node to a fixed value.
# Everything downstream sees the stuck value instead of the real one.

def circuit_with_fault(a, b, c, fault_node, fault_val):
    """Evaluate the circuit with one stuck-at fault injected.

    fault_node : which node is stuck  ('a', 'b', 'c', 'z1', 'z_out')
    fault_val  : 0 for SA0, 1 for SA1
    """
    def stuck(name, real_val):
        return fault_val if name == fault_node else real_val

    a_f   = stuck("a", a)
    b_f   = stuck("b", b)
    c_f   = stuck("c", c)
    z1_f  = stuck("z1",   int(a_f and b_f))
    z_out_f = stuck("z_out", int(z1_f or c_f))
    return z_out_f


# ── Fault detection check ─────────────────────────────────────────────────
# A fault is DETECTED by a test pattern if:
#   fault_free_output ≠ faulty_output
# This means the fault caused a visible difference at the primary output.

def is_detected(a, b, c, fault_node, fault_val):
    free = circuit(a, b, c)["z_out"]
    faulty = circuit_with_fault(a, b, c, fault_node, fault_val)
    return free != faulty


# ── Run ATPG over all faults ──────────────────────────────────────────────

def run_fault_simulation():
    nodes      = ["a", "b", "c", "z1", "z_out"]
    fault_vals = [0, 1]

    # All input combinations (2^3 = 8 patterns)
    patterns = [(a, b, c) for a in (0,1) for b in (0,1) for c in (0,1)]

    faults = [(node, val) for node in nodes for val in fault_vals]
    total  = len(faults)

    print("=" * 60)
    print(" Fault Simulation — AND-OR circuit")
    print("=" * 60)
    print()
    print(" Circuit:  z1 = AND(a, b)")
    print("           z_out = OR(z1, c)")
    print()
    print(f" Total nodes       : {len(nodes)}  ({', '.join(nodes)})")
    print(f" Total faults      : {total}  (SA0 + SA1 per node)")
    print(f" Test patterns     : {len(patterns)}  (all {len(patterns)} input combinations)")
    print()

    # For each fault: find which patterns detect it
    detected_faults = []
    undetected = []

    print(f" {'Fault':<16}  {'Detected by pattern':>20}  {'Count':>5}")
    print(f" {'─'*16}  {'─'*20}  {'─'*5}")

    for fault_node, fault_val in faults:
        fault_name = f"{fault_node}-SA{fault_val}"
        detecting  = [p for p in patterns if is_detected(*p, fault_node, fault_val)]

        if detecting:
            detected_faults.append(fault_name)
            # Show first detecting pattern compactly
            p = detecting[0]
            pat_str = f"a={p[0]},b={p[1]},c={p[2]}  (+{len(detecting)-1} more)" if len(detecting)>1 else f"a={p[0]},b={p[1]},c={p[2]}"
            print(f" {fault_name:<16}  {pat_str:>20}  {len(detecting):>5}")
        else:
            undetected.append(fault_name)
            print(f" {fault_name:<16}  {'— untestable —':>20}  {'0':>5}")

    coverage = len(detected_faults) / total * 100

    print()
    print("=" * 60)
    print(f" Results")
    print("=" * 60)
    print(f"  Faults total     : {total}")
    print(f"  Faults detected  : {len(detected_faults)}")
    print(f"  Untestable       : {len(undetected)}")
    print(f"  Fault coverage   : {coverage:.1f}%")
    print()

    if coverage >= 95:
        print(f"  ✓ Coverage {coverage:.1f}% meets industry target (>95%)")
    else:
        print(f"  ✗ Coverage {coverage:.1f}% is below industry target (>95%)")
        print(f"    Untestable faults: {', '.join(undetected)}")

    # Show the minimum set of patterns needed to detect everything
    print()
    print(" Minimum test set (patterns that together detect all faults):")
    covered = set()
    used    = []
    for pat in patterns:
        new = set()
        for fn, fv in faults:
            name = f"{fn}-SA{fv}"
            if name in detected_faults and name not in covered:
                if is_detected(*pat, fn, fv):
                    new.add(name)
        if new:
            covered |= new
            used.append((pat, new))

    for pat, catches in used:
        a,b,c = pat
        print(f"   a={a},b={b},c={c}  →  detects: {', '.join(sorted(catches))}")

    print(f"\n  {len(used)} patterns cover all {len(detected_faults)} detectable faults.")
    print()
    print(" Note: in real chips ATPG tools do this automatically for millions")
    print(" of faults across millions of gates, with compression to reduce")
    print(" test time. This script shows the underlying logic.")


if __name__ == "__main__":
    run_fault_simulation()
