import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker
import sys # For exiting on error

# --- Configuration ---
# Input file names
diameter_file = "diameter.dat"
conc_file_10m = "particle_conc_10.dat"
conc_file_2000m = "particle_conc_2000.dat"

# Output file names prefix
output_prefix = "PSD" # Files will be saved as PSD_Heatmap.png, PSD_Day4_Lines.png etc.

# Simulation time setup
total_timesteps = 121 # Total number of time steps in the input files
start_day = 1.0      # Simulation start day corresponding to the first timestep
end_day = 6.0        # Simulation end day (exclusive, e.g., Day 5 24:00 is start of Day 6)

# Timesteps to plot for line graphs (indices based on 121 steps from Day 1 00:00 to Day 5 24:00)
# Check these indices match your data structure. If Day 1 00:00 is index 0:
# Day 4: Indices 72 (00:00), 78 (06:00), 84 (12:00), 90 (18:00), 96 (24:00)
day4_indices = {'00:00': 72, '06:00': 78, '12:00': 84, '18:00': 90, '24:00': 96}
# Day 5: Indices 96 (00:00), 102 (06:00), 108 (12:00), 114 (18:00), 120 (24:00)
day5_indices = {'00:00': 96, '06:00': 102, '12:00': 108, '18:00': 114, '24:00': 120}

# Plotting styles for line plots (matching example image)
# Day 4 styles
day4_styles = {
    '00:00': {'color': 'purple', 'linestyle': 'None', 'marker': 'o', 'mfc': 'none'}, # Purple circles
    '06:00': {'color': 'cyan', 'linestyle': 'dotted'},       # Cyan dotted
    '12:00': {'color': 'lightgreen', 'linestyle': 'dashed'}, # Light green dashed
    '18:00': {'color': 'orange', 'linestyle': '-.'},         # Orange dash-dot
    '24:00': {'color': 'red', 'linestyle': 'solid'}           # Red solid (End of Day 4 / Start of Day 5)
}
# Day 5 styles (similar, but 00:00 uses circle marker)
day5_styles = {
    '00:00': {'color': 'purple', 'linestyle': 'None', 'marker': 'o', 'mfc': 'none'}, # Purple circles
    '06:00': {'color': 'cyan', 'linestyle': 'dotted'},       # Cyan dotted
    '12:00': {'color': 'lightgreen', 'linestyle': 'dashed'}, # Light green dashed
    '18:00': {'color': 'orange', 'linestyle': '-.'},         # Orange dash-dot
    '24:00': {'color': 'red', 'linestyle': 'solid'}           # Red solid (End of Day 5)
}

# Heatmap time range (inclusive)
heatmap_start_day = 3.0
heatmap_end_day = 5.0

# Heatmap color normalization and levels (Matching the example image)
heatmap_cmap = 'jet' # Colormap used in the example
# Define the specific contour levels shown in the example colorbar
heatmap_levels = [1, 10, 100, 500, 1000, 5000, 10000, 20000, 40000, 80000]
# Create a logarithmic normalization based on these levels
heatmap_norm = mcolors.LogNorm(vmin=min(heatmap_levels), vmax=max(heatmap_levels))
# Colorbar label
colorbar_label = 'dN/dlog$_{10}$Dp (# cm$^{-3}$)'

# --- Data Loading and Processing ---

# Create time array in days
# linspace includes the endpoint, so end_day=6.0 for 121 steps ending at Day 5 24:00
try:
    days = np.linspace(start_day, end_day, total_timesteps, endpoint=False)
    # If your 121 steps represent midpoints or start times up to just BEFORE Day 6, use endpoint=False.
    # If the 121st step IS Day 6 00:00 (which is Day 5 24:00), use endpoint=True
    # Assuming the 121 steps cover Day 1 00:00 to Day 5 24:00, linspace needs 121 points.
    # Example: If 121 steps cover 5 days exactly (120 intervals), endpoint=True might be needed. Adjust as per your time definition.
    # Let's assume 121 points cover the interval [start_day, end_day] where end_day is Day 5 24:00 (start of day 6)
    days = np.linspace(start_day, 6.0, total_timesteps)


except Exception as e:
    print(f"Error creating time array: {e}")
    sys.exit(1)


# Load diameter in meters and convert to nanometers
try:
    diameter_m = np.loadtxt(diameter_file)
    diameter_nm = diameter_m * 1e9
    print(f"Loaded {len(diameter_nm)} diameter bins from '{diameter_file}'.")
