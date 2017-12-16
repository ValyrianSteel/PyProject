import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.set_title("Axes Example")

major_ticks = np.arange(0, 101, 20)
minor_ticks = np.arange(0, 101, 5)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")

ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

ax.text(42.5, 50, "shiyanlou")

fig.show()
