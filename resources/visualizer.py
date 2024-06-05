from PIL import ImageColor
import matplotlib.pyplot as plt

def convert(hex_color_string):
    return ImageColor.getrgb(hex_color_string)

# Define the color palettes
red_palette = ["#330000", "#660000", "#990000", "#cc0000", "#ff0000", "#ff3333", "#ff6666", "#ff9999"]
blue_palette = ["#191b1a", "#294257", "#579c9a", "#99c9b3", "#cce5df", "#e5f2f0"]
purple_palette = ["#2d162c", "#412752", "#683a68", "#9775a6", "#c7a6cc", "#e5cce5"]

red_palette = [convert(c) for c in red_palette]
blue_palette = [convert(c) for c in blue_palette]
purple_palette = [convert(c) for c in purple_palette]

# Plot the color palettes
fig, axes = plt.subplots(3, 1)

for ax, palette, title in zip(axes, [red_palette, blue_palette, purple_palette], ['Red', 'Blue', 'Purple']):
    ax.imshow([palette], aspect='equal')
    ax.set_xticks(range(len(palette)))
    ax.set_xticklabels(palette)
    ax.set_yticks([])
    ax.set_title(title)

plt.tight_layout()
plt.show()
