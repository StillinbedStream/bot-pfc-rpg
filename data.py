
import pickle

# -- DATA MANAGER
class DataManager:

    data = {}
    ranking = {}

    def __init__(self):
        self.data = {
            "players": {},
            "fights": [],
            "ids": {
                "fights": 0
            }
        }
    

    # - FONCTIONS MODELE PLAYER
    def getPlayerById(self, id):
        '''
        Retourne le joueur trouvé à l'identifiant donné.
        Si le joueur n'est pas trouvé, retourne None
        '''
        if id in self.data["players"]:
            player = self.data["players"][id]
            if not "actif" in player:
                player["actif"] = True
            if not "nb_loose_cons_max" in player:
                player["nb_loose_cons_max"] = 0
            if not "nb_win_cons_max" in player:
                player["nb_win_cons_max"] = 0
            return player
        else:
            return None
    
    def getPlayerByName(self, name):
        '''
        Retourne le joueur trouvé au nom donné.
        Si le joueur n'est pas trouvé, retourne None
        '''
        for _, player in self.data["players"].items():
            if player["name"] == name:
                return player
        return None

    def setPlayer(self, player):
        '''
        '''
        self.data["players"][player["id"]] = player
    
    def addPlayer(self, id_, name_):
        '''
            Ajoute un joueur à la BDD s'il n'existe pas déjà
            Retourne True si le joueur a bien été ajouté
            Retourne False dans le cas contraire
        '''
        if id in self.data["players"]:
            return False
        else:
            self.data["players"][id_] = {"name": name_, "id": id_, "in_fight": None, "nb_win": 0, "nb_loose": 0, "nb_loose_cons": 0, "nb_win_cons": 0, "score": 0, "actif": True, "nb_loose_cons_max" : 0, "nb_win_cons_max": 0}
            self.syncRanking()
            return True

    def getListNamePlayers(self):
        '''
            Retourne une liste avec les noms de tous les joueurs
        '''
        return [player["name"] for _, player in self.data["players"].items()]

    def setFight(self, fight_index, fight):
        self.data["fights"][fight_index] = fight

    def getFight(self, id_player): 
        '''
            Retourne True si le joueur est en combat.
            Return False dans le cas contraire.
        '''

        for i, fight in enumerate(self.data["fights"]):
            if (fight["id_player1"] == id_player or fight["id_player2"] == id_player) and fight["winner"] is None:
                return i, fight
        return None            


    def isInFight(self, id_player):
        '''
            Retourne True si le joueur est en combat.
            Return False dans le cas contraire.
        '''
        if not id_player in self.data["players"]:
            return None
        else:
            return self.data["players"][id_player]["in_fight"] == True

    # - FONCTIONS MODELE COMBAT
    def createFight(self, id_player1, id_player2):
        # Vérifier que les deux utilisateurs ne sont pas déjà en combat
        if self.isInFight(id_player1):
            return False
        
        if self.isInFight(id_player2):
            return False
        
        # Ajouter le combat
        self.data["fights"].append({
            "id": self.data["ids"]["fights"],
            "id_player1": id_player1,
            "id_player2": id_player2,
            "winner": None,
            "action_player1": None,
            "action_player2": None,
            "waiting": id_player2
        })

        self.data["players"][id_player1]["in_fight"] = True
        self.data["players"][id_player2]["in_fight"] = True
        return True
    
    def getCurrentFights(self):
        '''
        Récupérer les combats qui ne sont pas finis (dont sans gagnant)
        '''
        current_fights = []
        for fight in self.data["fights"]:
            if fight["winner"] == None:
                current_fights.append(fight)
        return current_fights
    

    def findCurrentFight(self, id_joueur):
        '''
            Chercher un combat en cours d'un joueur donné. 
            Il ne peut y en avoir qu'un.
            Retourne None si non trouvé
        '''
        for fight in self.data["fight"]:
            if fight["id_player1"] == id_joueur and fight["winner"] is None:
                return True
        return False
    
    def endFight(self, fight):
        '''
            Réalise toutes les actions de synchronise en fin de combat
            comme mettre à jour les variables in_fight de chaque joueur.
        '''
        self.data["players"][fight["id_player1"]]["in_fight"] = False
        self.data["players"][fight["id_player2"]]["in_fight"] = False
            
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
        self.ranking = [v for k, v in sorted(self.data["players"].items(), key=lambda item: item[1]["score"], reverse=True)]
