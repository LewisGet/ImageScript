import PIL.Image as Image
import numpy as np
import webcolors as color
import get_minecraft_color as mc

# about convert mode
# http://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes
img = Image.open("./test/1.png").convert("RGBA")
imgArray = np.array(img)

display = []
ownColors, ownColorsDataset = mc.getItemColors()

for x, row in enumerate(imgArray):
    for y, color in enumerate(row):
        r, g, b, visible = color
        rgb = [r, g, b]

        if (visible > 200):
            closest_index, _ = mc.getClosestColor(rgb, ownColors)
            colorsData = ownColorsDataset[closest_index]

            display.append([x, y, colorsData])

for item in display:
    print(item)