from data import DataManager
import os
import discord


# -- UTILS FUNCTIONS
async def send_direct_message(player, message):
    if player is None:
        print(message)
    else:
        if player.dm_channel is None:
            await player.create_dm()
        await player.dm_channel.send(message)


async def send_message(channel, message):
    '''
    Envois un message, soit au channel donné, soit en print si le channel est None.
    '''
    if channel is None:
        print(message)
    else:
        await channel.send(message)



# -- GAME MANAGER
class GameManager:
    '''
        Cette classe gère tous les aspects du jeu. Il permet aussi d'envoyer des messages.
    '''
    dataManager = None
    

    PICKLE_FILE = "data.cornichon"

    def __init__(self, data = None):
        print("On a construit GameManager")
        self.dataManager = DataManager()
    


    def score(self, player):
        '''
        Compute the score of a player
        '''
        win = player["nb_win"]
        loose = player["nb_loose"]
        score = win * 20 - loose * 5 
        player["score"] = score
        return score
    
    async def register(self, id_joueur, name, channel=None):
        print(f"Enregistrer avec {name}")
        '''
        Enregistrer un membre dans le jeu
        '''
        
        # Vérifier que le joueur n'existe pas déjà, soit son ID, soit son name, hein FlutterShy !
        if self.dataManager.getPlayerById(id_joueur) is not None:
            await send_message(channel, "T'es déjà enregistré, bouffon !")
            return False
        
        if self.dataManager.getPlayerByName(name) is not None:
            await send_message(channel, "Le pseudo est déjà pris, t'es mauvais jack !")
            return False
        
        self.dataManager.addPlayer(id_joueur, name)
        await send_message(channel, "Enregistrement DONE. Welcome to the trigone ! Que la triforce soit avec toi !")
        return True
        

    async def listPlayers(self, channel=None):
        '''
        Liste les joueurs enregistrés
        '''
        players = self.dataManager.getListNamePlayers()
        message = "Liste des joueurs : \n"
        for player in players:
            message += player + "\n"
        await send_message(channel, message)



    # -- FIGHTS
    async def attack(self, id_joueur1, id_joueur2, client=None):
        '''
        Attaquer un joueur
        '''
        # On récupère le player 1 du client
        c_player1 = None
        c_player2 = None
        if client is not None:
            c_player1 = client.get_user(id_joueur1)

        if c_player1.dm_channel is None:
            print("ON A UN PROBLEM CHEF!")
            return False

        # Est-ce que le joueur 1 existe dans BDD ? 
        player1 = self.dataManager.getPlayerById(id_joueur1)
        if player1 is None:
            await send_direct_message(c_player1, "https://media.giphy.com/media/XZ39zg4naZ1O8/giphy.gif")
            return False

        # Est-ce que le joueur 2 existe dans la BDD
        player2 = self.dataManager.getPlayerById(id_joueur2)
        if player2 is None: 
            await send_direct_message(c_player1, "Joueur 2 non trouvé")
            return False

        # Est-ce que le joueur 2 est le joueur 1?
        if player2["id"] == player1["id"]:
            await send_direct_message(c_player1, "Tu ne peux pas t'attaquer toi-même ! https://i.pinimg.com/originals/50/ab/ee/50abee00257155868ac43c7e9cb64bed.gif")
            return False

        # Est-ce que joueur 1 est passif ?
        if player1["actif"] is False:
            await send_direct_message(c_player1, "Tu es en mode passif espèce de singe ! https://tplmoms.com/wp-content/uploads/2017/05/crottes.gif")
            return False
        
        # Est-ce que joueur 2 est passif ?
        if player2["actif"] is False:
            await send_direct_message(c_player1, "Le joueur que tu as attaqué est en mode 'passif'.")
            return False
            
        # Est-ce que le player 2 existe dans le discord ?
        if client is not None:
            c_player2 = client.get_user(id_joueur2)
            if c_player2 is None:
                await send_direct_message(c_player1, "Il y a eu un bug de communication, ce n'est pas possible d'atteindre le joueur.")
                return False
        
        # Est-ce que les deux joueurs sont déjà en fight ?
        created = self.dataManager.createFight(id_joueur1, id_joueur2)
        if created:
            await send_direct_message(c_player1, "Invitation reçue !\npierre, feuille, ou ciseaux ?")
            await send_direct_message(c_player2, "Vous avez été défié !\npierre, feuille, ou ciseaux ?")
        else:
            await send_direct_message(c_player1, "L'un des deux joueurs est déjà en duel.")
        return True
        

    def fightIsFinished(self, fight):
        '''
            Vérifie si les deux actions ont été remplies et retourne True si le combat est fini, False dans le cas contraire.
        '''
        return not (fight["action_player1"] is None or fight["action_player2"] is None)
    

    def getWinner(self, fight):
        '''
            action_1: action du player 1
            action_2: action du player 2

            return : return None if not ended

                the id of winner
        '''
        act1 = fight["action_player1"]
        act2 = fight["action_player2"]
        key_idj = fight["id_player1"]
        key_idj2 = fight["id_player2"]
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
        
    async def actionPlayer(self, id_player, action, channel=None, client=None):
        '''
        Réaliser l'action 'pierre' 'feuille' ou 'ciseaux' du joueur
        dans son combat.
        '''
        # Chercher son combat
        fight_index, fight = self.dataManager.getFight(id_player)

        # Vérifier qu'il y a bien un combat
        if fight is None:
            await send_message(channel, "Tu n'es pas en combat !")
            return False

        # Déjà voté ?
        if (fight["id_player1"] == id_player and fight["action_player1"] is not None) or (fight["id_player2"] == id_player and fight["action_player2"] is not None):
            await send_message(channel, "Tu as déjà voté !")
            return False
        
        # Match terminé ?
        if fight["winner"] is not None:
            await send_message(channel, "Le duel est fini ! ")
            return False
        
        # Sinon on peut ajouter l'action
        if fight["id_player1"] == id_player:
            fight["action_player1"] = action
        else:
            fight["action_player2"] = action

        
        # Qui est le joueur 2
        if id_player == fight["id_player1"]:
            id_player2 = fight["id_player2"]
        else:
            id_player2 = fight["id_player1"]

        # Créer le DM de Joueur 2
        c_player2 = None;
        if client is not None:
            c_player2 = client.get_user(id_player2)
        
        
        # Match terminé maintenant ?
        if self.fightIsFinished(fight):
            # Récupération du winner id et création variable looser is
            winner_id = self.getWinner(fight)
            looser_id = None

            # Cas d'égalité
            if winner_id is None:
                fight["action_player1"] = None
                fight["action_player2"] = None
                await send_message(channel, "Il y a eu égalité !\npierre, feuille, ciseaux ?")
                await send_direct_message(c_player2, "Il y a eu égalité !\npierre, feuille, ciseaux ?")
                self.dataManager.setFight(fight_index, fight)
                
            # Cas le combat est fini !
            else:
                # Update fight
                fight["winner"] = winner_id
                self.dataManager.setFight(fight_index, fight)

                # Get winner and looser
                if winner_id == id_player:
                    looser_id = id_player2
                else:
                    looser_id = id_player

                # Get players
                winner_player = self.dataManager.getPlayerById(winner_id)
                looser_player = self.dataManager.getPlayerById(looser_id)
                # Augmenter les compteurs win et loose
                winner_player["nb_win"] += 1
                looser_player["nb_loose"] += 1

                # Gérer les win et loose consécutives
                if winner_player["nb_loose_cons"] > 0:
                    winner_player["nb_win_cons"] = 0
                    winner_player["nb_loose_cons"] = 0
                winner_player["nb_win_cons"] += 1
                if winner_player["nb_win_cons"]  > winner_player["nb_win_cons_max"]:
                    winner_player["nb_win_cons_max"] = winner_player["nb_win_cons"]
                
                if looser_player["nb_win_cons"] > 0:
                    looser_player["nb_win_cons"] = 0
                    looser_player["nb_loose_cons"] = 0
                looser_player["nb_loose_cons"] += 1
                if looser_player["nb_loose_cons"]  > looser_player["nb_loose_cons_max"]:
                    looser_player["nb_loose_cons_max"] = looser_player["nb_loose_cons"]

                self.score(winner_player)
                self.score(looser_player)

                # On prépare les messages de win et de loose
                win_message = f"Vous avez vaincu le joueur {looser_player['name']} !"
                loose_message = f"Vous avez perdu contre le joueur {winner_player['name']} !"

                # Envoyer le message à la bonne personne
                if winner_id == id_player:
                    await send_message(channel, win_message)
                    await send_direct_message(c_player2, loose_message)
                else:
                    await send_message(channel, loose_message)
                    await send_direct_message(c_player2, win_message)

                self.dataManager.endFight(fight)
                self.dataManager.syncRanking()
        else:
            await send_direct_message(c_player2, "L'autre joueur a fait son choix, et toi (pierre, feuille, ciseaux) ?")
            await send_message(channel, "Nous avons bien reçu votre action")
        return True


    async def listCurrentFights(self, channel=None):
        '''
        Donne la liste des combats en cours à l'utilisateur
        '''
        fights = self.dataManager.getCurrentFights()
        message = "Liste des combats : \n"
        for fight in fights:
            player1 = self.dataManager.getPlayerById(fight['id_player1'])
            player2 = self.dataManager.getPlayerById(fight['id_player2'])

            message += f"{player1['name']} versus {player2['name']}\n"
        
        await send_message(channel, message)
            
    async def mystats(self, id_player, channel=None):
        
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier que l'utilisateur existe bien
        if player is None:
            await send_message(channel, "Vous n'êtes pas encore enregistré. Veuillez vous enregistrer avec !register.")
            return False
        
        # Retourner les stats du joueur
        score = self.score(player)
        actif_message = "actif" if player["actif"] else "passif"
        in_fight_message = "oui" if player["in_fight"] else "non"
        message = "\n".join([
            f"Vos stats {player['name']}",
            f"win : {player['nb_win']}",
            f"loose : {player['nb_loose']}",
            f"Wins consécutives : {player['nb_win_cons']}",
            f"Looses consécutives : {player['nb_loose_cons']}",
            f"Wins consécutives MAX : {player['nb_win_cons_max']}",
            f"Looses consécutives MAX: {player['nb_loose_cons_max']}",
            f"score : {score}",
            f"état du compte : {actif_message}",
            f"en combat? : {in_fight_message}"
        ])
        await send_message(channel, message)

    async def listRanking(self, channel=None):
        '''
            Permet à l'utilisateur de faire lister le classement
        '''
        message = "Le classement : \n"
        print(self.dataManager.ranking)
        for i, player in enumerate(self.dataManager.ranking):
            message += f"({i}) {player['name']} avec {player['score']} pts\n"
        await send_message(channel, message)
    
    def load_game(self):
        '''
        Charger les données du jeu
        '''
        if os.path.isfile(self.PICKLE_FILE):
            print("Chargement des données")
            self.dataManager.loadPickleFile(self.PICKLE_FILE)
    
    def save_game(self):
        '''
        Sauvegarde les données du jeu
        '''
        print("sauvegarde des données")
        self.dataManager.dumpPickleFile(self.PICKLE_FILE)


    
    async def becomePassif(self, id_joueur, channel=None):
        '''
            Devenir passif pour ne plus être attaqué
        '''
        # Récupération du joueur
        player = self.dataManager.getPlayerById(id_joueur)

        # Est-ce que le joueur existe ? 
        if player is None:
            await send_message(channel, "Vous n'êtes pas encore enregistré.\nVeuillez écrire !register [nom]")
            return False

        # Est-ce que le joueur est actif ?
        print(player) 
        if player["actif"]:
            print("Devient passif !")
            player["actif"] = False
            print(player)
            self.dataManager.setPlayer(player)
            await send_message(channel, "Tu es bien passé en mode passif ! https://thumbs.gfycat.com/PoliteClearBlackfish-size_restricted.gif")
        else:
            await send_message(channel, "T'es déjà passif ! https://thumbs.gfycat.com/PoliteClearBlackfish-size_restricted.gif")



    async def becomeActif(self, id_joueur, channel=None):
        '''
            Devenir actif pour être à nouveau attaqué
        '''
        # Récupération du joueur
        player = self.dataManager.getPlayerById(id_joueur)

        # Est-ce que le joueur existe ? 
        if player is None:
            send_message(channel, "Vous n'êtes pas encore enregistré.\nVeuillez écrire !register [nom]")
            return False

        # Est-ce que le joueur est actif ? 
        if not player["actif"]:
            player["actif"] = True
            await send_message(channel, "Tu es bien passé en mode actif ! https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR5olQJ0iCPut7COcWGoAePC36usg_uE3O8xCYcnp03EPuFz4f9w&s")
        else:
            await send_message(channel, "T'es déjà actif ! https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR5olQJ0iCPut7COcWGoAePC36usg_uE3O8xCYcnp03EPuFz4f9w&s")

    async def cancelFight(self, id_player, channel):
        '''
        '''

        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier existence du joueur
        if player is None:
            await send_message(channel, "Il faut d'abord t'enregistrer tête de noeuds !")
        
        # Est-ce qu'il est en combat ?
        if not player["in_fight"]:
            await send_message(channel, "Tu n'es pas en combat !")
            return False
        
        # En combat ? il faut le trouver et le supprimer
        for i, fight in enumerate(self.dataManager.data["fights"]):
            if (fight["id_player1"] == id_player or fight["id_player2"] == id_player) and fight["winner"] is None:
                player1 = self.dataManager.getPlayerById(fight["id_player1"])
                player2 = self.dataManager.getPlayerById(fight["id_player2"])
                player1["in_fight"] = False
                player2["in_fight"] = False
                del self.dataManager.data["fights"][i]
                await send_message(channel, "On a bien supprimé ton combat ! Retourne te battre moussaillon ! https://media.giphy.com/media/ihMKNwb2yPEbWJiAmn/giphy.gif")
                return True
        
        await send_message(channel, "On n'a pas trouvé de combat mais tu peux maintenant attaquer qui tu veux ! https://media.giphy.com/media/ihMKNwb2yPEbWJiAmn/giphy.gif")
        return False

    async def changeName(self, name, new_name, channel):
        # Chercher le player avec le nom donné
        player = self.dataManager.getPlayerByName(name)

        # Est-ce que le joueur existe ?
        if player is None:
            await send_message(channel, f"Le joueur {name} n'existe pas.")
            return False

        # Est-ce que le nouveau nom n'existe pas déjà ?
        player_new = self.dataManager.getPlayerByName(new_name)

        if player_new is not None:
            await send_message(channel, f"Le pseudo {new_name} existe déjà")
            return False
        
        # Modifier son nom
        player["name"] = new_name
        await send_message(channel, "Le nom du joueur a bien été modifié")
        return True


    async def help(self, channel):

        message = "\n".join([
            "T'es nouveau, si tu veux jouer, fais ces commandes :",
            "`!register [pseudo]` : enregistre toi avec un pseudo",
            "`!players` : liste les joueurs",
            "`!attack [pseudo du joueur]` : attaque la personne ayant le pseudo fourni",
            "",
            "Bienvenu sur le message d'aide, voici la liste des commandes :",
            "`!help` : message d'aide avec la liste des commandes",
            "`!register [pseudo]` : s'enregistrer avec le pseudo donné",
            "`!players` : liste les noms des joueurs",
            "`!attack [pseudo du joueur]` : attaquer le joueur avec le pseudo donné",
            "`!mystats` : voir mes statistiques",
            "`!current-fights` : liste les combats en cours",
            "`!ranking` : liste le classement des joueurs avec leurs points",
            "`!actif` : vous met en mode actif, vous pouvez être attaqué et attaquer à nouveau",
            "`!passif` : vous met en mode passif, vous ne pouvez plus attaquer et être attaqué",
            "`!cancel` : supprime le combat en cours, n'en abuse pas s'il te plaît.",
            "",
            "PS : J'ai soif de boire https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHHzo3NXvZN2D63gbYVvpzWJ9lyk4gC6v3mheuGX-XeOc-FRe5&s"
        ])

        await send_message(channel, message)



class EventManager:
    '''
    La classe qui gère les événements et appelle les bonnes méthodes.
    '''
    def __init__(self):
        print("Construction de l'event manager")