

class ErrorWithCustomModel(Exception):
    def __init__(self, name, error):

        self.message= 'Error loading {} module (USER DEFINED). Error message: {}'.format(name, error)
        # Calling super
        super().__init__(self.message)
    def __str__(self):
        return self.message


class InvalidModelException(Exception):
    def __init__(self, message = 'Invalid model type entered. See config files to add models. See Logs/CustomModels.log for details'):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message


