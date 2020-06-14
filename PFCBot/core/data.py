# TODO: Gérer la synchronisation du classement.
from typing import List, Dict

import pickle
import exceptions
import copy
import json
from datetime import datetime
from datetime import timedelta 
from copy import deepcopy

from PFCBot.messages.message import send_message
from PFCBot.messages.player import *
import PFCBot.core.engine
from PFCBot.core.wall import WallOfPFC


TIME_DELTA_PLAYER_ENCOUNTERED = timedelta(seconds=30)
# -- Entities
class Entity:

    def __init__(self):
        pass

    def hydrate(self, d):
        '''
            d est le dictionnaire donné dans lequel il y a les infos qu'on souhaite rentrer.
        '''
        for key, value in d.items():
            if key in self.__dict__:
                self.__dict__[key] = value
        return self
    
    def get_dict_json(self):
        '''
            d is the returned dictionary with all value to save into a json file.
        '''
        d = {}
        black_list_keys = [
            "_" + type(self).__name__ + "__dataManager",
            "_Player__last_players_encountered"
        ]

        for key, value in self.__dict__.items():
            if not key in black_list_keys:
                d[key] = value
        
        return d

class Player(Entity):
    def __init__(self, dataManager):
        self.__dataManager = dataManager
        self.__name = ""
        self.__id_player = ""
        self.__sent_fight = None
        self.__received_fights = []

        self.__nb_win = 0
        self.__nb_win_cons = 0
        self.__nb_win_cons_max = 0

        self.__nb_loose = 0
        self.__nb_loose_cons = 0
        self.__nb_loose_cons_max = 0

        self.__received_tokens = 0
        self.__sent_tokens = 0
        self.__actif = True

        self.__last_players_encountered = []
        self.__coins = 0

        self.__signature = ""
        self.__signature_image = ""
        self.__mobile = False
        
        
    
    def reset_fights(self):
        self.__sent_fight = None
        self.__received_fights = []
    
    # name
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    # displayed name
    @property
    def displayedName(self):
        add_name = ""

        if len(self.__dataManager.ranking) > 3:
            # Rank Emoji
            if self.__dataManager.ranking[0] == self:
                add_name += ":first_place:"
            elif self.__dataManager.ranking[1] == self:
                add_name += ":second_place:"
            elif self.__dataManager.ranking[2] == self:
                add_name += ":third_place:"
            
        # Other emojis ?
        return add_name + self.name

    # idPlayer
    @property
    def idPlayer(self):
        return self.__id_player
    
    @idPlayer.setter
    def idPlayer(self, id_player):
        self.__id_player = id_player
    
    # nbWin
    @property
    def nbWin(self):
        return self.__nb_win
    
    @nbWin.setter
    def nbWin(self, nb_win):
        self.__nb_win = nb_win
    

    # nbWinCons
    @property
    def nbWinCons(self):
        return self.__nb_win_cons
    
    @nbWinCons.setter
    def nbWinCons(self, nb_win_cons):
        self.__nb_win_cons = nb_win_cons
    

    # nbWinConsMax
    @property
    def nbWinConsMax(self):
        return self.__nb_win_cons_max
    
    @nbWinConsMax.setter
    def nbWinConsMax(self, nb_win_cons_max):
        self.__nb_win_cons_max = nb_win_cons_max


    # nbLoose
    @property
    def nbLoose(self):
        return self.__nb_loose
    
    @nbLoose.setter
    def nbLoose(self, nb_loose):
        self.__nb_loose = nb_loose


    # nbLooseCons
    @property
    def nbLooseCons(self):
        return self.__nb_loose_cons

    @nbLooseCons.setter
    def nbLooseCons(self, nb_loose_cons):
        self.__nb_loose_cons = nb_loose_cons
    

    # nbLooseConsMax
    @property
    def nbLooseConsMax(self):
        return self.__nb_loose_cons_max
    
    @nbLooseConsMax.setter
    def nbLooseConsMax(self, nb_loose_cons_max):
        self.__nb_loose_cons_max = nb_loose_cons_max
    

    # actif
    @property
    def actif(self):
        return self.__actif
    
    @actif.setter
    def actif(self, actif):
        self.__actif = actif
    

    # score
    @property
    def score(self):
        return PFCBot.core.engine.compute_score_player(self)
    
    # exp
    @property
    def exp(self):
        return self.score
    
    def addReceivedFight(self, fight):
        if self.hasAlreadyReceivedFight(fight):
            return False
        self.__received_fights.append(fight.idFight)       
        return True
    
    def hasAlreadyReceivedFight(self, fight):
        for f in self.receivedFights:
            if fight.idFight == f.idFight:
                return True
        return False
        
    def removeReceivedFight(self, fight):
        '''
            Permet de supprimer un combat 
            que le joueur a reçu.
        '''
        for i, f in enumerate(self.receivedFights):
            if fight == f:
                self.__received_fights.pop(i)
                return True
        return False

    def getNbReceivedFights(self):
        return len(self.receivedFights)
    
    @property
    def sentFight(self):
        return self.__dataManager.getFightById(self.__sent_fight)
    
    @sentFight.setter
    def sentFight(self, fight):
        if fight is None:
            self.__sent_fight = None
        else:
            self.__sent_fight = fight.idFight
    
    @property
    def receivedFights(self):
        return [self.__dataManager.getFightById(id_fight) for id_fight in self.__received_fights]


    @property
    def receivedFightsIds(self):
        return self.__received_fights
    

    @property
    def receivedTokens(self):
        return self.__received_tokens
    
    

    @receivedTokens.setter
    def receivedTokens(self, received_tokens):
        self.__received_tokens = received_tokens

    @property
    def sentTokens(self):
        return self.__sent_tokens
    
    @sentTokens.setter
    def sentTokens(self, sent_tokens):
        self.__sent_tokens = sent_tokens
    
    def getCurrentReceivedFight(self):
        for fight in self.receivedFights:
            if not fight.alreadyVote(self):
                return fight
        return None

    def initFights(self):
        '''
        '''
        self.sentFight = None
        self.__received_fights = []

        # if self.sentFight is not None:
        #     self.sentFight.cancel = True
        #     self.sentFight = None
        
        # # Cancel les received fights
        # for fight in self.receivedFights:
        #     fight.cancel = True
        
        # self.__received_fights = []
    
    @property
    def signature(self):
        return self.__signature
    
    @signature.setter
    def signature(self, signature):
        self.__signature = signature

    @property
    def signatureImage(self):
        return self.__signature_image

    @signatureImage.setter
    def signatureImage(self, signature_image):
        self.__signature_image = signature_image

    def addPlayerEncountered(self, player):
        if not self.playerAlreadyEncountered(player):
            self.__last_players_encountered.append([player, datetime.now()])

    def playerAlreadyEncountered(self, player):   
        for informations in self.__last_players_encountered:
            p = informations[0]
            dt = deepcopy(informations[1])
            dt_futur = dt + TIME_DELTA_PLAYER_ENCOUNTERED

            if p is player:
                return dt_futur - datetime.now()
        return None

    def synchroniseTimePlayerEncountered(self):
        for i, information in enumerate(reversed(self.__last_players_encountered)):
            dt = deepcopy(information[1])
            dt = dt + TIME_DELTA_PLAYER_ENCOUNTERED
            # Si le temps est dépassé
            if dt < datetime.now():
                del self.__last_players_encountered[0:len(self.__last_players_encountered) - i]
                return

    @property
    def coins(self):
        return self.__coins
    
    @coins.setter
    def coins(self, coins):
        self.__coins = coins

    @property
    def mobile(self):
        return self.__mobile
    
    @mobile.setter
    def mobile(self, mobile):
        self.__mobile = mobile
    
    @property
    def rank(self):
        for i, player in enumerate(self.__dataManager.ranking):
            if player == self:
                return i
        return -1
    
