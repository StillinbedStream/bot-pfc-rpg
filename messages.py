
import discord
import exceptions

# La fonction pour envoyer des messages
async def send_message(message, channel=None):
    if message.channel is None:
        if channel is None:
            raise exceptions.channelUndefined()
        else:
            message.channel = channel
    await message.channel.send(message.content, embed=message.embed)

# Classe mère des messages
class Message(discord.Message):
    '''
        Cette classe permet d'encapsuler des informations pour 
        envoyer des messages à un joueur. On profite de la puissance
        que nous offre discord.Message.
    '''
    __content = ""
    __channel = None
    __embed = None

    def __init__(self):
        self.__content = ""
        self.__channel = None
        self.__embed = None
    
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @property
    def channel(self):
        return self.__channel
    
    @channel.setter
    def channel(self, channel):
        self.__channel = channel
    
    @property
    def embed(self):
        return self.__embed
    
    @embed.setter
    def embed(self, embed):
        self.__embed = embed
    
    async def direct_message(self, user):
        '''
            Méthode chainable qui permet de configurer le message pour 
            être envoyé en direct message
        '''
        if user.dm_channel is None:
            await user.create_dm()
        self.channel = user.dm_channel
        return self

# Classes filles à remplir une à une
class PlayerNotRegistered(Message):
    def __init__(self, channel=None):
        self.content = "Tu n'es pas enregistré. Utilise la commande !register. !help pour en savoir plus.\nhttps://media.giphy.com/media/XZ39zg4naZ1O8/giphy.gif"
        self.channel = channel

class Player2NotRegistered(Message):
    def __init__(self, channel=None):
        self.content = "Le joueur 2 n'existe pas dans notre base de données"
        self.channel = channel

class AttackMySelf(Message):
    def __init__(self, channel=None):
        self.content = "Tu ne peux pas t'attaquer toi-même ! https://i.pinimg.com/originals/50/ab/ee/50abee00257155868ac43c7e9cb64bed.gif"
        self.channel = channel

class PlayerPassif(Message):
    def __init__(self, channel=None):
        self.content = "Tu es en monde passif."
        self.channel = channel

class Player2Passif(Message):
    def __init__(self, channel=None):
        self.content = "Le joueur que tu as attaqué est en mode 'passif'."
        self.channel = channel

class PlayerAlreadyRegistered(Message):
    def __init__(self, player, channel=None):
        self.content = f"T'es déjà enregistré sous le nom de {player.name}, bouffon !"
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

class NameExists(Message):
    def __init__(self, name, channel=None):
        self.content = f"Le pseudo {name} est déjà pris, t'es mauvais jack !"
        self.channel = channel

class PlayerInFight(Message):
    def __init__(self, channel=None):
        self.content = "Tu es en combat !"
        self.channel = channel

class PlayerNotInFight(Message):
    def __init__(self, channel=None):
        self.content = "Tu n'es pas en combat !"
        self.channel = channel

class Player2InFight(Message):
    def __init__(self, player, channel=None):
        self.content = f"Le joueur {player.name} est déjà en combat !"
        self.channel = channel

class PlayerNotFound(Message):
    def __init__(self, name, channel=None):
        self.content = f"Le joueur {name} n'a pas été trouvé."
        self.channel = channel

class PlayerHasNotSentFight(Message):
    def __init__(self, channel=None):
        self.content = "Tu n'as pas déjà attaqué de joueurs."
        self.channel = channel

class Player2DoesNotExist(Message):
    def __init__(self, name, channel=None):
        self.content = f"Le joueur {name} n'existe pas"
        self.channel = channel

class AlreadyPassif(Message):
    def __init__(self, channel=None):
        self.content = "T'es déjà passif ! https://thumbs.gfycat.com/PoliteClearBlackfish-size_restricted.gif"
        self.channel = channel

class AlreadyActif(Message):
    def __init__(self, channel=None):
        self.content = "T'es déjà actif ! https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR5olQJ0iCPut7COcWGoAePC36usg_uE3O8xCYcnp03EPuFz4f9w&s"
        self.channel = channel

class AlreadySentFight(Message):
    def __init__(self, fight, channel=None):
        self.content = f"T'as déjà attaqué le joueur {fight.player2.name} !"
        self.channel = channel

class DuelAlreadyFinished(Message):
    def __init__(self, channel=None):
        self.content = "Le duel est fini !"
        self.channel = channel

class BugDiscordCommunication(Message):
    def __init__(self, channel=None):
        self.content = "Il y a eu un bug, ce n'est pas possible d'atteindre le joueur 2. Contacte l'admin stp. Tu sais, le big boss."
        self.channel = channel

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


