import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---

# Input file names
diameter_file = "diameter.dat"
conc_file_10m = "particle_conc_10.dat"
conc_file_2000m = "particle_conc_2000.dat"

# Simulation time setup
total_timesteps = 121
start_day = 1.0    
end_day = 6.0        

# Day 5: Time indices and plotting styles
day5_indices = {
    '9:00': 105, '10:00': 106, '11:00': 107, '12:00': 108, '13:00': 109,
    '14:00': 110, '15:00': 111, '16:00': 112, '17:00': 113, '18:00': 114
}

day5_styles = {
    '9:00':  {'color': '#1569C7', 'linestyle': 'dashed'}, 
    '10:00': {'color': 'black', 'linestyle': 'dashed'},
    '11:00': {'color': 'yellow', 'linestyle': 'dashed'},
    '12:00': {'color': 'purple', 'linestyle': 'dashed'},
    '13:00': {'color': 'green', 'linestyle': 'solid'},
    '14:00': {'color': 'aqua', 'linestyle': 'solid'},
    '15:00': {'color': '#800000', 'linestyle': 'solid'},
    '16:00': {'color': '#1569C7', 'linestyle': 'solid', 'marker': 'o'},
    '17:00': {'color': 'orange',  'linestyle': 'solid', 'marker': 'o'},
    '18:00': {'color': 'black',   'linestyle': 'solid', 'marker': 'o'}
}

# --- Load Data ---

# Create time array in days
days = np.linspace(start_day, end_day, total_timesteps)

# Load diameter in meters
try:
    diameter_m = np.loadtxt(diameter_file)
except Exception as e:
    raise RuntimeError(f"Failed to load '{diameter_file}': {e}")

# Load concentration data (in #/m³)
try:
    psd_m3_10m = np.loadtxt(conc_file_10m)
    psd_m3_2000m = np.loadtxt(conc_file_2000m)
except Exception as e:
    raise RuntimeError(f"Failed to load concentration data: {e}")

# Convert from #/m³ to #/cm³
psd_cm3_10m = psd_m3_10m / 1e6
psd_cm3_2000m = psd_m3_2000m / 1e6

# --- Plotting Function ---

def plot_psd_lines(ax, diameter, psd_data, time_indices, styles, title):
    """Plot multiple PSD lines on the same axis."""
    ax.set_prop_cycle(None)  # Reset color cycle

    for label, index in time_indices.items():
        if index >= psd_data.shape[0]:
            print(f"Warning: Index {index} out of bounds for time '{label}'")
            continue

        style = styles.get(label, {})
        ax.plot(
            diameter,
            psd_data[index, :],
            label=label,
            color=style.get('color', 'k'),
            linestyle=style.get('linestyle', '-'),
            marker=style.get('marker', None),
            mfc=style.get('color', 'k'),
            mec=style.get('color', 'k'),
            markersize=5,
            linewidth=1.5
        )

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Diameter (m)')
    ax.set_ylabel('N (# cm$^{-3}$)')
    ax.set_title(title)
    ax.grid(True, which="both", linestyle="--", alpha=0.6)
    ax.set_ylim(1e0, 5e4)
    ax.set_xlim(0, 10**(-7))
    ax.legend(title="Time", fontsize='small')

# --- Plotting ---

fig, axes = plt.subplots(2, 1, figsize=(7, 10), sharex=True)
fig.suptitle('Day 5 Particle Size Distributions', fontsize=14)

plot_psd_lines(axes[0], diameter_m, psd_cm3_10m, day5_indices, day5_styles, "At 10 m")
plot_psd_lines(axes[1], diameter_m, psd_cm3_2000m, day5_indices, day5_styles, "At 2000 m")

fig.tight_layout(rect=[0, 0.03, 1, 0.96])
fig.savefig("PSD_day5.png", dpi=300)
