from matplotlib import pyplot as p
import numpy as np

# select parameters and data! 
model_v = 3     # model version
day     = 1     # day
i       = 0     # 0 - uwind, 1 - vwind, 2 - theta

data_x_axis_list    = ['uwind.dat', 'vwind.dat', 'theta.dat']
data_x_axis_labels  = ['u (m/s)', 'v (m/s)', 'theta (K)']
x_axis_limits       = {0: [0, 16],
                       1: [-5, 8],
                       2: [288.15, 303.15]}

# load all the input files
data_x_axis = np.loadtxt(data_x_axis_list[i])
data_time   = np.loadtxt('time.dat')
data_hh     = np.loadtxt('hh.dat')

p.figure(figsize=(8, 8))

# line colors and list index
colors  = ['b', 'orange', 'g', 'r', 'purple', 'brown']
color_i = 0

# every 4th hour is plotted
time_start = (day-1) * 24
time_i     = time_start
time_end   = (day*24) - 4

while time_i <= time_end:
    p.plot(data_x_axis[time_i], data_hh, color=colors[color_i], linestyle='-', marker='.', markersize=16, alpha=0.5)
    time_i  += 4
    color_i += 1
    
p.xlabel(data_x_axis_labels[i])
p.ylabel('h (m)')

min_x = (x_axis_limits[i])[0]
max_x = (x_axis_limits[i])[1]
p.xlim((min_x, max_x))
p.ylim((0,3000))
p.grid(True)
title = 'K' + str(model_v) + ' - Day ' + str(day)
p.title(title)

#p.show()
p.savefig('profileplot_o.svg')
    


