import numpy as np
import matplotlib.pyplot as plt


diameter_file = "diameter.dat"
conc_file_10m = "particle_conc_10.dat"

total_timesteps = 121
start_day = 1.0
end_day = 6.0

day5_indices = {
    '9:00': 105, '10:00': 106, '11:00': 107, '12:00': 108, '13:00': 109,
    '14:00': 110, '15:00': 111, '16:00': 112, '17:00': 113, '18:00': 114
}

day5_styles = {
    '9:00': {'color': '#1569C7', 'linestyle': 'dashed'},
    '10:00': {'color': 'black',   'linestyle': 'dashed'},
    '11:00': {'color': 'yellow',  'linestyle': 'dashed'},
    '12:00': {'color': 'purple',  'linestyle': 'dashed'},
    '13:00': {'color': 'green',   'linestyle': 'solid'},
    '14:00': {'color': 'aqua',    'linestyle': 'solid'},
    '15:00': {'color': '#800000', 'linestyle': 'solid'},
    '16:00': {'color': '#1569C7', 'linestyle': 'solid', 'marker': 'o'},
    '17:00': {'color': 'orange',  'linestyle': 'solid', 'marker': 'o'},
    '18:00': {'color': 'black',   'linestyle': 'solid', 'marker': 'o'}
}

days = np.linspace(start_day, end_day, total_timesteps)

try:
    diameter_m = np.loadtxt(diameter_file)
except Exception as e:
    raise RuntimeError(f"Failed to load '{diameter_file}': {e}")

try:
    psd_m3_10m = np.loadtxt(conc_file_10m)
except Exception as e:
    raise RuntimeError(f"Failed to load '{conc_file_10m}': {e}")

psd_cm3_10m = psd_m3_10m / 1e6


def plot_psd_lines(ax, diameter, psd_data, time_indices, styles, title):
    """Plot multiple PSD lines on the same axis."""
    ax.set_prop_cycle(None) 

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
    ax.set_xlabel('Diameter (m)')
    ax.set_ylabel('N (# cm$^{-3}$)')
    ax.set_title(title)
    ax.grid(True, which="both", linestyle="--", alpha=0.6)
    ax.set_ylim(0, 3.0e4)
    ax.set_xlim(1e-9, 1e-7)
    ax.legend(title="Time", fontsize='small')

fig, ax = plt.subplots(figsize=(7, 5))
plot_psd_lines(ax, diameter_m, psd_cm3_10m, day5_indices, day5_styles, "PSD at 10 m")

fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.savefig("PSD_day5_10m.png", dpi=300)