class Fight(Entity):
    def __init__(self, id_fight, player1, player2, dataManager):
        self.__dataManager = dataManager

        self.__id_fight = id_fight
        self.__id_player1 = None if player1 == None else player1.idPlayer
        self.__id_player2 = None if player2 == None else player2.idPlayer
        
        self.__id_winner = None
        self.__action_player1 = None
        self.__action_player2 = None
        self.__cancel = False

        self.__id_message_player1 = None
        self.__id_message_player2 = None

        if player1 is not None:
            player1.sentFight = self
        if player2 is not None:
            player2.addReceivedFight(self)
    
    # idFight
    @property
    def idFight(self):
        return self.__id_fight
    
    @idFight.setter
    def idFight(self, id_fight):
        self.__id_fight = id_fight
    
    # player1
    @property    
    def player1(self):
        return self.__dataManager.getPlayerById(self.__id_player1)
    
    @player1.setter
    def player1(self, player1):
        if player1 is None:
            self.__id_player1 = None
        else:
            self.__id_player1 = player1.idPlayer

    # player2
    @property
    def player2(self):
        return self.__dataManager.getPlayerById(self.__id_player2)
    
    @player2.setter
    def player2(self, player2):
        if player2 is None:
            self.__id_player2 = None
        else:
            self.__id_player2 = player2.idPlayer
    
    # winner
    @property
    def winner(self):
        return self.__dataManager.getPlayerById(self.__id_winner)
    
    @winner.setter
    def winner(self, winner):
        self.__id_winner = winner.idPlayer
    
    @property
    def looser(self):
        if self.winner is None:
            return None
        if self.player1.idPlayer == self.winner.idPlayer:
            return self.player2
        else:
            return self.player1
    
    # actionPlayer1
    @property
    def actionPlayer1(self):
        return self.__action_player1
    
    @actionPlayer1.setter
    def actionPlayer1(self, action_player1):
        self.__action_player1 = action_player1
    
    # actionPlayer2
    @property
    def actionPlayer2(self):
        return self.__action_player2
    
    @actionPlayer2.setter
    def actionPlayer2(self, action_player2):
        self.__action_player2 = action_player2

    # cancel
    @property
    def cancel(self):
        return self.__cancel
    
    @cancel.setter
    def cancel(self, cancel):
        self.__cancel = cancel
        self.player1.inFight = False
        self.player2.inFight = False

    def isInvolved(self, player):
        '''
            Vérifie si le joueur donné est impliqué dans le combat 
            même si le combat est fini ou cancel.
        '''
        if self.player1.idPlayer == player.idPlayer or self.player2.idPlayer == player.idPlayer:
            return True
        return False

    @property
    async def messagePlayer1(self):
        if self.__dataManager.client.get_user(self.player1.idPlayer).dm_channel is None:
            await self.__dataManager.client.get_user(self.player1.idPlayer).create_dm()
        if self.__id_message_player1 is None:
            return None
        return await self.__dataManager.client.get_user(self.player1.idPlayer).dm_channel.fetch_message(self.__id_message_player1)
    

    async def getMessageOfPlayer(self, player: Player):
        '''
        Return fight message of given player
        or return None
        '''
        if self.player1 is player:
            return await self.messagePlayer1
        if self.player2 is player:
            return await self.messagePlayer2
        return None
    
    @messagePlayer1.setter
    def messagePlayer1(self, message):
        self.__id_message_player1 = message.id
    
    @property
    def idMessagePlayer1(self):
        return self.__id_message_player1

    @property
    async def messagePlayer2(self):
        if self.__dataManager.client.get_user(self.player2.idPlayer).dm_channel is None:
            await self.__dataManager.client.get_user(self.player2.idPlayer).create_dm()
        if self.__id_message_player2 is None:
            return None
        return await self.__dataManager.client.get_user(self.player2.idPlayer).dm_channel.fetch_message(self.__id_message_player2)

    @messagePlayer2.setter
    def messagePlayer2(self, message):
        self.__id_message_player2 = message.id
    
    @property
    def idMessagePlayer2(self):
        return self.__id_message_player2

    
    @property
    async def messageLooser(self):
        if self.looser == None:
            return None
        if self.looser is self.player1:
            return await self.__dataManager.client.get_user(self.player1.idPlayer).dm_channel.fetch_message(self.__id_message_player1)
        else:
            return await self.__dataManager.client.get_user(self.player2.idPlayer).dm_channel.fetch_message(self.__id_message_player2)
    
    @property
    async def messageWinner(self):
        if self.winner == None:
            return None
        if self.winner is self.player1:
            return await self.__dataManager.client.get_user(self.player1.idPlayer).dm_channel.fetch_message(self.__id_message_player1)
        else:
            return await self.__dataManager.client.get_user(self.player2.idPlayer).dm_channel.fetch_message(self.__id_message_player2)
    

    
    def isFighting(self, player):
        '''
            Vérifie si le joueur est en train de combattre
        '''
        if self.isInvolved(player) and self.isCurrent():
            return True
        return False
    
    def isCurrent(self):
        return self.winner is None and not self.cancel
        
    def alreadyVote(self, player):
        return ((self.player1.idPlayer == player.idPlayer and self.actionPlayer1 is not None) 
            or (self.player2.idPlayer == player.idPlayer and self.actionPlayer2 is not None))

    def computeWinner(self):
        act1 = self.actionPlayer1
        act2 = self.actionPlayer2
        key_idj = self.player1.idPlayer
        key_idj2 = self.player2.idPlayer
        winner = None
        if act1.lower() == "feuille".lower():
            if act2.lower() == "feuille".lower():
                winner = None
            elif act2.lower() == "ciseaux".lower():
                winner = key_idj2
            else:
                winner = key_idj
        
        if act1.lower() == "ciseaux".lower():
            if act2.lower() == "ciseaux".lower():
                winner = None
            elif act2.lower() == "pierre".lower():
                winner = key_idj2
            else:
                winner = key_idj


        if act1.lower() == "pierre".lower():
            if act2.lower() == "pierre".lower():
                winner = None
            elif act2.lower() == "feuille".lower():
                winner = key_idj2
            else:
                winner = key_idj
        return winner

    def isFinished(self):
        return not (self.actionPlayer1 is None or self.actionPlayer2 is None)


