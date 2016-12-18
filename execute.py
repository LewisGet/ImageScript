import training_data as td

class taing_action:
    action_name = None
    last_actions = []
    action_training = []
    execute_action = []

    def __init__ (self, action_name, last_actions):
        self.action_name = action_name
        self.last_actions = last_actions

    def load_traing_action (self):
        self.action_training = getattr(td, self.action_name)

    def correct_action (self):
        pass
