class CustomException(Exception):

    def __init__(self, msg):
        super().__init__()
        self.msg = msg
