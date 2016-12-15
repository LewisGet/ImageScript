import PIL.Image as Image
import numpy as np
import image_to_command as ic

imc = ic.imageCommander("./test/1.png")

for item in imc.contour:
    print(item)