# Register player
class RegisterDone(Message):
    def __init__(self, channel):
        self.content = "\n".join([
            "Enregistrement DONE. Welcome to the trigone ! Que la triforce soit avec toi !",
            "Dans un premier temps affiche la liste des joueurs actifs avec la commande : !show-actifs",
            "Tu peux ensuite attaquer qui tu veux avec la commande : !attack [pseudo]",
            "Pour ne plus subir d'attaques, utilises la commande : !passif"
        ])
        self.channel = channel


# Show stats
class MyStats(Message):
    def __init__(self, player, channel=None):
        self.embed = discord.Embed()
        self.embed.title = f"Vos stats {player.name}"

        actif_message = "actif" if player.actif else "passif"
        in_fight_message = "non" if player.sentFight is None else "oui"

        self.embed.add_field(name="actif", value=actif_message, inline=True)
        self.embed.add_field(name="en combat ?", value=in_fight_message, inline=True)
        self.embed.add_field(name="**score**", value=f"**{player.score}**", inline=True)

        self.embed.add_field(name="wins", value=f"{player.nbWin}", inline=True)
        self.embed.add_field(name="wins cons", value=f"{player.nbWinCons}", inline=True)
        self.embed.add_field(name="wins cons max", value=f"{player.nbWinConsMax}", inline=True)

        self.embed.add_field(name="looses", value=f"{player.nbLoose}", inline=True)
        self.embed.add_field(name="looses cons", value=f"{player.nbLooseCons}", inline=True)
        self.embed.add_field(name="looses cons max", value=f"{player.nbLooseConsMax}", inline=True)

        self.channel = channel

class PlayerStats(Message):
    def __init__(self, player, channel=None):
        actif_message = "actif" if player.actif else "passif"
        message = "\n".join([
            f"Statistiques de **{player.name}** : ",
            f"win : {player.nbWin}",
            f"loose : {player.nbLoose}",
            f"Wins consécutives MAX : {player.nbWinConsMax}",
            f"Looses consécutives MAX: {player.nbLooseConsMax}",
            f"score : {player.score}",
            f"état du compte : {actif_message}",
        ])
        self.content = message
        self.channel = channel

# Fight messages
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


# List commands
class ListPlayers(Message):
    def __init__(self, players, channel=None):
        self.channel = channel

        self.embed = discord.Embed()
        self.embed.title = f"Liste des joueurs"
        self.embed.description="!show-actifs pour lister les joueurs actifs"
        players_names = ""
        players_status = ""
        for player in players:
            players_names += player.name + "\n"
            if player.actif:
                players_status += ":v:\n"
            else:
                players_status += " :sleeping:\n"


        self.embed.add_field(name="name", value=players_names, inline=True)
        self.embed.add_field(name="statut", value=players_status, inline=True)
        self.channel = channel

class ListCurrentFights(Message):
    def __init__(self, fights, channel=None):
        message = "Liste des combats : \n"
        for fight in fights:
            message += f"{fight.player1.name} versus {fight.player2.name}\n"
        self.content = message
        self.channel = channel


# Passif or Actif
class BecomePassif(Message):
    def __init__(self, channel=None):
        self.content = "Tu es bien passé en mode passif ! Utilises la commande !actif pour redevenir attaquable. https://thumbs.gfycat.com/PoliteClearBlackfish-size_restricted.gif"
        self.channel = channel

class BecomeActif(Message):
    def __init__(self, channel=None):
        self.content = "Tu es bien passé en mode actif ! Utilises la commande !passif pour ne plus être attaqué. https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR5olQJ0iCPut7COcWGoAePC36usg_uE3O8xCYcnp03EPuFz4f9w&s"
        self.channel = channel

# signature 

class SignatureModified(Message):
    def __init__(self, channel=None):
        self.content = "Votre signature a bien été modifiée"
        self.channel = channel

class ShowSignature(Message):
    def __init__(self, signature, channel=None):
        self.content = f"Votre signature : \n{signature}"
        self.channel = channel

class SignatureWinMessage(Message):
    def __init__(self, winner, looser, channel=None):
        self.embed = discord.Embed()
        self.embed.title=f"Le joueur {winner.name} vous a envoyé une signature car vous êts un looser"
        self.embed.description = f"=> \n{winner.signature}"
        self.channel = channel


# Cancel
class FightCanceledByPlayer1(Message):
    def __init__(self, player, channel=None):
        self.content = f"Le combat avec {player.name} a été annulé."
        self.channel = channel

