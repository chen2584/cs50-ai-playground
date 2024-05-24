from logic import *
import termcolor

chen = Symbol("Chen")
john = Symbol("John")
adam = Symbol("Adam")
characters = [chen, john, adam]

kitchen = Symbol("Kitchen")
toilet = Symbol("Toilet")
living = Symbol("Living")
rooms = [kitchen, toilet, living]

knift = Symbol("Knift")
gun = Symbol("Gun")
scrissor = Symbol("Scrissor")
weapons = [knift, gun, scrissor]

symbols = characters + rooms + weapons # Merge Multiple list into One list

def knowledge_check(knowledge: Sentence):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol.formula()}: YES!", "green")
        elif not model_check(knowledge, Not(symbol)): # If still false, That's means knowledge not sure
            print(f"{symbol.formula()}: MAYBE")

knowledge = And(
    Or(chen, john, adam),
    Or(kitchen, toilet, living),
    Or(knift, gun, scrissor)
)

# เปิดการ์ดทั้ง 3 ประเภท อย่างละ 1 ใบ รู้ว่าไม่ใช่ 3 ใบนี้แน่นอน
knowledge.add(And(
    Not(john), Not(kitchen), Not(knift)
))

# หลังจากทายผล ผิด และรู้ว่าต้องมีการ์ดใบไดใบหนึ่ง ที่ไม่อยู่ใน ซองจดหมาย อาจมีแค่ 1 ใบ หรือ มากกว่า 1 ใบ (อาจจะทั้งหมดด้วย)
knowledge.add(Or(
    Not(chen), Not(toilet), Not(scrissor)
))

knowledge.add(Not(adam)) # รู้ว่าไม่ใช่ adam
knowledge.add(Not(living)) # รู้ว่าไม่ใช่ห้องนั่งเล่น

knowledge_check(knowledge)