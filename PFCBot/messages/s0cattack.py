from PFCBot.messages.message import Message

class TokenReceived(Message):
    def __init__(self, sender, channel=None):
        # envoyer le message disant que l'on a reçu un token du joueur "sender"
        self.content=f"Vous avez reçu un token de {sender.name}"
        self.channel = channel

class TokenSent(Message):
    def __init__(self, receiver, channel=None):
        # envoyer le message disant que l'on a bien envoyé un token au joueur "receiver"
        self.content=f"Le token a bien été envoyé au joueur {receiver.name}"
        self.channel = channel

class TokenNotSentCauseNegativeScore(Message):
    def __init__(self, channel=None):
        # envoyer le message disant que l'on a bien envoyé un token au joueur "receiver"
        self.content=f"Le token n'a pas été envoyé parce que l'un des deux joueurs aurait un score trop faible (<0)"
        self.channel = channel

