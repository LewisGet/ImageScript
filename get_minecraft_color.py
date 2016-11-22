import PIL.Image as Image
import numpy as np
import math

colorPix = 0
prefix = 0

def getR (color):
    return color[0]
def getG (color):
    return color[1]
def getB (color):
    return color[2]

def getImageArray (number):
    colors = []

    img = Image.open("./colors/" + number + ".png").convert("RGB")
    imageArray = np.array(img)

    for xy in imageArray:
        for y in xy:
            colors.append(y)

    colors = np.array(colors)
    rgb = np.mean(colors, axis=0)

    return [int(round(rgb[0])), int(round(rgb[1])), int(round(rgb[2]))]

colors = []

for i in range(32):
    rgb = getImageArray(str(i + 1))

    colors.append(rgb)

def distance (c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2

    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def getClosestColor (targetColor, colorList):
    closest = 0
    closest_index = None
    closest_color = None
    closest_isset = False

    for index, thisColor in enumerate(colorList):

        color_dis = distance(targetColor, thisColor)

        if ((color_dis < closest) or (not closest_isset)):
            closest = color_dis
            closest_index = index
            closest_color = thisColor
            closest_isset = True

    return [closest_index, closest_color]

(index, color) = getClosestColor([255, 55, 55], colors)

imageName = index + 1

print(index, imageName, color)