from PFCBot.messages.message import Message
import discord

# Fight messages

class AttackMySelf(Message):
    def __init__(self, channel=None):
        self.content = "Tu ne peux pas t'attaquer toi-même ! https://i.pinimg.com/originals/50/ab/ee/50abee00257155868ac43c7e9cb64bed.gif"
        self.channel = channel

class Equality(Message):
    def __init__(self, player1, player2, channel=None):
        self.content = f"[{player1.getNbReceivedFights()}] Il y a eu égalité avec **{player2.name}** ! Rejouez."
        self.channel = channel

class WinMessage(Message):
    def __init__(self, winner, looser, channel=None):
        self.content = f"[{winner.getNbReceivedFights()}] Vous avez vaincu **{looser.name}** !"
        self.channel = channel

class LooseMessage(Message):
    def __init__(self, winner, looser, channel=None):
        self.content = f"[{looser.getNbReceivedFights()}] Vous avez perdu contre le joueur {winner.name} !"
        self.channel = channel

class PlayerMadeChoice(Message):
    '''
        "[{player2.getNbReceivedFights()}] **{player1.name}** a fait son choix"
    '''
    def __init__(self, player1, player2, channel=None):
        self.content = f"[{player2.getNbReceivedFights()}] **{player1.name}** a fait son choix"
        self.channel = channel

class ActionReceived(Message):
    def __init__(self, player, channel=None):
        self.content = f"[{player.getNbReceivedFights()}] Nous avons bien reçu votre action"
        self.channel = channel

class AlreadyVote(Message):
    def __init__(self, channel=None):
        self.content = "Tu as déjà voté !"
        self.channel = channel

class AlreadyVotedAll(Message):
    def __init__(self, channel=None):
        self.content = "Tu as déjà voté pour tous les duels en cours !"
        self.channel = channel

class AlreadyEncountered(Message):
    def __init__(self, player2, minutes, secondes, channel=None):
        self.content = f"Le joueur {player2.name} a déjà été rencontré. Il vous reste {minutes} minutes {secondes} secondes avant de pouvoir l'attaquer."
        self.channel = channel

class FightCanceledByPlayer1(Message):
    def __init__(self, player, channel=None):
        self.content = f"Le combat avec {player.name} a été annulé."
        self.channel = channel

class FightCanceled(Message):
    def __init__(self, channel=None):
        self.content = "On a bien supprimé ton combat ! Retourne te battre moussaillon ! https://media.giphy.com/media/ihMKNwb2yPEbWJiAmn/giphy.gif"
        self.channel = channel

class SentInvite(Message):
    def __init__(self, player1, player2, channel=None):
        self.content = f"[{player1.getNbReceivedFights()}] {player2.name} a reçu l'invitation"
        self.channel = channel

class DoTheChoice(Message):
    def __init__(self, channel=None):
        self.content = "Choisis : pierre, feuille ou ciseaux"
        self.channel = channel

class YouAreAttacked(Message):
    def __init__(self, player1, player2, channel=None):
        self.content = f"[{player2.getNbReceivedFights()}] **{player1.name}** vous a défié"
        self.channel = channel


class DuelAlreadyFinished(Message):
    def __init__(self, channel=None):
        self.content = "Le duel est fini !"
        self.channel = channel


class FightsInit(Message):
    def __init__(self, channel=None):
        self.content = "Les combats sont bien réinitialisés !"
        self.channel = channel


class SignatureWinMessage(Message):
    def __init__(self, winner, looser, channel=None):
        self.embed = discord.Embed()
        self.embed.title=f"Le joueur {winner.name} vous a envoyé une signature car vous êts un looser"
        self.embed.description = f"{winner.signature}"
        if winner.signatureImage != "":
            self.embed.set_image(url=winner.signatureImage)
        self.channel = channel

class Provoc(Message):
    def __init__(self, player, provoc, provoc_image, channel = None):
        self.embed = discord.Embed()
        self.embed.title = f"{player.name} vous provoque : "
        self.embed.description=provoc
        if provoc_image != "":
            self.embed.set_image(url=provoc_image)
        self.channel = channel