# step1_truth_tables.py
#
# DFT ladder, Step 1: see what each gate actually does.
#
# A "gate" is just a tiny function that takes 1 or 2 input bits and
# returns 1 output bit. That's it. Nothing magic.
#
# We will define each gate as a plain Python function, then print
# its truth table -- every possible input combination and the output.
#
# The truth table IS the gate. If you can read the table, you know
# the gate. Forget Boolean algebra and K-maps for now.
#
# Run it:    python step1_truth_tables.py


# -----------------------------------------------------------------
# The five gates we care about for latches & flip-flops.
# Each function takes bits (0 or 1) and returns a bit (0 or 1).
# -----------------------------------------------------------------

def NOT(a):
    # NOT flips the bit.   0 -> 1,   1 -> 0
    if a == 0:
        return 1
    else:
        return 0


def AND(a, b):
    # AND is 1 only when BOTH inputs are 1.
    if a == 1 and b == 1:
        return 1
    else:
        return 0


def OR(a, b):
    # OR is 1 when AT LEAST ONE input is 1.
    if a == 1 or b == 1:
        return 1
    else:
        return 0


def NAND(a, b):
    # NAND = NOT AND.  It's AND, then flip.
    # NAND is 0 only when BOTH inputs are 1. Otherwise 1.
    return NOT(AND(a, b))


def NOR(a, b):
    # NOR = NOT OR.  It's OR, then flip.
    # NOR is 1 only when BOTH inputs are 0. Otherwise 0.
    return NOT(OR(a, b))


# -----------------------------------------------------------------
# Truth-table printers.
# -----------------------------------------------------------------

def print_table_1input(name, gate_function):
    """Print the truth table for a 1-input gate (just NOT)."""
    print(f"\n{name} truth table")
    print(" A | Y")
    print("---+---")
    for a in (0, 1):
        y = gate_function(a)
        print(f" {a} | {y}")


def print_table_2input(name, gate_function):
    """Print the truth table for a 2-input gate."""
    print(f"\n{name} truth table")
    print(" A B | Y")
    print("-----+---")
    for a in (0, 1):
        for b in (0, 1):
            y = gate_function(a, b)
            print(f" {a} {b} | {y}")


# -----------------------------------------------------------------
# Run all of them.
# -----------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 30)
    print(" Step 1: basic gate truth tables")
    print("=" * 30)

    print_table_1input("NOT",  NOT)
    print_table_2input("AND",  AND)
    print_table_2input("OR",   OR)
    print_table_2input("NAND", NAND)
    print_table_2input("NOR",  NOR)

    # A couple of patterns to notice (stare at the output above):
    #
    # 1. NAND is the EXACT OPPOSITE of AND, row by row.
    # 2. NOR  is the EXACT OPPOSITE of OR,  row by row.
    # 3. NAND with both inputs tied together acts like NOT:
    #       NAND(0,0) = 1     same as NOT(0)
    #       NAND(1,1) = 0     same as NOT(1)
    #    -> we'll use this fact in Step 2.

    print("\nNotice: NAND(a, a) == NOT(a):")
    for a in (0, 1):
        print(f"  NAND({a}, {a}) = {NAND(a, a)}    NOT({a}) = {NOT(a)}")
