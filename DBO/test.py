import matplotlib.pyplot as plt
import random


def fun(xi, u):
    if xi < u:
        return xi / u
    else:
        return (1 - xi)/(1 - u)


result = random.random()
u = 0.499
x = [result]
for i in range(1000):
    x.append(fun(x[-1], u))

plt.plot(x)
plt.title("Tent Mapping with u = {}".format(u))
plt.xlabel("iterations")
plt.ylabel("value")
plt.show()
