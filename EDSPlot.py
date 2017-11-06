import numpy as np
import matplotlib.pyplot as plot


filepath="G:\StardustResearch\SEM\Acfer3A_SEM\Acfer3ASmallCraterEMSA\Crater16(1)_pt1.emsa"

with open(filepath) as file:
    data = file.read()

data = data.split('\n')

x = [row.split(' ')[0] for row in data]
y = [row.split(' ')[1] for row in data]

fig = plot.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Plot title...")    
ax1.set_xlabel('your x label..')
ax1.set_ylabel('your y label...')

ax1.plot(x,y, c='r', label='the data')

leg = ax1.legend()

plot.show()