import re


def get_input(filename="inputs/day8.txt"):
    with open(filename) as f:
        data = f.read()
        return [line for line in data.split("\n") if line]


def parse_instruction(inst):
    inst = inst.split()
    target, incdec, val, _, *cond = inst
    cond = " ".join(cond)
    val = int(val)
    val = val * -1 if incdec == "dec" else val
    return target, val, cond


registers = dict()
vals = []

for i in get_input():
    target, val, cond = parse_instruction(i)
    cond = cond.split()
    cond_var = cond[0]
    cond[0] = f"registers['{cond[0]}']"
    cond = (" ".join(cond))
    if target not in registers:
        registers[target] = 0
    if cond_var not in registers:
        registers[cond_var] = 0
    if eval(cond):
        registers[target] += val
    vals.append(max(registers.values()))


print(registers)
print(max(registers.values()))
print(max(vals))
