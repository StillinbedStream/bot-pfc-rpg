
class channelUndefined(Exception):
    def __init__(self):
        super().__init__("Le channel n'a pas été défini")
