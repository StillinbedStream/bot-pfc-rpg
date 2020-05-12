from PFCBot.messages.message import Message


class BugDiscordCommunication(Message):
    def __init__(self, channel=None):
        self.content = "Il y a eu un bug, ce n'est pas possible d'atteindre le joueur 2. Contacte l'admin stp. Tu sais, le big boss."
        self.channel = channel