class FightCanceled(Message):
    def __init__(self, channel=None):
        self.content = "On a bien supprimé ton combat ! Retourne te battre moussaillon ! https://media.giphy.com/media/ihMKNwb2yPEbWJiAmn/giphy.gif"
        self.channel = channel

class Help(Message):
    def __init__(self, channel=None):
        self.content = "\n".join([
            "T'es nouveau, si tu veux jouer, fais ces commandes :",
            "`!register [pseudo]` : enregistre toi avec un pseudo",
            "`!players` : liste les joueurs",
            "`!attack [pseudo du joueur]` : attaque la personne ayant le pseudo fourni",
            "",
            "**Note pour jouer :** quand tu reçois une attaque, réponds par pierre, feuille ou ciseaux",
            "",
            "Commandes de base pour jouer : ",
            "`!help` : message d'aide avec la liste des commandes",
            "`!register [pseudo]` : s'enregistrer avec le pseudo donné",
            "`!attack [pseudo du joueur]` : attaquer le joueur avec le pseudo donné",
            "`!next-fights` : affiche la liste de nos combats en cours.",
            "`pierre`, `feuille`, ou `ciseaux` : donner son choix au prochain combat",
            "",
            "",
            "Liste des commandes en plus :",
            "`!help` : message d'aide avec la liste des commandes",
            "`!players` : liste les noms des joueurs",
            "`!show-actifs` : Liste tous les joueurs actifs",
            "`!mystats` : voir mes statistiques",
            "`!current-fights` : liste les combats en cours",
            "`!ranking` : liste le classement des joueurs avec leurs points",
            "`!actif` : vous met en mode actif, vous pouvez être attaqué et attaquer à nouveau",
            "`!passif` : vous met en mode passif, vous ne pouvez plus attaquer et être attaqué",
            "`!cancel` : supprime le combat en cours, n'en abuse pas s'il te plaît.",
            "",
            "PS : J'ai soif de boire https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHHzo3NXvZN2D63gbYVvpzWJ9lyk4gC6v3mheuGX-XeOc-FRe5&s"
        ])
        self.channel = channel

class Ranking(Message):
    def __init__(self, ranking, channel=None):
        message = "Le classement : \n"
        for i, player in enumerate(ranking):
            message += f"({i}) {player.name} avec {player.score} pts\n"
        self.content = message
        self.channel = channel

class NextFights(Message):
    def __init__(self, player, channel):
        
        self.embed = discord.Embed()
        self.embed.title = f"Mes prochains combats"
        self.embed.description = ""
        
        message = "Combat envoyé : "
        next_fight_pointed = False
        if player.sentFight is None:
            message += "Aucun\n"
        else:
            message += f"**{player.sentFight.player2.name}** "
            if player.sentFight.alreadyVote(player):
                message += ":ok_hand:"
            elif not next_fight_pointed:
                message += ":point_left:"
                next_fight_pointed = True
            message += "\n"
                
        
        message += "\nCombats reçus :\n"
        if len(player.receivedFights) == 0:
            message += "Il n'y a pas de combats"
        for i, fight in enumerate(player.receivedFights):
            message += f"[{i}] {fight.player1.name} "
            if fight.alreadyVote(player):
                message += ":ok_hand:"
            elif not next_fight_pointed:
                message += ":point_left:"
                next_fight_pointed = True
            message += "\n"

        self.embed.description += message
        self.channel = channel

class ShowActifs(Message):
    def __init__(self, players, guild, channel):
        self.embed = discord.Embed()
        self.embed.title = f"Liste des actifs"
        self.embed.description = ""
        for player in players:
            c_player = guild.get_member(player.idPlayer)
            if player.actif and c_player.status == discord.Status.online:
                self.embed.add_field(name="name", value=player.name, inline=True)
                self.embed.add_field(name="statut", value=f"{player.score} pts", inline=True)
                self.embed.add_field(name="\u200b", value="\u200b", inline=True)
                #self.embed.description += f"{player.name} avec  :v:\n"
        
        self.channel = channel

class Provoc(Message):
    def __init__(self, player, provoc, channel = None):
        self.embed = discord.Embed()
        self.embed.title = f"{player.name} vous provoque : "
        self.embed.description=provoc
        self.channel = channel

# Admin messages
class NameChanged(Message):
    def __init__(self, name, new_name, channel=None):
        self.content = f"Le nom du joueur {name} a bien été remplacé par {new_name}"
        self.channel = channel

class FightsInit(Message):
    def __init__(self, channel=None):
        self.content = "Les combats sont bien réinitialisés !"
        self.channel = channel

