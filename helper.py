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

class training_data:
    actions = []
    actions_reverse = []
    first_place_fps = None
    first_place_location = None
    first_place_location_array = None
    last_place_fps = None
    last_place_location = None
    last_place_location_array = None

    def __init__ (self, actions):
        self.actions = actions
        self.actions_reverse = actions[:]
        self.actions_reverse.reverse()

    def set_fps_location (self, fps, value):
        self.actions[fps]['location'] = xyz(value)

        return self

    def get_fps_location (self, fps):
        return xyz(self.actions[fps]['location'])

    def get_fps_location_array (self, fps):
        return self.get_fps_location().toArray()

    def get_fps_block (self, fps):
        return xyz(self.actions[fps]['block'])

    def set_fps_block_location (self, fps, value):
        self.actions[fps]['blockLocation'] = xyz(value)

        return self

    def get_fps_block_location (self, fps):
        return xyz(self.actions[fps]['blockLocation'])

    def get_fps_block_location_array (self, fps):
        return self.get_fps_block_location().toArray()

    def set_fps_direction (self, fps, value):
        self.actions[fps]['direction'] = xyz(value)

        return self

    def get_fps_direction (self, fps):
        return xyz(self.actions[fps]['direction'])

    def get_fps_direction_array (self, fps):
        return self.get_fps_direction().toArray()

    def get_first_place (self):
        if self.first_place_fps not None
            return self.first_place_fps, self.first_place_location, self.first_place_location_array
        
        for fps, frame in enumerate(self.actions):
            if self.get_fps_block(fps) is "place":
                self.first_place_fps, self.first_place_location, self.first_place_location_array = fps, self.get_fps_block_location(fps), self.get_fps_block_location_array(fps)
                return self.first_place_fps, self.first_place_location, self.first_place_location_array

        return [None] * 3

    def get_last_place (self):
        if self.last_place_fps not None
            return self.last_place_fps, self.last_place_location, self.last_place_location_array
        
        for fps, frame in enumerate(self.actions_reverse):
            if self.get_fps_block(fps) is "place":
                self.last_place_fps, self.last_place_location, self.last_place_location_array = fps, self.get_fps_block_location(fps), self.get_fps_block_location_array(fps)
                return self.last_place_fps, self.last_place_location, self.last_place_location_array

        return [None] * 3

    def get_after_place_half_sec_fps (self):
        value = []

        placeFps, _, _ = self.get_last_place()

        for fps in range(placeFps + 1, placeFps + 16):
            value.append(self.actions[fps])

        return value

    def get_before_place_half_sec_fps (self):
        value = []

        placeFps, _, _ = self.get_first_place()

        for fps in range(placeFps + 1, placeFps + 16):
            value.append(self.actions[fps])

        return value

    def get_start_half_sec_fps (self):
        value = []

        for fps in range(0, 15):
            value.append(self.actions[fps])

        return value

    def get_end_half_sec_fps (self):
        value = []

        for fps in range(len(self.actions) - 16, len(self.actions) - 1):
            value.append(self.actions[fps])

        return value
