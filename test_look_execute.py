import training_data as td
import helper as hp
import numpy as np
import time
import json
import os

class test_action:
    file_path = None
    look_test = hp.training_data(td.action_2_in_line_look_around_1)
    fps = 30

    def __init__ (self):
        for fps, action in enumerate(self.look_test.actions):
            self.file_path = os.path.expanduser("~Public") + os.sep + os.sep.join(["Documents", "execute", ("%d.txt" % (fps))])

            location = self.look_test.get_fps_location_array(fps)
            direction = self.look_test.get_fps_direction_array(fps)

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
