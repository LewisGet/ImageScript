import training_data as td
import helper as hp
import numpy as np

class training_action:
    action_name = None
    correct_fps = 15
    correct_target = "place"
    correct_target_location = [0] * 3
    last_actions = []
    action_training = []
    execute_action = []

    def __init__ (self, action_name, last_actions, action_location):
        self.action_name = action_name
        self.last_actions = last_actions
        self.correct_target_location = action_location

    def load_traing_action (self):
        self.action_training = getattr(td, self.action_name)

    def correct_merge_last_actions (self):
        pass

    def correct_location_by_target_location (self):
        target_location = hp.xyz(self.get_training_target_location()).toArray()
        correct_target_location = (target_location * -1) + hp.xyz(self.correct_target_location).toArray()

        for fps, frames in enumerate(self.action_training):
            location = hp.xyz(frames['location']).toArray()
            location + correct_target_location
            self.action_training[fps]['location'] = location

    def get_training_target_location (self):
        for frames in self.action_training:
            if frames['block'] is self.correct_target:
                return frames['blockLocation']