except Exception as e:
    print(f"Error loading diameter file '{diameter_file}': {e}")
    sys.exit(1)

# Load particle concentration data (assuming dN/dlog10Dp in #/m^3)
try:
    psd_m3_10m = np.loadtxt(conc_file_10m)
    print(f"Loaded 10m concentration data with shape {psd_m3_10m.shape} from '{conc_file_10m}'.")
except Exception as e:
    print(f"Error loading 10m concentration file '{conc_file_10m}': {e}")
    sys.exit(1)
try:
    psd_m3_2000m = np.loadtxt(conc_file_2000m)
    print(f"Loaded 2000m concentration data with shape {psd_m3_2000m.shape} from '{conc_file_2000m}'.")
except Exception as e:
    print(f"Error loading 2000m concentration file '{conc_file_2000m}': {e}")
    sys.exit(1)


# Verify data shapes
expected_shape = (total_timesteps, len(diameter_nm))
if psd_m3_10m.shape != expected_shape:
    print(f"Error: Shape mismatch for 10m data. Expected {expected_shape}, got {psd_m3_10m.shape}")
    sys.exit(1)
if psd_m3_2000m.shape != expected_shape:
    print(f"Error: Shape mismatch for 2000m data. Expected {expected_shape}, got {psd_m3_2000m.shape}")
    sys.exit(1)

# Convert concentration units from #/m^3 to #/cm^3
psd_cm3_10m = psd_m3_10m / 1e6
psd_cm3_2000m = psd_m3_2000m / 1e6
print("Converted concentration units from #/m^3 to #/cm^3.")

# --- Plotting Functions ---

def plot_psd_lines(ax, diameter, psd_data, time_indices, styles, title):
    """Plots multiple PSD timesteps on a single axes object."""
    ax.set_prop_cycle(None) # Reset color cycle if needed
    for label, index in time_indices.items():
        if not (0 <= index < psd_data.shape[0]):
            print(f"Warning: Index {index} for label '{label}' is out of bounds (0-{psd_data.shape[0]-1}). Skipping.")
            continue
        style = styles[label]
        ax.plot(diameter, psd_data[index, :],
                label=label,
                color=style.get('color', 'k'),
                linestyle=style.get('linestyle', '-'),
                marker=style.get('marker', None),
                mfc=style.get('mfc', style.get('color')), # marker face color
                mec=style.get('color', 'k'), # marker edge color matches line
                markersize=5, # Adjust marker size if needed
                linewidth=1.5) # Adjust line width if needed
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Diameter (nm)')
    # Using N(# cm^-3) as shorthand label like the example image line plots
    ax.set_ylabel('N (# cm$^{-3}$)')
    ax.set_title(title)
    ax.grid(True, which="both", ls="--", alpha=0.6)
    ax.set_xlim(10**0, 10**3) # Adjust limits if needed based on diameter_nm range
    ax.set_ylim(10**0, 10**5) # Adjust limits if needed based on psd_cm3 data range
    ax.legend(title="Time", fontsize='small')

def plot_psd_heatmap(fig, ax, diameter, days_data, psd_data, norm, cmap, levels, title, cbar_label):
    """Plots a PSD heatmap (contourf) with a consistent colorbar."""
    # Select time range for heatmap
    time_mask = (days_data >= heatmap_start_day) & (days_data <= heatmap_end_day)
    if not np.any(time_mask):
        print(f"Warning: No data found within heatmap time range {heatmap_start_day} - {heatmap_end_day}. Skipping heatmap plot '{title}'.")
        return None

    heatmap_times = days_data[time_mask]
    # Ensure psd_data is indexed correctly if time_mask is not contiguous (should be here)
    heatmap_psd = psd_data[time_mask, :]

    # Create meshgrid for contourf (X=time, Y=diameter)
    # contourf expects Z[y, x] so transpose psd data
    T, D = np.meshgrid(heatmap_times, diameter)

    # Plot filled contours
    # Use extend='max' to color values above the highest level with the max color
    # Use extend='min' to color values below the lowest level with the min color
    # Use extend='both' for both.
    contourf_plot = ax.contourf(T, D, heatmap_psd.T, levels=levels, norm=norm, cmap=cmap, extend='max') # Extend max matches example

    ax.set_yscale('log')
    ax.set_xlabel('Day (d)')
    ax.set_ylabel('Diameter (nm)')
    ax.set_title(title)
    # Set Y limits based on data or fixed range like example
    ax.set_ylim(1, 1000) # Match example image Y-axis limits
    # ax.set_ylim(diameter_nm.min(), diameter_nm.max()) # Alternative: Use actual data range
    ax.set_xlim(heatmap_start_day, heatmap_end_day)

    # Customize Y-axis ticks for log scale
    ax.yaxis.set_major_locator(mticker.LogLocator(base=10, numticks=4)) # 1, 10, 100, 1000
    ax.yaxis.set_major_formatter(mticker.LogFormatterSciNotation(base=10)) # Format as 10^0, 10^1 etc.
    # Or use simple number format:
    # ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%g'))
    ax.yaxis.set_minor_formatter(mticker.NullFormatter()) # Hide minor ticks


    # Add colorbar, explicitly setting ticks and format
    cbar = fig.colorbar(contourf_plot, ax=ax, label=cbar_label, ticks=levels, format=mticker.FormatStrFormatter('%g'))

    return contourf_plot # Return the contour plot object

