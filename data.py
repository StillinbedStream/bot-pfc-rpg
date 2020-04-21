# TODO: Gérer la synchronisation du classement.

import pickle
import exceptions
import messages

# -- Entities
class Entity:

    def __init__(self):
        pass

class Player(Entity):
    def __init__(self):
        self.__name = ""
        self.__id_player = ""
        self.__sent_fight = None
        self.__receive_fights = []

        self.__nb_win = 0
        self.__nb_win_cons = 0
        self.__nb_win_cons_max = 0

        self.__nb_loose = 0
        self.__nb_loose_cons = 0
        self.__nb_loose_cons_max = 0

        self.__actif = True
        pass
    
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
        return self.nbWin * 20 - self.nbLoose * 5
    
    # exp
    @property
    def exp(self):
        return self.score
    
    def addReceiveFight(self, fight):
        if self.hasAlreadyReceiveFight(fight):
            return False
        self.__receive_fights.append(fight)       
        return True
    
    def hasAlreadyReceiveFight(self, fight):
        for f in self.__receive_fights:
            if fight == f:
                return True
        return False
        
    def removeReceiveFight(self, fight):
        '''
            Permet de supprimer un combat 
            que le joueur a reçu.
        '''
        for i, f in enumerate(self.__receive_fights):
            if fight == f:
                del self.__receive_fights[i]
                return True
        return False

    def getNbReceiveFights(self):
        return len(self.__receive_fights)
    
    @property
    def sentFight(self):
        return self.__sent_fight
    
    @sentFight.setter
    def sentFight(self, fight):
        self.__sent_fight = fight
    
    @property
    def receiveFights(self):
        return self.__receive_fights
    
    def getCurrentReceiveFight(self):
        for fight in self.__receive_fights:
            if not fight.alreadyVote(self):
                return fight
        return None

class Fight(Entity):
    def __init__(self, idFight, player1, player2):
        player1.sentFight = self
        player2.addReceiveFight(self)

        self.__id_fight = idFight
        self.__player1 = player1
        self.__player2 = player2
        self.__winner = None
        self.__action_player1 = None
        self.__action_player2 = None
        self.__cancel = False
    
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
        return self.__player1
    
    @player1.setter
    def player1(self, player1):
        self.__player1 = player1

    # player2
    @property
    def player2(self):
        return self.__player2
    
    @player2.setter
    def player2(self, player2):
        self.__player2 = player2
    
    # winner
    @property
    def winner(self):
        return self.__winner
    
    @winner.setter
    def winner(self, winner):
        self.__winner = winner
    
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
        return (self.player1.idPlayer == player.idPlayer and self.actionPlayer1 is not None) or (self.player2.idPlayer == player.idPlayer and self.actionPlayer2 is not None)

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
        player = Player()
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
        fight = Fight(self.__id_counter_fights, player1, player2)
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
        fight.player2.removeReceiveFight(fight)
    
    # Ranking methods
    def syncRanking(self):
        '''
            Synchronise le classement quand c'est demandé pour mettre à jour la 
            liste des utilisateurs
        '''
        self.ranking = [v for k, v in sorted(self.__players_indexed.items(), key=lambda item: item[1].score, reverse=True)]
