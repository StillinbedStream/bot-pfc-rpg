from PFCBot.messages.message import Message
import discord

# Fight messages

class AttackMySelf(Message):
    def __init__(self, channel=None):
        self.content = "Tu ne peux pas t'attaquer toi-même ! https://i.pinimg.com/originals/50/ab/ee/50abee00257155868ac43c7e9cb64bed.gif"
        self.channel = channel

class Equality(Message):
    def __init__(self, player1, player2, message_player, channel=None):
        #Todo: Ajouter le fight pour pouvoir ajouer des liens vers les messages des players.
        self.embed = discord.Embed()
        self.embed.title = f"Egalité avec {player2.name}"
        self.embed.description = f"[[lien]({message_player.jump_url})] Il y a eu égalité avec **{player2.name}** ! Rejouez."

class WinMessage(Message):
    def __init__(self, winner, looser, bet=0, channel=None):
        bet_message = ""
        if bet > 0:
            bet_message=f"\nVous avez gagné {bet} :chicken: de l'autre joueur"
        self.content = f"[{winner.getNbReceivedFights()}] Vous avez vaincu **{looser.name}** !{bet_message}"
        self.channel = channel

class LooseMessage(Message):
    def __init__(self, winner, looser, bet=0, channel=None):
        bet_message = ""
        if bet > 0:
            bet_message=f"\n{bet} :chicken: de vos papoules donné(s) à l'autre joueur."
        self.content = f"[{looser.getNbReceivedFights()}] Vous avez perdu contre le joueur {winner.name} !{bet_message}"
        self.channel = channel

class PlayerMadeChoice(Message):
    '''
        "[{player2.getNbReceivedFights()}] **{player1.name}** a fait son choix"
    '''
    def __init__(self, player1, player2, message_player, channel=None):
        self.embed = discord.Embed()
        self.embed.title = "Un joueur vous a répondu"
        self.embed.description = f"[[lien]]({message_player.jump_url}) **{player1.name}** a fait son choix"
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
    def __init__(self, message_player, channel=None):
        self.embed = discord.Embed()
        self.embed.title = f"Annulation du combat"
        self.embed.description = f"[[lien]]({message_player.jump_url}) On a bien supprimé ton combat ! Retourne te battre moussaillon !"
        self.embed.set_image(url="https://media.giphy.com/media/ihMKNwb2yPEbWJiAmn/giphy.gif")
        self.channel = channel

class SentInvite(Message):
    def __init__(self, fight, channel=None):
        player1 = fight.player1
        player2 = fight.player2
        
        bet_message = ""
        if fight.bet > 0:
            bet_message = f"{fight.bet} :chicken: en jeu !\n"

        self.embed = discord.Embed()
        self.embed.title = f"Duel envoyé à {player2.name}"
        self.embed.description = f"Vous avez envoyé un duel à {player2.name}.\n {bet_message}\nAjoute une réaction à ce message pour répondre : \n ✊ \:fist\: \n ✋ \:raised_hand\: \n ✌️ \:v\: \n \n Ou envoie moi un DM :\n pierre (p), feuille (f), ou ciseaux (c)"
        self.channel = channel

class DoTheChoice(Message):
    def __init__(self, channel=None):
        self.content = "Choisis : pierre, feuille ou ciseaux"
        self.channel = channel

class YouAreAttacked(Message):
    def __init__(self, fight, channel=None):
        player1 = fight.player1
        player2 = fight.player2
        bet_message = ""
        if fight.bet > 0:
            bet_message = f"{fight.bet} :chicken: en jeu !\n"
        self.embed = discord.Embed()
        self.embed.title = f"{player1.name} vous a défié"
        self.embed.description = f"{player1.name} vous a défié.\n{bet_message}\nPour répondre :\nAjoute une réaction à ce message pour répondre : \n ✊ \:fist\: \n ✋ \:raised_hand\: \n ✌️ \:v\: \n \n Ou envoie moi un DM :\n pierre (p), feuille (f), ou ciseaux (c)"
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
        self.embed.title=f"Le joueur {winner.name} vous a envoyé une signature car vous êtes un looser"
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