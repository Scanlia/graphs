import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Original data provided by the user
data = {
    'Model': [
        'DF',
        'CVRF',
        'DF+TPV+HRP',
        'DF+TPV+HRP+DS',
        'CVRF+TPV+HRP',
        'CVRF+TPV+HRP+DS'
    ],
    'AUC': [
        0.548,
        0.668,
        0.723,
        0.755,
        0.791,
        0.797
    ]
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# --- Define the NEW desired order ---
desired_order = [
    'DF',
    'DF+TPV+HRP',
    'DF+TPV+HRP+DS',
    'CVRF',
    'CVRF+TPV+HRP',
    'CVRF+TPV+HRP+DS'
]

# --- Reorder the DataFrame ---
# Use pd.Categorical to set the specific order for the 'Model' column
df['Model'] = pd.Categorical(df['Model'], categories=desired_order, ordered=True)
df = df.sort_values('Model') # Sort the DataFrame based on the categorical order

# --- Font Sizes (kept from previous step) ---
title_fontsize = 16
axis_label_fontsize = 14
tick_label_fontsize = 14
bar_label_fontsize = 13

# --- Create the Bar Chart with NEW Figure Size and Order ---
# Keep figsize=(6, 6)
fig, ax = plt.subplots(figsize=(7, 6))

# Get colors from Viridis map (colors will map to the new order)
colors = plt.cm.viridis(np.linspace(0, 1, len(df)))

# Create bars using the reordered DataFrame
bars = ax.bar(df['Model'], df['AUC'], color=colors)

# --- Add Labels and Title (with larger font sizes) ---
ax.set_ylabel('Area Under Curve (AUC)', fontsize=axis_label_fontsize)
ax.set_xlabel('Model', fontsize=axis_label_fontsize)
ax.set_title('Comparison of Logistic Model Performance (AUC)', fontsize=title_fontsize)

# --- Add Bar Labels (with larger font size) ---
ax.bar_label(bars, fmt='%.3f', fontsize=bar_label_fontsize, padding=3)

# --- Adjust Ticks and Limits (with larger font sizes) ---
# Rotate x-axis labels to 30 degrees
plt.xticks(rotation=30, ha='right', fontsize=tick_label_fontsize)

# Apply increased font size to y-axis ticks
ax.tick_params(axis='y', labelsize=tick_label_fontsize)

# Set y-axis limits
# Recalculate min/max just in case, though order shouldn't change them
min_auc = df['AUC'].min()
max_auc = df['AUC'].max()
ax.set_ylim([min_auc - 0.05, max_auc + 0.05])

# Optional: Add horizontal grid lines
ax.yaxis.grid(True, linestyle=':', alpha=0.7)

# --- Layout and Display ---
# Use tight_layout first
plt.tight_layout()
# Add specific adjustment for bottom margin
plt.subplots_adjust(bottom=0.25) # Adjusted bottom margin slightly more if needed
plt.savefig('mace-logistic-models.png', dpi=300, bbox_inches='tight', transparent=True)
plt.show()