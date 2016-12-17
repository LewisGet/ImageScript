import PIL.Image as Image
import numpy as np
import image_to_command as ic

for images in range(1, 53):
    try:
        imc = ic.imageCommander("./builderTest1/test%04d.png" % (images))

        for dataset in imc.builds:
            print (imc.getBuildCommand(dataset))
    except Exception as e:
        pass

    try:
        imc = ic.imageCommander("./countingTest1/test%04d.png" % (images))

        a, b = imc.builds[0], imc.builds[len(imc.builds) - 1]

        command = imc.getCountingCommand(a, b)

        print (command)
    except Exception as e:
        pass
