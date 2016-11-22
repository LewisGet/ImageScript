import PIL.Image as Image
import numpy as np
import webcolors as color
import minecraftItem

# about convert mode
# http://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes
img = Image.open("./test.png").convert("RGBA")
imgArray = np.array(img)

display = []

for x, row in enumerate(imgArray):
    for y, color in enumerate(row):
        r = color[0]
        g = color[1]
        b = color[2]
        visible = color[3]

        if (visible > 200):
            display.append([x, y, [r, g, b]])

for item in display:
    print(item)