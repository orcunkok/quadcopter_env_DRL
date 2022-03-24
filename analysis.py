import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import pandas as pd
import numpy as np
DIR = "/home/orc/dev_projects/quadcopter_env_DRL/analysis_data"
FILE = "03-23-2022--13:36:38"
df = pd.read_csv(f"{DIR}/{FILE}")

goal=df.goal[0]
time=df.dt

posX=df.posX
posY=df.posY
posZ=df.posZ


fig =plt.subplots()
plt.plot(time,posX, label="posX")
plt.plot(time,posY, label="posY")
plt.plot(time,posZ, label="posZ")
ax=plt.gca()
ax.axes.xaxis.set_visible(False)
ax.yaxis.grid()
plt.legend()
plt.title(f"GOAL: {goal}", fontsize=20)
plt.suptitle(f"{FILE} Data")
plt.ylabel("Positions")
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
plt.show()


