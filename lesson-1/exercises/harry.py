from logic import *

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

knowledge = And(
    Implication(Not(rain), hagrid), # If is not Raning then visit hagrid # error because False => True
    Or(hagrid, dumbledore), # Visit hagrid and dumblesore
    Not(And(hagrid, dumbledore)), # but Not Both
    dumbledore # Visit Dumbledore
)

print(knowledge.formula())

print(model_check(knowledge, rain))
