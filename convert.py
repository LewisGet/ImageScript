class text_to_python:
    logs_file, output_file, action = None, None, None

    def __init__ (self, logs_file, output, action):
        self.logs_file = logs_file
        self.output_file = output
        self.action = action

    def read_file (self):
        logs = open(self.logs_file, "r")
        value = []

        for line in logs:
            lineContent = line.rstrip()

            if (lineContent):
                value.append(lineContent)

        return value

    def write_file (self, content):
        text_file = open(self.output_file, "w")
        text_file.write(content)
        text_file.close()

    def file_append (self, content):
        text_file = open(self.output_file, "a")
        text_file.write(content + "\r\n")
        text_file.close()

    def logs_variable_init (self):
        return self.action + " = []"

    def logs_line_to_variable (self, contnet):
        return self.action + ".append(" + str(contnet) + ")"

    def save_variable (self):
        logs = self.read_file()

        code = self.logs_variable_init()
        self.file_append(code)

        for line in logs:
            code = self.logs_line_to_variable(line)
            self.file_append(code)

actions = [
    'in_line_look_around',
    'in_line_put_next',
    'in_line_put_next_have_mistake_with_fixed',
    'look_down_put_one_block',
    'look_down_put_one_block_have_mistake_with_fixed'
]

action_look_at = [2, 4, 6, 8]

action_number = [1, 2, 3]

save_file = "taring_data.py"

for dir_name in action_look_at:
    for file_prefix in actions:
        for file_last in action_number:
            action_name = "action_" + str(dir_name) + "_" + file_prefix + "_" + str(file_last)
            logs_file = "./logs/" + str(dir_name) + "/" + file_prefix + "_" + str(file_last) + ".txt"

            execute = text_to_python(logs_file, save_file, action_name)

            try:
                execute.save_variable()
            except Exception as e:
                print (e)
