from PFCBot.commands.converters import is_name

from PFCBot.messages.message import send_message
from PFCBot.messages.s0cattack import *
from PFCBot.messages.player import *
from PFCBot.messages.fights import *
from PFCBot.messages.discord_related import *
from PFCBot.messages.others import *
from PFCBot.messages.lists import *
from PFCBot.messages.coins import *
from PFCBot.messages.FallEllyss import *


class CommandArguments():

    def __init__(self):
        pass



class SpellFactory():
    '''
    '''

    def getSpell(self, name):
        # todo: gérer le moment où le spell n'est pas le bon
        self.spells = {
            "s0cattack": S0cattackSpell()
        }
        return self.spells[name]
    

class Spell():
    '''
    '''
    price = 0
    level = 0
    user = None

    def __init__(self):
        ''' 
        '''
        self.__gameManager = None
        self.__dataManager = None
        self.__arguments = None
        pass

    async def use(self, channel=None):
        '''
        '''
        self.user.coins -= self.price
        pass

    async def checkUsable(self, channel=None):
        '''
            Est-ce qu'on a assez de sous par exemple ? Le niveau suffisant ?
        '''
        # Est-ce qu'on a assez de coins ? 
        if self.user.coins < self.price:
            await send_message(NotEnoughCoins(self.price, channel))
            return False
        return True
        

    @property
    def arguments(self):
        return self.__arguments
    
    @arguments.setter
    def arguments(self, arguments: CommandArguments):
        self.__arguments = arguments

    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self, sender):
        self.__sender = sender

    @property
    def gameManager(self):
        return self.__game_manager
    
    @gameManager.setter
    def gameManager(self, game_manager):
        self.__game_manager = game_manager
    
    @property
    def dataManager(self):
        return self.__data_manager
    
    @dataManager.setter
    def dataManager(self, data_manager):
        self.__data_manager = data_manager
    

class S0cattackSpell(Spell):
    '''
        s0cattackSkill.arguments = S0cattackSkill.Arguments(args)
    '''
    class Arguments(CommandArguments):
        def __init__(self, name_player2: is_name):
            self.name_player2 = name_player2
    

    def __init__(self):
        '''

        '''
        self.level = 2
        self.price = 1

    
    async def use(self, channel=None):
        name_player2 = self.arguments.name_player2
        
        # Est-ce que le joueur 1 existe ?
        player1 = self.dataManager.getPlayerById(self.user.idPlayer)

        # Est-ce que le joueur 1 existe ?
        if player1 is None:
            return await send_message(PlayerNotRegistered(channel))

        # Chercher le joueur 2
        player2 = self.dataManager.getPlayerByName(name_player2)

        # Est-ce que le joueur 2 existe ?
        if player2 is None:
            return await send_message(Player2DoesNotExist(name_player2, channel))

        # On ajoute les tokens
        player1.sentTokens += 1
        player2.receivedTokens += 1
        
        # Créer le DM de Joueur 1
        c_player2 = None
        if self.gameManager.client is not None:
            c_player2 = self.gameManager.client.get_user(player2.idPlayer)
        
        # Créer le DM de Joueur 2
        c_player1 = None
        if self.gameManager.client is not None:
            c_player1 = self.gameManager.client.get_user(player1.idPlayer)

        # Vérifier que le score des joueurs ne puisse pas être négatif
        if player1.score < 0 or player2.score < 0:
            player1.sentTokens -= 1
            player2.receivedTokens -= 1
            await send_message(await TokenNotSentCauseNegativeScore().direct_message(c_player1))
        else:
            await send_message(await TokenSent(player2).direct_message(c_player1))
            await send_message(await TokenReceived(player1).direct_message(c_player2))
        
        self.dataManager.syncRanking()
        await super().use(channel)

