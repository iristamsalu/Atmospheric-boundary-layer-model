import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load the data from PN.dat
PN_coag = np.loadtxt('PN.dat')

# Define the time and height axes
time = np.linspace(0, 120, 121) / 24  # Time in days
height = np.linspace(0, 3000, PN_coag.shape[1])  # Height in meters, assuming linear spacing

# Select the time range of interest
time_start = 72  # Index corresponding to 3 days (72 hours)
time_end = -1    # Use all time steps

# Extract the data for the selected time range
PN_data = PN_coag[time_start:time_end, :]

# Define the custom colormap
colors = ["#00008B", "#0000FF", "#00FFFF", "#7CFC00", "#FFFF00", "#FF7F00", "#FF0000", "#8B0000"]  # Colors from the image
cmap = LinearSegmentedColormap.from_list("mycmap", colors, N=256)

# Create the heatmap plot
plt.figure(figsize=(10, 8))
im = plt.imshow(PN_data.T, extent=[time[time_start], time[-1], height[0], height[-1]],
           aspect='auto', origin='lower', cmap=cmap, vmin=0, vmax=3.75e4)  # Set vmin and vmax

# Add labels and title
plt.xlabel("Time (days)")
plt.ylabel("Height (m)")
plt.title("Total particle number concentration (sim with nucleation, condensation and coagulation sink)")

# Add colorbar
cbar = plt.colorbar(im, label=r"PN ($\mathrm{cm}^{-3}$) $\times 10^4$")

# Set the colorbar ticks and labels
cbar.formatter = plt.FuncFormatter(lambda x, p: format(x/1e4, ".1f"))
cbar.update_ticks()

# Set the colorbar ticks
cbar.set_ticks(np.linspace(0, 3.75e4, 9))  # Set 9 ticks from 0 to 3.75e4
cbar.set_ticklabels([str(i/2) for i in range(9)]) # Set the tick labels from 0 to 4 with a 0.5 step

# Set the x and y axis limits
plt.xlim(3, 5)
plt.ylim(0, 3000)

# Show the plot
plt.tight_layout()
plt.savefig("PN_heatmap.png")