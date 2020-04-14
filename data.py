# TODO: Gérer la synchronisation du classement.

import pickle

# -- Entities
class Entity:

    def __init__(self):
        pass

class Player(Entity):
    def __init__(self):
        self.__name = ""
        self.__id_player = ""
        self.__in_fight = ""

        self.__nb_win = 0
        self.__nb_win_cons = 0
        self.__nb_win_cons_max = 0

        self.__nb_loose = 0
        self.__nb_loose_cons = 0
        self.__nb_loose_cons_max = 0

        self.__score = 0
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
    

    # inFight
    @property
    def inFight(self):
        return self.__in_fight
    
    @inFight.setter
    def inFight(self, in_fight):
        self.__in_fight = in_fight
    

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
    def nbWinConsMax(self, nb_win_cons_max):
        return self.__nb_win_cons_max
    
    @nbWinConsMax.setter
    def nbWinConsMax(self,nb_win_cons_max):
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

    @nbLooseMax.setter
    def nbLooseMax(self, nb_loose_cons):
        self.__nb_loose_cons = nb_loose_cons
    

    # nbLooseConsMax
    @property
    def nbLooseConsMax(self):
        return self.__nb_loose_cons_max
    
    @nbLooseConsMax.setter
    def nbLooseConsMax(self, nb_loose_cons_max):
        self.__nb_loose_cons_max = nb_loose_cons_max
    

    # score
    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self, score):
        self.__score = score
    
    # exp
    @property
    def exp(self):
        return self.__score
    
class Fight(Entity):

    def __init__(self, idFight, player1, player2):
        '''
            Initialise le combat. Il vérifie aussi que les joueurs ne soient pas
            déjà en combat via la propriété inFight.
        '''
        # Vérifie si le player 1 et 2 sont en combat
        if player1.inFight == True:
            raise Exception(f"Le joueur {player1.name} est déjà en combat.")

        if player2.inFight == True:
            raise Exception(f"Le joueur {player2.name} est déjà en combat.")

        player1.inFight = True
        player2.inFight = True

        self.__id_fight = idFight
        self.__player1 = player1
        self.__player2 = player2
        self.__winner = None
        self.__action_player1 = None
        self.__action_player2 = None
    

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


    # Players methods
    def getPlayerById(self, id_player):
        '''
        Retourne le joueur trouvé à l'identifiant donné.
        Si le joueur n'est pas trouvé, retourne None
        '''
        if id_player in self.__players_indexed:
            return self.__players_indexed["id_player"]
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
        self.addPlayer(player)
    
    def addPlayer(self, player):
        '''
        Permet d'ajouter un utilisateur, vérifie si l'utilisateur existe déjà.
        '''
        # Vérifier que le joueur existe pas déjà
        if player.idPlayer in self.__players:
            raise Exception("Le joueur ne peut pas être ajouté, son id existe déjà.")
        
        # Vérifier que le nom du joueur n'est pas déjà prix
        if player.name in self.__players_ind_name:
            raise Exception("Le joueur ne peut pas être ajouté, son nom existe déjà")
        
        # Ajouter le joueur dans le tableau et dans les index
        self.__players.append(player)
        self.__players_indexed[player.idPlayer] = player
        self.__players_ind_name[player.name] = player
    
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

    def setFight(self, fight):
        if fight.idFight not in self.__fights_indexed:
            raise Exception("L'identifiant du combat n'existe pas. Il y a peut-être un bug, veuillez contacter l'administrateur.")
        self.__fights[fight.idFight] = fight

    def getFight(self, id_player): 
        '''
            Retourne True si le joueur est en combat.
            Return False dans le cas contraire.
        '''

        for fight in self.data["fights"]:
            if (fight.player1.idPlayer == id_player or fight.player2.idPlayer == id_player) and fight.winner is None:
                return fight
        return None

    def createFight(self, player1, player2):
        '''
        Create the fight and add it to the BDD
        '''
        fight = Fight(self.__id_counter_fights, player1, player2)
        self.__id_counter_fights += 1
        self.addFight(fight)
        return fight
    
    def addFight(self, fight):
        '''
            Ajoute un combat, la classe Fight vérifie déjà si les deux joueurs ne sont pas en
            combat. On vérifie aussi que l'identifiant n'existe pas.
        '''
        if fight.idFight <= len(self.__fights):
            raise Exception("L'identifiant du combat existe déjà. Veuillez contacter votre administrateur, le boss quoi.")
        self.__fights.append(fight)
    
    def getCurrentFights(self):
        '''
        Récupérer les combats qui ne sont pas finis (dont sans gagnant)
        '''
        current_fights = []
        for fight in self.__fights:
            if fight.winner == None:
                current_fights.append(fight)
        return current_fights
    
    def findPlayerCurrentFights(self, id_player):
        '''
            Chercher un combat en cours d'un joueur donné. 
            Il ne peut y en avoir qu'un.
            Retourne None si non trouvé
        '''
        for fight in self.__fights:
            if fight.player1.idPlayer == id_player or fight.player2.idPlayer == id_player:
                return fight
        return None
    
    def endFight(self, fight):
        '''
            Réalise toutes les actions de synchronise en fin de combat
            comme mettre à jour les variables in_fight de chaque joueur.
        '''
        self.getPlayerById(fight.player1.idPlayer).inFight = False
        self.getPlayerById(fight.player2.idPlayer).inFight = False
    
    # - FONCTIONS UTILITAIRES
    def loadPickleFile(self, filename):
        '''
            Charge le fichier pickle dans self.data
        '''
        with open(filename, "rb") as f:
            self.data = pickle.load(f)
        self.syncRanking()

    def dumpPickleFile(self, filename):
        '''
            Sauverde self.data dans le fichier pickle.
        '''
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    def syncRanking(self):
        '''
            Synchronise le classement quand c'est demandé pour mettre à jour la 
            liste des utilisateurs
        '''
        self.ranking = [v for k, v in sorted(self.__players, key=lambda item: item.score, reverse=True)]
