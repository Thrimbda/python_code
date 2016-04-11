import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-20, 20, 3000, endpoint=True)
k = np.arange(-100, 100)
y = []

for i in k:
    y.append(x ** k)

for i in np.arange(200):
    plt.plot(x, y[i], color="blue", linewidth=2, linestyle='-')
plt.show()
