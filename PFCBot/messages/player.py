from PFCBot.messages.message import Message
import discord

class PlayerNotRegistered(Message):
    def __init__(self, channel=None):
        self.content = "Tu n'es pas enregistré. Utilise la commande !register. !help pour en savoir plus.\nhttps://media.giphy.com/media/XZ39zg4naZ1O8/giphy.gif"
        self.channel = channel

class Player2NotRegistered(Message):
    def __init__(self, channel=None):
        self.content = "Le joueur 2 n'existe pas dans notre base de données"
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

class PlayerHasNotSentFight(Message):
    def __init__(self, channel=None):
        self.content = "Tu n'as pas déjà attaqué de joueurs."
        self.channel = channel

class Player2DoesNotExist(Message):
    def __init__(self, name, channel=None):
        self.content = f"Le joueur {name} n'existe pas"
        self.channel = channel



class AttackMySelf(Message):
    def __init__(self, channel=None):
        self.content = "Tu ne peux pas t'attaquer toi-même ! https://i.pinimg.com/originals/50/ab/ee/50abee00257155868ac43c7e9cb64bed.gif"
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

class RegisterDone(Message):
    def __init__(self, channel):
        self.content = "\n".join([
            "Enregistrement DONE. Welcome to the trigone ! Que la triforce soit avec toi !",
            "Dans un premier temps affiche la liste des joueurs actifs avec la commande : !show-actifs",
            "Tu peux ensuite attaquer qui tu veux avec la commande : !attack [pseudo]",
            "Pour ne plus subir d'attaques, utilises la commande : !passif"
        ])
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

class SignatureModified(Message):
    def __init__(self, channel=None):
        self.content = "Votre signature a bien été modifiée"
        self.channel = channel

class ShowSignature(Message):
    def __init__(self, player, channel=None):
        self.embed = discord.Embed()
        self.embed.title=f"Votre signature"
        self.embed.description = f"{player.signature}"
        
        if player.signatureImage != "":
            self.embed.set_image(url=player.signatureImage)
        
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

        self.embed.add_field(name="papoules", value=f"{player.coins} :chicken:", inline=True)

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


class NameChanged(Message):
    def __init__(self, name, new_name, channel=None):
        self.content = f"Le nom du joueur {name} a bien été remplacé par {new_name}"
        self.channel = channel

