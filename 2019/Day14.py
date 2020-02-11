import jimpy
import re

data = jimpy.get_input("inputs\day14.txt", "\n")


def parse_data(line):
    inputs, output = line.split(" => ")
    inputs = inputs.split(", ")
    clean_inputs = []
    for i in inputs:
        amount, name = i.split()
        clean_inputs.append((int(amount), name))
    amount, name = output.split()
    clean_output = (int(amount), name)
    return clean_inputs, clean_output


recipe_dict = dict()

for i in data:
    inboy, outboy = parse_data(i)
    recipe_dict[outboy] = inboy


print(recipe_dict)