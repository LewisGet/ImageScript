import PIL.Image as Image
import numpy as np
import get_minecraft_color as mc

class imageCommander:

    imageArray = None;
    imageShape = None;
    registeredColor = None;
    colorDataset = None;
    contour = [];
    builds = [];

    def __init__ (self, imageName):
        self.imageArray = self.getImageArray(imageName)
        self.imageShape = self.imageArray.shape
        self.registeredColor, self.colorDataset = mc.getItemColors()
        self.getBuilderDataset();

    def getImageArray (self, name):
        img = Image.open(name).convert("RGBA")

        return np.array(img)

    def isVisible (self, rgba):
        return (rgba[3] > 200)

    def unVisible (self, rgba):
        return not self.isVisible(rgba)

    def isBorder (self, x, y):
        return (
            x == 0 or
            y == 0 or
            x == self.imageShape[0] - 1 or
            y == self.imageShape[1] - 1
        )

    def isContour (self, x, y):
        if (self.isBorder(x, y)):
            return True

        up, down = self.unVisible(self.imageArray[x][y - 1]), self.unVisible(self.imageArray[x][y + 1])
        left, right = self.unVisible(self.imageArray[x - 1][y]), self.unVisible(self.imageArray[x + 1][y])

        return (up or down or left or right)

    def sortContour (self):
        def dec(data):
            return ((data[0] ** 2) + (data[1] ** 2) + ((data[2][0] + 100) ** 2) + ((data[2][1] + 100) ** 2)) ** (1/2)

        self.contour = sort(my_list_of_objects, key=dec)

    def getBuilderDataset (self):
        for x, row in enumerate(self.imageArray):
            for y, color in enumerate(row):
                r, g, b, visible = color
                rgb = [r, g, b]

                if (self.isVisible(color)):
                    data = [x, y, self.getColorDataset(rgb)]
                    self.builds.append(data)

                    if (self.isContour(x, y)):
                        self.contour.append(data)

    def getColorDataset (self, rgb):
        closest_index, _ = mc.getClosestColor(rgb, self.registeredColor)

        return self.colorDataset[closest_index]

    def getBuildCommand (self, dataset):
        return "builder.builder.buildBlock(" + str(dataset[0]) + ", " + str(dataset[1]) + ", " + str(dataset[2][0])  + ", " + str(dataset[2][1]) + ");"

    def getCountingCommand (self, a, b):
        return "builder.builder.countingBlock(" + str(a[0]) + ", " + str(a[1]) + ", "  + str(b[0]) + ", " + str(b[1]) + ");"
