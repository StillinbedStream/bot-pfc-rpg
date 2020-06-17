from PFCBot.messages.message import Message

class NotEnoughCoins(Message):
    def __init__(self, player, nb_needed, channel=None):
        self.content = f"Le joueur {player.name} n'a pas assez de coins. Il lui reste {player.coins} papoules, et il lui en faut {nb_needed} !"
        self.channel = channel

class AddCoinsMessage(Message):
    def __init__(self, player, nb_add, channel=None):
        self.content = f"Tu as bien ajouté des {nb_add} papoules au joueur {player.name} !"
        self.channel = channel
    
class IncreasedCoins(Message):
    def __init__(self, receiver, nb_add, channel=None):
        self.content = f"Le tout puissant t'a ajouté {nb_add} papoules ! Tu en as maintenant {receiver.coins}."
        self.channel = channel
    
