import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker

# File paths
files = {
    "diameter": "diameter.dat",
    "conc_10m": "particle_conc_100.dat",
    "conc_2000m": "particle_conc_500.dat",
    "pn": "PN.dat",
    "pm": "PM.dat",
    "height": "hh.dat",
}

# Time settings
total_steps = 121
time_days = np.linspace(0.0, 5.0, total_steps)
day_times = {
    "Day 4": {'00:00': 72, '06:00': 78, '12:00': 84, '18:00': 90, '24:00': 96},
    "Day 5": {'00:00': 96, '06:00': 102, '12:00': 108, '18:00': 114, '24:00': 120}
}
styles = {
    '00:00': {'color': 'purple', 'marker': 'o', 'linestyle': 'None', 'mfc': 'none'}, 
    '06:00': {'color': 'cyan', 'linestyle': 'dotted'},
    '12:00': {'color': 'lightgreen', 'linestyle': 'dashed'},
    '18:00': {'color': 'orange', 'linestyle': '-.'},
    '24:00': {'color': 'red', 'linestyle': 'solid'}
}

# Heatmap settings
psd_levels = [1, 10, 100, 500, 1000, 5000, 10000, 20000, 40000, 80000]
pn_levels = [0, 1e3, 1e4, 2e4, 3e4, 3.2e4, 3.4e4, 3.6e4, 3.8e4]
pm_levels = [0.000, 1.200, 1.225, 1.250, 1.275, 1.300, 1.325, 1.350]
cmap = {'psd': 'jet', 'pn': 'viridis', 'pm': 'viridis'}
psd_norm = mcolors.LogNorm(vmin=min(psd_levels), vmax=max(psd_levels))
pm_norm = mcolors.BoundaryNorm(pm_levels, plt.get_cmap(cmap['pm']).N)

# Load data 
diameter_nm = np.loadtxt(files["diameter"]) * 1e9
psd_data = {
    "10 m": np.loadtxt(files["conc_10m"]) / 1e6,
    "2000 m": np.loadtxt(files["conc_2000m"]) / 1e6
}
PN = np.loadtxt(files["pn"])
PM = np.loadtxt(files["pm"])
height = np.loadtxt(files["height"])

# Time slicing for heatmaps
t_start, t_end = 3.0, 5.0
i_start = np.abs(time_days - t_start).argmin()
i_end = np.abs(time_days - t_end).argmin()
time_hm = time_days[i_start:i_end+1]
T_h, H_h = np.meshgrid(time_hm, height)
PN_sel = PN[i_start:i_end+1, :]
PM_sel = PM[i_start:i_end+1, :]

# Plot setup
fig, axs = plt.subplots(3, 3, figsize=(18, 15))

# 1. PSD Heatmaps
for i, (label, data) in enumerate(psd_data.items()):
    ax = axs[i, 0]
    T, D = np.meshgrid(time_hm, diameter_nm)
    cs = ax.contourf(T, D, data[i_start:i_end+1].T, 
                     levels=psd_levels, norm=psd_norm, cmap=cmap['psd'], extend='max')
    
    ax.set(yscale='log', xlabel='Day (d)', ylabel='Diameter (nm)', 
           title=f'Particle size distribution\nat {label}', xlim=(t_start, t_end), ylim=(1, 1000))
    ax.yaxis.set_major_locator(mticker.LogLocator(base=10))
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%g'))
    ax.yaxis.set_minor_locator(mticker.NullLocator())
    ax.tick_params(labelsize=8)
    
    cbar = fig.colorbar(cs, ax=ax, format='%g')
    cbar.set_label('dN/dlog$_{10}$Dp (# cm$^{-3}$)', size=9)
    cbar.ax.tick_params(labelsize=8)

# 2. PSD Line Plots
for i, (label, data) in enumerate(psd_data.items()):
    for j, (day, times) in enumerate(day_times.items(), start=1):
        ax = axs[i, j]
        for time_label, idx in times.items():
            s = styles[time_label]
            ax.plot(diameter_nm, data[idx], label=time_label, 
                    color=s['color'], linestyle=s.get('linestyle', '-'), 
                    marker=s.get('marker', None), mfc=s.get('mfc', 'none'),
                    mec=s['color'], linewidth=1.2, markersize=4)
        ax.set(xscale='log', yscale='log', xlabel='Diameter (nm)', ylabel='N (# cm$^{-3}$)',
               title=f'{day} at {label}', xlim=(1, 1000), ylim=(1, 1e5))
        ax.grid(True, which="both", ls="--", alpha=0.5)
        ax.legend(fontsize=7, title="Time")
        ax.tick_params(labelsize=8)

# 3. PN and PM Heatmaps
for col, (data, levels, cmap_name, norm, label, title) in enumerate([
    (PN_sel, pn_levels, cmap['pn'], None, 'PN (# cm$^{-3}$)', f'PN Concentration \nmax={PN_sel.max():.2e}'),
    (PM_sel, pm_levels, cmap['pm'], pm_norm, 'PM (μg/m³)', f'PM Concentration \nmax={PM_sel.max():.2e}')
]):
    ax = axs[2, col]
    cf = ax.contourf(T_h, H_h, data.T, levels=levels, cmap=cmap_name, norm=norm, extend='max')
    ax.set(xlabel='Day (d)', ylabel='Height (m)', title=title, xlim=(t_start, t_end), ylim=(0, 3000))
    ax.tick_params(labelsize=8)
    cbar = fig.colorbar(cf, ax=ax, ticks=levels)
    cbar.set_label(label, size=9)
    cbar.ax.tick_params(labelsize=8)

axs[2, 2].axis('off')
plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig("combined_plots_i.png", dpi=300)
