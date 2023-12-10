import matplotlib.pyplot as plt


def fun(xi, u):
    if xi < u:
        return xi / u
    else:
        return (1 - xi)/(1 - u)


result = 0.200000
u = 0.7
x = [result]
for i in range(200):
    x.append(fun(x[-1], u))

plt.plot(x)
plt.title("Tent Mapping with u = {}".format(u))
plt.xlabel("iterations")
plt.ylabel("value")
plt.show()
