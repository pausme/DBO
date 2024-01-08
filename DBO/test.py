import matplotlib.pyplot as plt
import random

pop = 30
P_percent = 0.2
pNum = round(P_percent * pop)
# print(pNum)
x = 0

for i in range(pNum):
    print(i)

for _ in range(20, pop):
    x += 1

print(x)