def HelloWorld(text):
    print(text)
HelloWorld("print")


def calculateSalary(bonus = 1000, deduction = 0):
    return 4000 + bonus - deduction

emp1 = calculateSalary(deduction = 600)
emp2 = calculateSalary(240)
emp3 = calculateSalary(0)

print(emp1, emp2, emp3)
