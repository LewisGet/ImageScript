import PIL.Image as Image
import numpy as np
import math

def getImageArray (number):
    colors = []

    img = Image.open("./colors/" + number + ".png").convert("RGB")
    imageArray = np.array(img)

    for xy in imageArray:
        for y in xy:
            colors.append(y)

    colors = np.array(colors)
    rgb = np.mean(colors, axis=0)
    r, g, b = rgb

    return [int(round(r)), int(round(g)), int(round(b))]

def getItemColors():
    colorsDataset = [[35,0], [35,1], [35,2], [35,3], [35,4], [35,5], [35,6], [35,7], [159,0], [159,1], [159,2], [159,3], [159,4], [159,5], [159,6], [159,7], [35,8], [35,9], [35,10], [35,11], [35,12], [35,13], [35,14], [35,15], [159,8], [159,9], [159,10], [159,11], [159,12], [159,13], [159,14], [159,15]]
    colors = [None] * 32

    for i in range(32):
        colors[i] = getImageArray(str(i + 1))

    return [colors, colorsDataset]

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
