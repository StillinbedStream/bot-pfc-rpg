# TODO: Gérer la synchronisation du classement.

import pickle
import exceptions
import messages
import copy
import json

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
        for key, value in self.__dict__.items():
            if not key == "_" + type(self).__name__ + "__dataManager":
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

        self.__signature = ""
        
    # name
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
    

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
        return (self.nbWin * 20 - self.nbLoose * 5
            - self.receivedTokens * 4 - self.sentTokens * 5)
    
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
                del self.__received_fights[i]
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

    ranking = {}

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

        # Counters
        self.__id_counter_fights = 0

    # Properties
    @property
    def fights(self):
        return self.__fights
    
    @fights.setter
    def fights(self, fights):
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
    

    # Players methods
    def getPlayerById(self, id_player):
        '''
        Retourne le joueur trouvé à l'identifiant donné.
        Si le joueur n'est pas trouvé, retourne None
        '''
        if id_player in self.__players_indexed:
            return self.__players_indexed[id_player]
        return None
    
    def getPlayerByName(self, name):
        '''
        Retourne le joueur trouvé au nom donné.
        Si le joueur n'est pas trouvé, retourne None
        '''
        for player in self.__players:
            if player.name == name:
                return player

    def createPlayer(self, id_player, name):
        '''
            Crée un player et l'ajoute à la BDD
        '''
        player = Player(self)
        player.idPlayer = id_player
        player.name = name
        message = self.addPlayer(player)
        self.syncRanking()
        return message
    
    def addPlayer(self, player):
        '''
        Permet d'ajouter un utilisateur, vérifie si l'utilisateur existe déjà.
        '''
        # Vérifier que le joueur existe pas déjà
        if player.idPlayer in self.__players:
            return messages.PlayerAlreadyRegistered(player)
        
        # Vérifier que le nom du joueur n'est pas déjà prix
        if player.name in self.__players_ind_name:
            return messages.NameExists(player.name)
        
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
    
    def getCurrentFights(self):
        '''
        Récupérer les combats qui ne sont pas finis (dont sans gagnant)
        '''
        current_fights = []
        for fight in self.__fights:
            if fight.isCurrent():
                current_fights.append(fight)
        return current_fights
    
    def endFight(self, fight):
        '''
            Réalise toutes les actions de synchronise en fin de combat
            comme mettre à jour les variables in_fight de chaque joueur.
        '''
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
            data["id_counter_fights"] = self.__id_counter_fights
            to_write = json.dumps(data)
            f.write(to_write)

    def load_json(self, file):
        data = None
        with open(file, "r") as f:
            data = json.load(f)
        
        self.__players = []
        for player_dict in data["players"]:
            self.__players.append(Player(self).hydrate(player_dict))
        
        for fight_dict in data["fights"]:
            self.__fights.append(Fight(0, None, None, self).hydrate(fight_dict))
        
        self.__id_counter_fights = data["id_counter_fights"]
        self.indexLists()
        self.syncRanking()

    # Ranking methods
    def syncRanking(self):
        '''
            Synchronise le classement quand c'est demandé pour mettre à jour la 
            liste des utilisateurs
        '''
        self.ranking = [v for k, v in sorted(self.__players_indexed.items(), key=lambda item: item[1].score, reverse=True)]
