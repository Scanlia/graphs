import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data from the first graph (Volumes)
data_vol = {
    'Feature': ['Total', 'Non-calcified', 'Calcified'],
    'Women': [38.2, 28, 3.8],
    'Men': [85.95, 64.4, 11.25]
}
df_vol = pd.DataFrame(data_vol).set_index('Feature')

# Data from the second graph (Percentages)
data_pct = {
    'Feature': ['High Risk', '% Atheroma\nVolume'],
    'Women': [2.5, 1.74],
    'Men': [9.2, 2.85]
}
df_pct = pd.DataFrame(data_pct).set_index('Feature')

# Combine feature names for the x-axis
features = list(df_vol.index) + list(df_pct.index)
x = np.arange(len(features))  # the label locations

# Bar width
width = 0.35

# Define colors
color_women = 'pink'
color_men = 'lightblue'

# Set font sizes
title_fontsize = 18
label_fontsize = 16
legend_fontsize = 14
tick_fontsize = 12
bar_label_fontsize = 10 # Slightly smaller for potentially crowded bars

# Create figure and primary axes
fig, ax1 = plt.subplots(figsize=(8, 8)) # Adjusted size slightly for 5 features

# --- Plot Volume Data on Primary Axis (ax1) ---
women_vol = df_vol['Women'].values
men_vol = df_vol['Men'].values
x_vol = np.arange(len(df_vol)) # Positions for volume features [0, 1, 2]

rects1_vol = ax1.bar(x_vol - width/2, women_vol, width, label='Women', color=color_women)
rects2_vol = ax1.bar(x_vol + width/2, men_vol, width, label='Men', color=color_men)

# Set primary y-axis label and color
ax1.set_ylabel('Volume (mm³)', color='black', fontsize=label_fontsize)
ax1.tick_params(axis='y', labelcolor='black', labelsize=tick_fontsize)
ax1.set_xlabel('Plaque Features', fontsize=label_fontsize)

# --- Create Secondary Axis (ax2) ---
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

# --- Plot Percentage Data on Secondary Axis (ax2) ---
women_pct = df_pct['Women'].values
men_pct = df_pct['Men'].values
# Positions for percentage features [3, 4] on the shared x-axis scale
x_pct = np.arange(len(df_vol), len(features))

rects1_pct = ax2.bar(x_pct - width/2, women_pct, width, color=color_women)
rects2_pct = ax2.bar(x_pct + width/2, men_pct, width, color=color_men)

# Set secondary y-axis label and color
ax2.set_ylabel('Percentage (%)', color='black', fontsize=label_fontsize)
ax2.tick_params(axis='y', labelcolor='black', labelsize=tick_fontsize)
# Ensure secondary y-axis doesn't use scientific notation if values are small
# ax2.ticklabel_format(style='plain', axis='y')


# --- Configure Combined X-axis ---
ax1.set_xticks(x)
ax1.set_xticklabels(features, rotation=0, ha='center')
ax1.tick_params(axis='x', labelsize=tick_fontsize)


# --- Title and Legend ---
plt.title('Comparison of Plaque Volumes and Percentages', fontsize=title_fontsize, pad=20) # Added padding

# Create a single combined legend
# Get handles and labels from ax1 (ax2 uses same colors/labels conceptually)
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, title='Sex', loc='upper right', bbox_to_anchor=(0.93, 0.90), fontsize=legend_fontsize, title_fontsize=legend_fontsize)


# --- Add Bar Labels ---
ax1.bar_label(rects1_vol, padding=3, fmt='%.2f', fontsize=bar_label_fontsize)
ax1.bar_label(rects2_vol, padding=3, fmt='%.2f', fontsize=bar_label_fontsize)

ax2.bar_label(rects1_pct, padding=3, fmt='%.2f%%', fontsize=bar_label_fontsize)
ax2.bar_label(rects2_pct, padding=3, fmt='%.2f%%', fontsize=bar_label_fontsize)

# --- Layout and Display ---
fig.tight_layout()  # otherwise the right y-label is slightly clipped
# Adjust layout further if needed after tight_layout
plt.subplots_adjust(top=0.9) # Make space for title and legend
plt.savefig('plaque_graph.png', transparent=True)
plt.show()