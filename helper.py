import numpy as np

class xyz:
    x, y, z = 0, 0, 0

    def __init__ (self, value):
        valueType = type(value)

        if valueType is dict:
            self.x, self.y, self.z = [value['x'], value['y'], value['z']]
        elif (valueType is list) or (valueType.__module__ is np.__name__):
            self.x, self.y, self.z = value
        else:
            self.x, self.y, self.z = [value.x, value.y, value.z]

    def toArray (self):
        return np.array([self.x, self.y, self.z])

    def toObject (self):
        return self

    def toDict (self):
        return {'x': self.x, 'y': self.y, 'z': self.z}
