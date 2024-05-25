# - Gilderoy, Minerva, Pomona and Horace each belong to a different one of the four hourses: Gryffindor, Hufflepuff, Revenclaw and Slytherin House.
# - Gilderoy belongs to Gryffindor or Ravenclaw.
# - Pomona does not belong in Slytherin.
# - Mimerva belongs to Gryffindor

# Summary by Chen
# Gilderoy => Ravenclaw
# Minerva => Gryffindor
# Ponoma => Hufflepuff
# Horace => Syltherin

from logic import *

people = ["Gilderoy", "Minerva", "Ponoma", "Horace"]

houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

symbols: list[Symbol] = []

knowledge = And()

for person in people:
    for house in houses:
        symbols.append(Symbol(f"{person}{house}"))

# each person must belong to a house.
for person in people:
    knowledge.add(Or(
        Symbol(f"{person}Gryffindor"),
        Symbol(f"{person}Hufflepuff"),
        Symbol(f"{person}Ravenclaw"),
        Symbol(f"{person}Slytherin"),
    ))

# If Person in one house then he/she must not be in another house.
for person in people:
    for h1 in houses:
        for h2 in houses:
            if h1 != h2:
                knowledge.add(Implication(Symbol(f"{person}{h1}"), Not(Symbol(f"{person}{h2}"))))

# If House already has a person then another person must not in the same house.
for house in houses:
    for p1 in people:
        for p2 in people:
            if p1 != p2:
                knowledge.add(Implication(Symbol(f"{p1}{house}"), Not(Symbol(f"{p2}{house}"))))

knowledge.add(Or(
    Symbol("GilderoyGryffindor"), Symbol("GilderoyRavenclaw")
))

knowledge.add(Not(Symbol("PonomaSlytherin")))

knowledge.add(Symbol("MinervaGryffindor"))

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)