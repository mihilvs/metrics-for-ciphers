import matplotlib.pyplot as plt
import numpy as np

# Data for the grouped bar chart
distance_measures = ["K-L", "Chi-\nSq", "Bhatt", 
                     "Tan-\neja", "Opt"]

# Normed values from Table 1 (|A| = 26)
shift_26 = [1.7802, 1.7262, 1.7865, 1.7929, 1.8492]
affine_26 = [1.6021, 1.5758, 1.6399, 1.6294, 1.7139]

# Setup for the plot
x = np.arange(2)  # two groups: Shift and Affine
width = 0.15  # the width of the bars
offsets = np.arange(len(distance_measures)) * width  # offsets for each bar within the groups

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8), layout='constrained')

# Add bars for each distance measure in the two groups
for i, (shift_value, affine_value) in enumerate(zip(shift_26, affine_26)):
    ax.bar(x[0] + offsets[i], shift_value, width,
           label=f"Shift ({distance_measures[i]})")
    ax.bar(x[1] + offsets[i], affine_value, width,
           label=f"Affine ({distance_measures[i]})")

# Add labels on top of bars
for i, rect in enumerate(ax.patches):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, f'{height:.3f}', 
            ha='center', va='bottom', fontsize=9)
    ax.text(rect.get_x() + rect.get_width() / 2, 0, 
            f'{distance_measures[i // 2]}', 
            ha='center', va='top', fontsize=9)

# Customize the plot
ax.set_ylabel('Normed Value')
ax.set_title('Normed Values for Distance Measures')
ax.set_xticks([])
ax.set_ylim(0, 2)  # Adjust the y-axis limit for better visualization

plt.show()
