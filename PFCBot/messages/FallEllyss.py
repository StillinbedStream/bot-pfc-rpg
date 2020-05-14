
from PFCBot.messages.message import Message

class FallEllyssDone(Message):
    def __init__(self, sender, receiver, channel=None):
        # envoyer le message disant que l'on a bien envoyé un token au joueur "receiver"
        self.content = f"Vous avez bien FallEllyssé le joueur {receiver.name} <:sip:710591429151555725>"
        self.channel = channel

class FallEllyssed(Message):
    def __init__(self, sender, receiver, channel=None):
        # envoyer le message disant que l'on a bien envoyé un token au joueur "receiver"
        self.content = f"Le joueur {sender.name} vous a FallEllyssé https://cdn.discordapp.com/attachments/354026678848192512/710587112294056006/fall.gif"
        self.channel = channel

class FallEllyssNotEnoughWin(Message):
    def __init__(self, nbFights, receiver, channel=None):
        self.content = f"Le joueur {receiver.name} n'a pas assez de victoires, il lui en faut au moins {nbFights}."
        self.channel = channel

    