# --- Generate Plots ---

print("\nGenerating plots...")

# Plot Day 4 Lines
try:
    fig_d4, axes_d4 = plt.subplots(2, 1, figsize=(7, 10), sharex=True)
    fig_d4.suptitle('Day 4 Particle Size Distributions', fontsize=14) # Overall title
    plot_psd_lines(axes_d4[0], diameter_nm, psd_cm3_10m, day4_indices, day4_styles, "At 10 m")
    plot_psd_lines(axes_d4[1], diameter_nm, psd_cm3_2000m, day4_indices, day4_styles, "At 2000 m")
    fig_d4.tight_layout(rect=[0, 0.03, 1, 0.96]) # Adjust layout (leave space for suptitle)
    save_name_d4 = f"{output_prefix}_Day4_Lines.png"
    fig_d4.savefig(save_name_d4, dpi=300)
    plt.close(fig_d4)
    print(f"Saved: {save_name_d4}")
except Exception as e:
    print(f"Error generating Day 4 line plot: {e}")

# Plot Day 5 Lines
try:
    fig_d5, axes_d5 = plt.subplots(2, 1, figsize=(7, 10), sharex=True)
    fig_d5.suptitle('Day 5 Particle Size Distributions', fontsize=14) # Overall title
    plot_psd_lines(axes_d5[0], diameter_nm, psd_cm3_10m, day5_indices, day5_styles, "At 10 m")
    plot_psd_lines(axes_d5[1], diameter_nm, psd_cm3_2000m, day5_indices, day5_styles, "At 2000 m")
    fig_d5.tight_layout(rect=[0, 0.03, 1, 0.96]) # Adjust layout
    save_name_d5 = f"{output_prefix}_Day5_Lines.png"
    fig_d5.savefig(save_name_d5, dpi=300)
    plt.close(fig_d5)
    print(f"Saved: {save_name_d5}")
except Exception as e:
    print(f"Error generating Day 5 line plot: {e}")

# Plot Heatmaps
try:
    fig_hm, axes_hm = plt.subplots(2, 1, figsize=(8, 10), sharey=True) # Share Y axis (Diameter), adjusted figsize
    fig_hm.suptitle('Particle Size Distribution Heatmaps (Day 3-5)', fontsize=14) # Overall title

    # Call the updated function, passing the figure object 'fig_hm'
    plot_psd_heatmap(fig_hm, axes_hm[0], diameter_nm, days, psd_cm3_10m, heatmap_norm, heatmap_cmap, heatmap_levels, "At 10 m", colorbar_label)
    plot_psd_heatmap(fig_hm, axes_hm[1], diameter_nm, days, psd_cm3_2000m, heatmap_norm, heatmap_cmap, heatmap_levels, "At 2000 m", colorbar_label)

    # Adjust shared Y axis limits AFTER plotting to ensure they are set correctly
    axes_hm[0].set_ylim(1, 1000) # Set Y limits from 1 nm to 1000 nm to match example

    # Adjust layout AFTER plotting and adding colorbars
    # Give more space on the right for the colorbars
    fig_hm.tight_layout(rect=[0, 0.03, 0.88, 0.95]) # [left, bottom, right, top]

    save_name_hm = f"{output_prefix}_Heatmap.png"
    fig_hm.savefig(save_name_hm, dpi=300)
    plt.close(fig_hm)
    print(f"Saved: {save_name_hm}")
except Exception as e:
    print(f"Error generating heatmap plot: {e}")


print("\nScript finished.")