# -- DATA MANAGER
class DataManager():

    ranking = []

    def __init__(self):
        '''
            _indexed sont des dictionnaires où les éléments sont indexés par identifiants are dictionary where elements are indexed by id.
            _ind_[property] sont des dictionnaires où la clef est la propriété précisée
        '''
        self.__players = []
        self.__players_indexed = {}
        self.__players_ind_name = {}

        self.__fights = []
        self.__fights_indexed = {}
        self.__fights_indexed_by_message = {}
        self.__wall_of_pfc = {}

        self.__ranking_message_id = None
        self.__chan_information_id = None
        self.__wall_of_epicness_id = None

        self.__guild = None
        self.__client = None

        self.__old_rank = None
        self.__pillow_knight_role_id = None

        # Counters
        self.__id_counter_fights = 0

    # Properties
    @property
    def fights(self):
        return self.__fights
    
    @fights.setter
    def fights(self, fights: List[Fight]):
        self.__fights = fights
        self.__fights_indexed = {}
        for fight in self.fights:
            self.__fights_indexed[fight.idFight] = fight

    @property
    def players(self):
        return self.__players
    
    @property
    def playersIndexed(self):
        return self.__players_indexed
    
    @property
    def wallOfPFC(self):
        return self.__wall_of_pfc

    @wallOfPFC.setter
    def wallOfPFC(self, wall_of_pfc):
        self.__wall_of_pfc = wall_of_pfc
        

    @property
    def channelInformation(self):
        return self.guild.get_channel(self.__chan_information_id)

    def setChannelInformationWithId(self, id_):
        '''
        Allow to change the id and check if the channel exists. 
        Return the channel if exists
        return false otherwise

        '''
        channel = self.guild.get_channel(id_)
        if channel is not None:
            self.__chan_information_id = id_
        return channel
        
    
    @property
    async def rankingMessage(self):
        chan_info = self.channelInformation
        if chan_info is None or self.__ranking_message_id is None:
            return None
        try:
            return await chan_info.fetch_message(self.__ranking_message_id)
        except discord.errors.NotFound:
            return None

    @rankingMessage.setter
    def rankingMessage(self, message: discord.message):
        self.__ranking_message_id = message.id
    

    @property
    def pillowKnightRoleId(self):
        return self.__pillow_knight_role_id
    
    @property
    def pillowKnightRole(self):
        if self.__pillow_knight_role_id is None:
            return None
        else:
            return self.guild.get_role(self.__pillow_knight_role_id)

    async def setPillowKnightRoleId(self, role_id: int):
        if role_id is None:
            raise Exception("Le rôle n'existe pas !")
        pillow_knight_role = self.guild.get_role(role_id)
        if pillow_knight_role is None:
            raise Exception("Le rôle n'existe pas !")


        # Remove le rôle de base s'il existe
        old_role = self.pillowKnightRole
        
        if old_role is not None:
            await self.replaceRoleFromPlayers(old_role, pillow_knight_role)
            self.__pillow_knight_role_id = role_id



    @property
    def wallOfEpicnessId(self):
        '''
            Channel id of the wall of epicness
        '''
        if self.wallOfPFC is None:
            return None
        
        channel = self.wallOfPFC.channel
        if channel is None:
            return None
        else:
            return channel.id
        

    
    @property
    def guild(self):
        return self.__guild
    
    @guild.setter
    def guild(self, guild):
        self.__guild = guild
    
    @property
    def client(self):
        return self.__client
    
    @client.setter
    def client(self, client):
        self.__client = client
    

    # Players methods
    def getPlayerById(self, id_player):
        '''
        Retourne le joueur trouvé à l'identifiant donné.
        Si le joueur n'est pas trouvé, retourne None
        '''
        if id_player in self.__players_indexed:
            return self.__players_indexed[id_player]
        return None
    
    def getPlayerByName(self, name, is_sensitive=False):
        '''
        Retourne le joueur trouvé au nom donné.
        Si le joueur n'est pas trouvé, retourne None
        '''
        for player in self.__players:
            if is_sensitive:
                if player.name == name:
                    return player
            else:
                if player.name.lower() == name.lower():
                    return player

    async def createPlayer(self, id_player, name):
        '''
            Crée un player et l'ajoute à la BDD
        '''
        player = Player(self)
        player.idPlayer = id_player
        player.name = name
        message = self.addPlayer(player)
        await self.syncRanking()
        return message
    
    def addPlayer(self, player):
        '''
        Permet d'ajouter un utilisateur, vérifie si l'utilisateur existe déjà.
        '''
        # Vérifier que le joueur existe pas déjà
        if player.idPlayer in self.__players:
            return PlayerAlreadyRegistered(player)
        
        # Vérifier que le nom du joueur n'est pas déjà prix
        if player.name in self.__players_ind_name:
            return NameExists(player.name)
        
        # Ajouter le joueur dans le tableau et dans les index
        self.__players.append(player)
        self.__players_indexed[player.idPlayer] = player
        self.__players_ind_name[player.name] = player
        return None

    def getListNamePlayers(self):
        '''
            Retourne une liste avec les noms de tous les joueurs
        '''
        return [player.name for _, player in self.__players_indexed.items()]


    # Fights methods
    def getFightById(self, id_fight):
        if id_fight in self.__fights_indexed:
            return self.__fights_indexed[id_fight]
        return None

    def getFightByMessageId(self, id_message):
        if id_message in self.__fights_indexed_by_message:
            return self.__fights_indexed_by_message[id_message]
        else:
            return None
    

    def getFight(self, id_player): 
        '''
            Retourne True si le joueur est en combat.
            Return False dans le cas contraire.
        '''

        for fight in self.__fights:
            if (fight.player1.idPlayer == id_player or fight.player2.idPlayer == id_player) and fight.winner is None:
                return fight
        return None

    def createFight(self, player1, player2):
        '''
        Create the fight and add it to the BDD
        '''
        fight = Fight(self.__id_counter_fights, player1, player2, self)
        self.addFight(fight)
        return fight
    
    def addFight(self, fight):
        '''
            Ajoute un combat, la classe Fight vérifie déjà si les deux joueurs ne sont pas en
            combat. On vérifie aussi que l'identifiant n'existe pas.
        '''
        fight.idFight = self.__id_counter_fights
        self.__id_counter_fights += 1
        self.__fights.append(fight)
        self.__fights_indexed[fight.idFight] = fight
        self.__fights_indexed_by_message[fight.idMessagePlayer1] = fight
        self.__fights_indexed_by_message[fight.idMessagePlayer2] = fight
    
    def getCurrentFights(self):
        '''
        Récupérer les combats qui ne sont pas finis (dont sans gagnant)
        '''
        current_fights = []
        for fight in self.__fights:
            if fight.isCurrent():
                current_fights.append(fight)
        return current_fights
    
    async def endFight(self, fight: Fight):
        '''
            Réalise toutes les actions de synchronisation en fin de combat
            comme mettre à jour les variables in_fight de chaque joueur.
        '''
        # Message players
        messagePlayer1 = await fight.messagePlayer1
        messagePlayer2 = await fight.messagePlayer2

        # Pop from indexes
        if messagePlayer1 is not None:
            self.__fights_indexed_by_message.pop(messagePlayer1.id, None)
        if messagePlayer2 is not None:
            self.__fights_indexed_by_message.pop(messagePlayer2.id, None)
        #self.__fights_indexed.pop(fight.idFight, None)
        
        # Remove from players
        fight.player1.sentFight = None
        fight.player2.removeReceivedFight(fight)
    
    def indexLists(self):
        # Indexed by id and name
        self.__players_indexed = {}
        self.__players_ind_name = {}
        for player in self.players:
            self.__players_indexed[player.idPlayer] = player
            self.__players_ind_name[player.name] = player
        
        # Indexed by name
        self.__fights_indexed = {}
        for fight in self.fights:
            self.__fights_indexed[fight.idFight] = fight
            self.__fights_indexed_by_message[fight.idMessagePlayer1] = fight
            self.__fights_indexed_by_message[fight.idMessagePlayer2] = fight
        
    def changeName(self, player, new_name):
        self.__players_ind_name.pop(player.name)
        player.name = new_name
        self.__players_ind_name[player.name] = player
        
    def getLastWinsOfPlayer(self, player):
        fights = []
        for fight in self.fights:
            if fight.isInvolved(player) and fight.winner is player:
                fights.append(fight)
        
        return fights
    
    def indexFight(self, fight):
        self.__fights_indexed[fight.idFight] = fight
        self.__fights_indexed_by_message[fight.idMessagePlayer1] = fight
        self.__fights_indexed_by_message[fight.idMessagePlayer2] = fight

    def resetFights(self):
        for fight in self.fights:
            print(fight)
            self.endFight(fight)
        
        self.__fights = []
        for player in self.players:
            player.reset_fights()

    def loadWallOfPFC(self, channel_id: int):
        if channel_id is None:
            wall_of_epicness_channel = None
        else:
            wall_of_epicness_channel = self.client.get_channel(channel_id)

        self.wallOfPFC = WallOfPFC(wall_of_epicness_channel)

    # Save and load
    def save_json(self, file):
        print("sauvegarde des données")
        data = {}
        with open(file, "w") as f:
            # On enregistred les joueurs
            data["players"] = [player.get_dict_json() for player in self.players]

            # On enregistre les combats
            data["fights"] = [fight.get_dict_json() for fight in self.fights]

            # Quelques données
            data["counter_fights_id"] = self.__id_counter_fights
            data["ranking_message_id"] = self.__ranking_message_id
            data["chan_information_id"] = self.__chan_information_id
            data["pillow_knight_role_id"] = self.__pillow_knight_role_id
            
            data["wall_of_epicness_id"] = self.wallOfPFC.channelId
            
            to_write = json.dumps(data)
            f.write(to_write)

    async def load_json(self, file, client):
        data = None
        with open(file, "r") as f:
            data = json.load(f)
        
        self.__players = []
        for player_dict in data["players"]:
            self.__players.append(Player(self).hydrate(player_dict))
        
        for fight_dict in data["fights"]:
            self.__fights.append(Fight(0, None, None, self).hydrate(fight_dict))
        
        self.__id_counter_fights = data.get("counter_fights_id", None)
        self.__ranking_message_id = data.get("ranking_message_id", None)
        self.__chan_information_id = data.get("chan_information_id", None)
        self.__pillow_knight_role_id = data.get("pillow_knight_role_id", None)
        
        self.loadWallOfPFC(data.get("wall_of_epicness_id", None))
        
        self.indexLists()
        await self.syncRanking()

    async def removeRoleFromPlayers(self, role: discord.Role):
        for player in self.players:
            member = self.guild.get_member(player.idPlayer)
            if member is None:
                continue
            roles = member.roles
            if role in roles:
                roles.remove(role)
                await member.edit(roles=roles)

    async def replaceRoleFromPlayers(self, old_role: discord.Role, new_role: discord.Role):
        print(f"{old_role} remplacé par {new_role}")
        for player in self.players:
            member = self.guild.get_member(player.idPlayer)
            if member is not None:
                roles = member.roles
                modified = False
                if old_role in roles:
                    roles.remove(old_role)
                    if new_role not in roles:
                        roles.append(new_role)
                    await member.edit(roles=roles)



    # Synchronisation Methods
    async def syncRolePlayers(self):
        '''
            Synchronise les roles des joueurs.
        '''
        pillow_knight_role = self.pillowKnightRole
        print(pillow_knight_role)
        
        for player in self.players:
            member = self.guild.get_member(player.idPlayer)

            if member is not None:

                # Pillow Knight Management
                if pillow_knight_role is not None:
                    # Pillow knight ?
                    if player.rank >= 0 and player.rank < 5:
                        if pillow_knight_role not in member.roles:
                            await member.add_roles(pillow_knight_role)

                    # Or not Pillow knight
                    else:
                        # Récupérer liste de rôles et le modifier
                        roles = member.roles
                        if pillow_knight_role in roles:
                            roles.remove(pillow_knight_role)
                            await member.edit(roles=roles)
            
            # Other roles ?
            pass
    
    async def syncRanking(self):
        '''
            Synchronise le classement quand c'est demandé pour mettre à jour la 
            liste des utilisateurs
        '''
        
        self.__old_rank = self.ranking
        if len(self.players) == 0: 
            self.ranking = []
            return 
        
        self.ranking = [v for k, v in sorted(self.__players_indexed.items(), key=lambda item: item[1].score, reverse=True)]

        if self.__old_rank == None:
            return
        
        # Réagir en fonction des changements de rank
        for i, player in enumerate(self.__old_rank):
            
            if i != player.rank:
                try:
                    await send_message(await ChangeRank(player, i, player.rank).direct_message_to_player(player, self.client))
                except discord.errors.Forbidden as e:
                    print(f"Forbbidden : On n'a pas envoyé de message au joueur {player.name} parce qu'il n'existe plus (FORBIDDEN)")
                except discord.errors.HTTPException as e:
                    print(f"Channel Undefined : On n'a pas envoyé de message au joueur {player.name} parce qu'il n'existe plus (FORBIDDEN)")
                except exceptions.channelUndefined as e:
                    print(f"Channel Undefined : Le joueur {player.name} n'existe certainement plus.")
                except Exception as e:
                    print(f"Exception non connue : Le joueur {player.name} n'existe certainement plus.")

        if self.wallOfPFC is not None and self.__old_rank != {}:
            await self.wallOfPFC.onRankSync(self.__old_rank, self.ranking)
        print("Synchronisation des rôles")
        await self.syncRolePlayers()
        
