import numpy as np

class xyz:
    x, y, z = 0, 0, 0

    def __init__ (self, value):
        valueType = type(value)

        if valueType == dict:
            self.x, self.y, self.z = [value['x'], value['y'], value['z']]
        elif (valueType == list) or (valueType.__module__ == np.__name__):
            self.x, self.y, self.z = value[0], value[1], value[2]
        else:
            self.x, self.y, self.z = [value.x, value.y, value.z]

    def toArray (self):
        return np.array([self.x, self.y, self.z], dtype=float)

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
        self.actions_reverse = self.actions[:]
        self.actions_reverse.reverse()

    def flush_actions (self):
        self.actions_reverse = []
        self.first_place_fps = None
        self.first_place_location = None
        self.first_place_location_array = None
        self.last_place_fps = None
        self.last_place_location = None
        self.last_place_location_array = None
        self.actions_reverse = self.actions[:]
        self.actions_reverse.reverse()

    def set_fps_location (self, fps, value):
        self.actions[fps]['location'] = xyz(value)

        return self

    def get_fps_location (self, fps):
        return xyz(self.actions[fps]['location'])

    def get_fps_location_array (self, fps):
        return self.get_fps_location(fps).toArray()

    def get_fps_block (self, fps):
        return self.actions[fps]['block']

    def set_fps_block_location (self, fps, value):
        self.actions[fps]['blockLocation'] = xyz(value)

        return self

    def get_fps_block_location (self, fps):
        return xyz(self.actions[fps]['blockLocation'])

    def get_fps_block_location_array (self, fps):
        return self.get_fps_block_location(fps).toArray()

    def set_fps_direction (self, fps, value):
        self.actions[fps]['direction'] = xyz(value)

        return self

    def get_fps_direction (self, fps):
        return xyz(self.actions[fps]['direction'])

    def get_fps_direction_array (self, fps):
        return self.get_fps_direction(fps).toArray()

    def get_first_place (self):
        if self.first_place_fps is not None:
            return self.first_place_fps, self.first_place_location, self.first_place_location_array
        
        for fps, frame in enumerate(self.actions):
            if self.get_fps_block(fps) is "place":
                self.first_place_fps, self.first_place_location, self.first_place_location_array = fps, self.get_fps_block_location(fps), self.get_fps_block_location_array(fps)
                return self.first_place_fps, self.first_place_location, self.first_place_location_array

        return [None] * 3

    def get_last_place (self):
        if self.last_place_fps is not None:
            return self.last_place_fps, self.last_place_location, self.last_place_location_array
        
        for fps, frame in enumerate(self.actions_reverse):
            if self.get_fps_block(fps) == "place":
                self.last_place_fps, self.last_place_location, self.last_place_location_array = fps, self.get_fps_block_location(fps), self.get_fps_block_location_array(fps)
                return self.last_place_fps, self.last_place_location, self.last_place_location_array

        return [None] * 3

    def get_first_location (self):
        return self.get_fps_location(0)

    def get_first_location_array (self):
        return self.get_first_location().toArray()

    def get_last_location (self):
        return self.get_fps_location(len(self.actions) - 1)

    def get_last_location_array (self):
        return self.get_last_location().toArray()

    def get_after_place_half_sec_fps (self):
        after_fps = []
        value = []

        placeFps, _, _ = self.get_last_place()

        for fps in range(placeFps + 1, placeFps + 16):
            after_fps.append(fps)
            value.append(self.actions[fps])

        return after_fps, value

    def get_before_place_half_sec_fps (self):
        before_fps = []
        value = []

        placeFps, _, _ = self.get_first_place()

        for fps in range(placeFps + 1, placeFps + 16):
            before_fps.append(fps)
            value.append(self.actions[fps])

        return before_fps, value

    def get_start_half_sec_fps (self):
        start_fps = []
        value = []

        for fps in range(0, 15):
            start_fps.append(fps)
            value.append(self.actions[fps])

        return start_fps, value

    def get_end_half_sec_fps (self):
        end_fps = []
        value = []

        for fps in range(len(self.actions) - 16, len(self.actions) - 1):
            end_fps.append(fps)
            value.append(self.actions[fps])

        return end_fps, value

# 僅作單一動作修正
class training_correct:
    dataset = []

    def __init__ (self, actions):
        self.dataset = training_data(actions)

    def correct_location (self, value):
        for fps, frame in enumerate(self.dataset.actions):
            location = (self.dataset.get_fps_location_array(fps)) + xyz(value).toArray()
            self.dataset.set_fps_location(fps, location)

            if (self.dataset.get_fps_block(fps) is not 0):
                block_location = (self.dataset.get_fps_block_location_array(fps)) + xyz(value).toArray()
                self.dataset.set_fps_block_location(fps, block_location)

        self.dataset.flush_actions()

    def merge_last_actions_from_start (self, last_actions):
        total_fps = len(last_actions)
        weghit_fps = 1 / total_fps
        last_actions = training_data(last_actions)

        for fps, frame in enumerate(last_actions.actions):
            last_biases, this_biases = total_fps - fps, fps
            last_weghit, this_weghit = last_biases * weghit_fps, this_biases * weghit_fps

            last_location = last_actions.get_fps_location_array(fps) * last_weghit
            this_location = self.dataset.get_fps_location_array(fps) * this_weghit
            new_location = last_location + this_location

            last_direction = last_actions.get_fps_direction_array(fps) * last_weghit
            this_direction = self.dataset.get_fps_direction_array(fps) * this_weghit
            new_direction = last_direction + this_direction

            self.dataset.set_fps_location(fps, new_location)
            self.dataset.set_fps_direction(fps, new_direction)

        self.dataset.flush_actions()

    # 表演性質動作，會需要依照開始到結束位置來做比例調整
    def correct_location_by_start_end (self):
        pass

# 做兩個動作的呼叫修正然後合併產出
class training_correct_merge:
    action_a, action_b, action_c = [], [], []

    # 合併執行性質動作到表演性質動作
    def merge_execute_start_demo_end (self):
        pass

    # 合併表演性質動作到執行性質動作
    def merge_demo_start_execute_end (self):
        pass

    # 合併兩個皆為表演性質的動作
    def merge_both_demo_action (self, demo_action):
        pass

    # 合併都是執行動作
    def merge_both_execute_action (self, execute_action):
        pass
