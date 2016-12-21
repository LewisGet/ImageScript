import training_data as td
import helper as hp
import numpy as np
import time
import json
import os

class test_action:
    file_path = None
    look_around = hp.training_correct(td.action_2_in_line_look_around_1)
    look_down = hp.training_correct(td.action_2_look_down_put_one_block_2)
    action_at = hp.xyz([5, 0, 5])
    target_execute = hp.training_data([])
    fps = 30

    def __init__ (self):
        look_around_last_location = self.look_around.dataset.get_last_location_array()
        _, _, look_down_target_location = self.look_down.dataset.get_last_place()

        # to do: 人類移動大部分會已格子中央為準，但依照 target 會變成開始點 0 為準
        look_down_target_location = look_down_target_location + np.array([0.5, 0.5, 0.5])

        two_action_diff_location = look_down_target_location - look_around_last_location
        look_around_correct_location = self.action_at.toArray() + two_action_diff_location
        look_down_correct_location = self.action_at.toArray()

        self.look_around.correct_location(look_around_correct_location)
        self.look_down.correct_location(look_down_correct_location)

        _, to_merge = self.look_around.dataset.get_end_half_sec_fps()
        self.look_down.merge_last_actions_from_start(to_merge)

        for fps in range(0, len(self.look_around.dataset.actions) - 16):
            self.target_execute.actions.append(self.look_around.dataset.actions[fps])

        for action in self.look_down.dataset.actions:
            self.target_execute.actions.append(action)

        self.target_execute.flush_actions()

        for fps, action in enumerate(self.target_execute.actions):
            self.file_path = os.path.expanduser("~Public") + os.sep + os.sep.join(["Documents", "execute", ("%d.txt" % (fps))])

            location = self.target_execute.get_fps_location_array(fps)
            direction = self.target_execute.get_fps_direction_array(fps)

            execute_json = self.get_execute_content_json(location, direction)
            self.write_file(execute_json)

    def read_file (self):
        logs = open(self.file_path, "r")
        value = []

        for line in logs:
            lineContent = line.rstrip()

            if (lineContent):
                value.append(lineContent)

        return "".join(value)

    def read_file_json (self):
        return json.loads(self.read_file())

    def write_file (self, content):
        text_file = open(self.file_path, "w+")
        text_file.write(content)
        text_file.close()

    def get_execute_content (self, location, direction):
        return {
            "location": hp.xyz(location).toDict(),
            "direction": hp.xyz(direction).toDict(),
            "message": "wait"
        }

    def get_execute_content_json(self, location, direction):
        return json.dumps(self.get_execute_content(location, direction))

test = test_action()
