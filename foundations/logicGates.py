def logic_gate(a, b, op):
    if op == "and":
        result = a and b
    elif op == "or":
        result = a or b
    elif op == "nand":
        result = not (a and b)
    elif op == "nor":
        result = not (a or b)
    elif op == "xor":
        result = a ^ b
    elif op == "xnor":
        result = not (a ^ b)
    else:
        return "Unknown operation!"
    
    return int(result)

while True:
    a = int(input("Choose value of a (0/1): "))
    b = int(input("Choose value of b (0/1): "))
    op = input("Choose operation (and/or/nand/nor/xor/xnor): ")
    
    result = logic_gate(a, b, op)
    print(f"\n{a} {op.upper()} {b} = {result}\n")
    
    again = input("Try another? (y/n): ")
    if again.lower() == "n":
        break