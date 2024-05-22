from logic import *

rain = Symbol("rain")
chen = Symbol("chen")
breath = Symbol("breath")

knowledge = And(
    BiConditional(rain, chen),
    Or(chen, breath),
    Not(And(chen, breath)),
    chen
)
print(knowledge.formula())

print(model_check(knowledge, rain))
