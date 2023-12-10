import matplotlib.pyplot as plt

def logstic(z, u):
    return u * z * (1 - z)

result = 0.200000
u = 0.5
x = [result]
for i in range(200):
    x.append(logstic(x[-1], u))

plt.plot(x)
plt.title("Tent Mapping with u = {}".format(u))
plt.xlabel("iterations")
plt.ylabel("value")
plt.show()
