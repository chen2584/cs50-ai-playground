class Sentence():

    def evaluate(self, model):
        """Evaluates the logical sentence."""
        raise Exception("nothing to evaluate")

    def formula(self):
        """Returns string formula representing logical sentence."""
        return ""

    def symbols(self):
        """Returns a set of all symbols in the logical sentence."""
        return set()

    @classmethod
    def parenthesize(cls, s):
        """Parenthesizes an expression if not already parenthesized."""
        def balanced(s):
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0
        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        else:
            return f"({s})"

class Symbol(Sentence):
    def __init__(self, name) -> None:
        self.name = name

    def __hash__(self) -> int:
        return hash(
            ("symbol", self.name)
        )
    
    def __repr__(self) -> str:
        return self.name
    
    def evaluate(self, model):
        try:
            return model[self.name]
        except KeyError:
            return False
    
    def formula(self):
        return self.name
    
    def symbols(self):
        return {self.name}
    
class Not(Sentence):
    def __init__(self, operand: Sentence) -> None:
        self.operand = operand

    def __hash__(self) -> int:
        return hash(("not", self.operand))
    
    def evaluate(self, model):
        return not self.operand.evaluate(model)
    
    def formula(self):
        return "¬" + Sentence.parenthesize(self.operand.formula())
    
    def symbols(self):
        return self.operand.symbols()
    
class And(Sentence):
    def __init__(self, *operands: Sentence) -> None:
        self.operands = list(operands)

    def __hash__(self) -> int:
        return hash(
            "and",
            (hash(operand for operand in self.operands))
        )
    
    def add(self, operand: Sentence):
        self.operands.append(operand)
    
    def evaluate(self, model):
        return all(operand.evaluate(model) for operand in self.operands)
    
    def formula(self):
        if (len(self.operands) == 1):
            return self.operands[0]
        return " ^ ".join(Sentence.parenthesize(operand.formula()) for operand in self.operands)
    
    def symbols(self):
        return set.union(*[operand.symbols() for operand in self.operands])
    
class Or(Sentence):
    def __init__(self, *operands: Sentence) -> None:
        self.operands = list(operands)

    def __hash__(self) -> int:
        return hash(
            "and",
            (hash(operand for operand in self.operands))
        )
    
    def evaluate(self, model):
        return any(operand.evaluate(model) for operand in self.operands)
    
    def formula(self):
        if (len(self.operands) == 1):
            return self.operands[0]
        return " ^ ".join(Sentence.parenthesize(operand.formula()) for operand in self.operands)
    
    def symbols(self):
        return set.union(*[operand.symbols() for operand in self.operands])
    
class Implication(Sentence):
    def __init__(self, left_operand: Sentence, right_operand: Sentence) -> None:
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __hash__(self) -> int:
        return hash(
            "implication",
            hash(self.left_operand),
            hash(self.right_operand)
        )
    
    def evaluate(self, model):
        return not (self.left_operand.evaluate(model) and not self.right_operand.evaluate(model))
    
    def formula(self):
        return f"{Sentence.parenthesize(self.left_operand.formula())} => {Sentence.parenthesize(self.right_operand.formula())}"
    
    def symbols(self):
        return set.union(self.left_operand.symbols(), self.right_operand.symbols())
    
class BiConditional(Sentence):
    def __init__(self, left_operand: Sentence, right_operand: Sentence) -> None:
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __hash__(self) -> int:
        return hash(
            "biconditional",
            hash(self.left_operand),
            hash(self.right_operand)
        )
    
    def evaluate(self, model):
        return self.left_operand.evaluate(model) == self.right_operand.evaluate(model)
    
    def formula(self):
        return f"{Sentence.parenthesize(self.left_operand.formula())} <=> {Sentence.parenthesize(self.right_operand.formula())}"
    
    def symbols(self):
        return set.union(self.left_operand.symbols(), self.right_operand.symbols())

def model_check(knowledge: Sentence, query: Sentence):

    def check_all(knowledge: Sentence, query: Sentence, symbols: set, model: dict):

        if not symbols:
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:
            remaining = symbols.copy()
            symbol = remaining.pop()

            model_true = model.copy()
            model_true[symbol] = True

            model_false = model.copy()
            model_false[symbol] = False

            return check_all(knowledge, query, remaining, model_true) and check_all(knowledge, query, remaining, model_false)
    
    symbols = set.union(knowledge.symbols(), query.symbols())
    return check_all(knowledge, query, symbols, dict())