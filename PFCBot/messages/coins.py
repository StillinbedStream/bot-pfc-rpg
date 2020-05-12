from PFCBot.messages.message import Message

class NotEnoughCoins(Message):
    def __init__(self, nb_needed, channel=None):
        self.content = f"Tu n'as pas assez de coins ! Il t'en faut {nb_needed} !"
        self.channel = channel