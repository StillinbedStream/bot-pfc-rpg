

class Message():
    '''
        Une message qui est renvoyé à l'utilisateur.
    '''

    def __init__(self, channel, content):
        self.__channel = channel
        self.__content = content
    
    @property
    def channel(self):
        return self.__channel
    
    @property
    def content(self):
        return self.__content

# Classe mère des exceptions à renvoyer à l'utilisateur
class ExceptionToUser(Exception):
    '''
        Une classe qui gère les exceptions qui sont envoyées à des utilisateurs.
    '''

    def __init__(self, string_output, message_to_user):
        self.__string_output = string_output
        self.__message_to_user = message_to_user

    @property
    def stringOutput(self):
        return self.__string_output
    
    @stringOutput.setter
    def stringOutput(self, string_output):
        self.__string_output = string_output

    @property
    def messageToUser(self):
        return self.__message_to_user

    @messageToUser.setter
    def messageToUser(self, message_to_user):
        self.__message_to_user = message_to_user
    

# Classes filles à remplir une à une
class PlayerNotRegistered(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur n'est pas enregistré."
        self.messageToUser = Message(None, "Tu n'es pas enregistré. Utilise la commande !register. !help pour en savoir plus.\nhttps://media.giphy.com/media/XZ39zg4naZ1O8/giphy.gif")

class Player2NotRegistered(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur 2 n'existe pas dans notre base de données"
        self.messageToUser = Message(None, "Le joueur 2 n'existe pas dans notre base de données")

class AttackMySelf(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur ne peut pas s'attaquer soi-même"
        self.messageToUser = Message(None, "Tu ne peux pas t'attaquer toi-même ! https://i.pinimg.com/originals/50/ab/ee/50abee00257155868ac43c7e9cb64bed.gif")

class PlayerPassif(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur est en mode passif et ne peut pas attaquer."
        self.messageToUser = Message(None, "Tu es en monde passif.")

class Player2Passif(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur 2 est en mode passif et ne peut pas être attaqué."
        self.messageToUser = Message(None, "Le joueur que tu as attaqué est en mode 'passif'.")

class PlayerAlreadyRegistered(ExceptionToUser):
    def __init__(self, player):
        self.stringOutput = "Le joueur est déjà enregistré"
        self.messageToUser = Message(None, "T'es déjà enregistré sous le nom de {player.name}, bouffon !")

class NameExists(ExceptionToUser):
    def __init__(self, name):
        self.stringOutput = f"Le pseudo {name} est déjà pris."
        self.messageToUser = Message(None, f"Le pseudo {name} est déjà pris, t'es mauvais jack !")

class PlayerInFight(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur est en combat"
        self.messageToUser = Message(None, "Tu es en combat !")

class PlayerNotInFight(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur n'est pas en combat"
        self.messageToUser = Message(None, "Tu n'es pas en combat !")

class Player2InFight(ExceptionToUser):
    def __init__(self, player):
        self.stringOutput = f"Le joueur 2 {player.name} est en combat"
        self.messageToUser = Message(None, f"Le joueur {player.name} est déjà en combat !")

class PlayerNotFound(ExceptionToUser):
    def __init__(self, name):
        self.stringOutput = "Le joueur {name} n'a pas été trouvé."
        self.messageToUser = Message(None, "Le joueur {name} n'a pas été trouvé.")


class AlreadyVote(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur a déjà voté"
        self.messageToUser = Message(None, "Tu as déjà voté !")

class AlreadyPassif(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur est déjà en mode passif."
        self.messageToUser = Message(None, "T'es déjà passif ! https://thumbs.gfycat.com/PoliteClearBlackfish-size_restricted.gif")

class AlreadyActif(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le joueur est déjà en mode actif."
        self.messageToUser = Message(None, "T'es déjà actif ! https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR5olQJ0iCPut7COcWGoAePC36usg_uE3O8xCYcnp03EPuFz4f9w&s")

class DuelAlreadyFinished(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Le duel est fini !"
        self.messageToUser = Message(None, "Le duel est fini !")


class BugDiscordCommunication(ExceptionToUser):
    def __init__(self):
        self.stringOutput = "Il y a eu un bug de communication, ce n'est pas possible d'atteindre le joueur 2."
        self.messageToUser = Message(None, "Il y a eu un bug, ce n'est pas possible d'atteindre le joueur 2. Contacte l'admin stp. Tu sais, le big boss.")

