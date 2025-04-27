import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches

# Parse the data including HR and CI
data = {
    'Feature': ['TPV', 'TPV', 'NCP', 'NCP', 'CP', 'CP'],
    'Sex': ['Women', 'Men', 'Women', 'Men', 'Women', 'Men'],
    'HR_CI_str': [
        '1.177 (1.117, 1.241)', # Corrected typo here
        '1.053 (1.033, 1.074)',
        '1.271 (1.166, 1.384)',
        '1.116 (1.080, 1.153)',
        '1.229 (1.137, 1.330)',
        '1.054 (1.012, 1.098)'
    ]
}
df = pd.DataFrame(data)

# Function to extract HR, Lower CI, Upper CI from string
def parse_hr_ci(hr_ci_str):
    parts = hr_ci_str.replace('(', '').replace(')', '').replace(',', '').split()
    hr = float(parts[0])
    lower_ci = float(parts[1])
    upper_ci = float(parts[2])
    return hr, lower_ci, upper_ci

# Apply parsing function
parsed_data = df['HR_CI_str'].apply(parse_hr_ci)
df['HR'] = [x[0] for x in parsed_data]
df['Lower CI'] = [x[1] for x in parsed_data]
df['Upper CI'] = [x[2] for x in parsed_data]

# Calculate errors for error bars (asymmetric)
df['err_lower'] = df['HR'] - df['Lower CI']
df['err_upper'] = df['Upper CI'] - df['HR']

# Define darker colors
color_map = {'Women': 'deeppink', 'Men': 'royalblue'}
df['color'] = df['Sex'].map(color_map)

# Sort data first by Feature (ascending), then Sex (descending - Women first visually)
df = df.sort_values(by=['Feature', 'Sex'], ascending=[True, False])
df = df.reset_index(drop=True)

# --- Calculate Custom Y-Positions ---
features = df['Feature'].unique() # ['CP', 'NCP', 'TPV']
group_sep = 2.0  # Vertical separation between the center of feature groups
pair_sep = 0.6   # Vertical separation between Men/Women within a feature group
y_positions = []
y_tick_positions = []
y_tick_labels = []

for i, feature in enumerate(features):
    base_y = i * group_sep # Center of the group
    y_tick_positions.append(base_y)
    y_tick_labels.append(feature)
    # Assign positions: Women slightly above center, Men slightly below
    y_positions.append(base_y + pair_sep / 2) # Women position (first in pair)
    y_positions.append(base_y - pair_sep / 2) # Men position (second in pair)

df['y_pos'] = y_positions

# --- Define NEW Font Sizes ---
title_fontsize = 16 # Increased
axis_label_fontsize = 14 # Increased
tick_label_fontsize = 12 # Increased
hr_text_fontsize = 11 # Increased
legend_fontsize = 11 # Increased

# --- Create the Forest Plot ---
# Keep figsize the same as previous plot
fig, ax = plt.subplots(figsize=(8, 6))

# Plot points and error bars using calculated y_pos
for i, row in df.iterrows():
    ax.errorbar(x=row['HR'], y=row['y_pos'],
                xerr=[[row['err_lower']], [row['err_upper']]],
                fmt='o', # 'o' for point marker
                color=row['color'],
                ecolor=row['color'], # Error bar color
                elinewidth=2,
                capsize=5,
                markersize=7,
                label=row['Sex'] if not i < 2 else "")

# --- Add Vertical Line at HR=1.0 ---
ax.axvline(x=1.0, color='grey', linestyle='--')

# --- Set Limits and Ticks ---
min_ci = df['Lower CI'].min()
max_ci = df['Upper CI'].max()
x_padding = (max_ci - min_ci) * 0.15
text_offset = (max_ci - min_ci) * 0.05 # May need adjustment if text overlaps bars

# Expand right limit even more to accommodate potentially wider text labels
ax.set_xlim([min_ci - x_padding, max_ci + x_padding + text_offset*3.5]) # Adjusted expansion factor

# Set custom y-ticks and labels with NEW font size
ax.set_yticks(y_tick_positions)
ax.set_yticklabels(y_tick_labels, fontsize=tick_label_fontsize) # Apply increased font size
ax.set_ylim([min(y_positions) - pair_sep, max(y_positions) + pair_sep])

# Set tick font size for x-axis as well
ax.tick_params(axis='x', labelsize=tick_label_fontsize)


# --- Labels and Title (with NEW font sizes) ---
ax.set_xlabel('Hazard Ratio (95% CI) per 50mm³ Plaque', fontsize=axis_label_fontsize)
ax.set_ylabel('Plaque Feature', fontsize=axis_label_fontsize)
ax.set_title('Forest Plot of Hazard Ratios by Sex', fontsize=title_fontsize, pad=20)

# --- Add Text Labels for HR [CI] (with NEW font size) ---
for i, row in df.iterrows():
    hr_text = f"{row['HR']:.3f} ({row['Lower CI']:.3f}, {row['Upper CI']:.3f})"
    text_x_pos = row['Upper CI'] + text_offset
    ax.text(text_x_pos, row['y_pos'], hr_text, verticalalignment='center', fontsize=hr_text_fontsize) # Apply increased font size

# --- Create Legend (with NEW font sizes) ---
handles = [mpatches.Patch(color=color_map['Women'], label='Women'),
           mpatches.Patch(color=color_map['Men'], label='Men')]
# Apply increased font size to legend text and title
ax.legend(handles=handles, title="Sex", loc='lower right', fontsize=legend_fontsize, title_fontsize=legend_fontsize)

# --- Adjust Layout ---
# Use tight_layout, potentially adjust rect further if needed for larger text
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjusted right margin slightly more
plt.grid(axis='y', linestyle=':', alpha=0.6)

plt.show()