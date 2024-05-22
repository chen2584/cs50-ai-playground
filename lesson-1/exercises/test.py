class Test:
    def __init__(self, number) -> None:
        self.number = number
        pass
    def __eq__(self, other) -> bool:
        return self.number == other.number

test1 = Test(1)
test2 = Test(1)
result = test1 == test2
print(result)

test3 = dict()
if not test3:
    print("3")