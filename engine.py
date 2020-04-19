from data import DataManager
import os
import discord
import pickle
import exceptions
import utils
import asyncio
from random import choice


# -- GAME MANAGER
class GameManager:
    '''
        Cette classe gère tous les aspects du jeu. Il permet aussi d'envoyer des messages.
    '''
    

    PICKLE_FILE = "data.cornichon"

    def __init__(self, wallOfPFC):
        self.__dataManager = DataManager()
        self.__wallOfPFC = wallOfPFC
    
    @property
    def dataManager(self):
        return self.__dataManager
    


    # Commands
    async def register(self, id_joueur, name, channel=None):
        '''
        Enregistrer un membre dans le jeu
        '''
        
        # Vérifier que le joueur n'existe pas déjà, soit son ID, soit son name, hein FlutterShy !
        player = self.__dataManager.getPlayerById(id_joueur)
        if player is not None:
            raise exceptions.PlayerAlreadyRegistered(player)
        
        if self.__dataManager.getPlayerByName(name) is not None:
            raise exceptions.NameExists(name)

        self.__dataManager.createPlayer(id_joueur, name)
        await utils.send_message(channel, "Enregistrement DONE. Welcome to the trigone ! Que la triforce soit avec toi !")
        await asyncio.sleep(4)
        await utils.send_message(channel, "Dans un premier temps affiche la liste des joueurs actifs avec la commande : !show-actifs")
        await asyncio.sleep(4)
        await utils.send_message(channel, "Tu peux ensuite attaquer qui tu veux avec la commande : !attack [pseudo]")
        await asyncio.sleep(4)
        await utils.send_message(channel, "Pour ne plus subir d'attaques, utilises la commande : !passif")

    async def attack(self, id_joueur1, id_joueur2, client=None):
        '''
        Attaquer un joueur
        '''
        # On récupère le player 1 du client
        c_player1 = None
        c_player2 = None
        if client is not None:
            c_player1 = client.get_user(id_joueur1)

        # Est-ce que le joueur 1 existe dans BDD ? 
        player1 = self.dataManager.getPlayerById(id_joueur1)
        if player1 is None:
            raise exceptions.PlayerNotRegistered()

        # Est-ce que le joueur 2 existe dans la BDD
        player2 = self.dataManager.getPlayerById(id_joueur2)
        if player2 is None: 
            raise exceptions.Player2NotRegistered()

        # Est-ce que le joueur 2 est le joueur 1?
        if player2.idPlayer == player1.idPlayer:
            raise exceptions.AttackMySelf()

        # Est-ce que joueur 1 est passif ?
        if player1.actif is False:
            raise exceptions.PlayerPassif()

        # Est-ce que joueur 2 est passif ?
        if player2.actif is False:
            raise exceptions.Player2Passif()

        # Est-ce que le player 2 existe dans le discord ?
        if client is not None:
            c_player2 = client.get_user(id_joueur2)
            if c_player2 is None:
                raise exceptions.BugDiscordCommunication()
        
        # On crée le fight
        created = self.dataManager.createFight(player1, player2)
        if created:
            await utils.send_direct_message(c_player1, f"[{player1.getNbReceiveFights()}] {player2.name} a reçu l'invitation")
            await utils.send_direct_message(c_player1, f"Choisis : pierre, feuille ou ciseaux")
            await utils.send_direct_message(c_player2, f"[{player2.getNbReceiveFights()}] **{player1.name}** vous a défié")
            await utils.send_direct_message(c_player2, f"Choisis : pierre, feuille, ciseaux")
        else:
            await utils.send_direct_message(c_player1, f"[{player1.getNbReceiveFights()}] Tu as déjà envoyé un duel.")
    
    async def attackRandomPlayer(self, id_player, client):

        # Récupérer le player
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier si le joueur existe
        if player is None:
            raise exceptions.PlayerNotRegistered()
        
        # Choisir un joueur aléatoirement
        players = self.dataManager.players.copy()
        players.remove(player)
        player2 = choice(players)

        # On crée le fight
        await self.attack(id_player, player2.idPlayer, client)

    async def mystats(self, id_player, channel=None):
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier que l'utilisateur existe bien
        if player is None:
            raise exceptions.PlayerNotRegistered()

        # Retourner les stats du joueur
        actif_message = "actif" if player.actif else "passif"
        in_fight_message = "non" if player.sentFight is None else "oui"
        message = "\n".join([
            f"Vos stats {player.name}",
            f"win : {player.nbWin}",
            f"loose : {player.nbLoose}",
            f"Wins consécutives : {player.nbWinCons}",
            f"Looses consécutives : {player.nbLooseCons}",
            f"Wins consécutives MAX : {player.nbWinConsMax}",
            f"Looses consécutives MAX: {player.nbLooseConsMax}",
            f"score : {player.score}",
            f"état du compte : {actif_message}",
            f"combat envoyé ? : {in_fight_message}"
        ])
        await utils.send_message(channel, message)

    async def actionPlayer(self, id_player, action, channel=None, client=None):
        '''
        Réaliser l'action 'pierre' 'feuille' ou 'ciseaux' du joueur
        dans son combat.
        '''
        # Chercher son combat
        player = self.dataManager.getPlayerById(id_player)
        
        if player is None:
            raise exceptions.PlayerNotRegistered()
        
        # A quel combat doit-on faire un choix ?
        fight = None
        if (player.sentFight is not None) and (not player.sentFight.alreadyVote(player)):
            fight = player.sentFight
        else:
            fight = player.getCurrentReceiveFight()
        
        # Si on a déjà fait des choix partout
        if fight is None:
            raise exceptions.AlreadyVotedAll()
        


        # ------ 
                
        # Sinon on peut ajouter l'action
        if fight.player1.idPlayer == id_player:
            fight.actionPlayer1 = action
        else:
            fight.actionPlayer2 = action

        # Qui est le joueur 2
        if id_player == fight.player1.idPlayer:
            id_player2 = fight.player2.idPlayer
            player2 = fight.player2
            player1 = fight.player1
        else:
            id_player2 = fight.player1.idPlayer
            player2 = fight.player1
            player1 = fight.player2

        # Créer le DM de Joueur 1
        c_player2 = None
        if client is not None:
            c_player2 = client.get_user(player2.idPlayer)
        
        # Créer le DM de Joueur 2
        c_player1 = None
        if client is not None:
            c_player1 = client.get_user(player1.idPlayer)
        
        
        # Match terminé maintenant ?
        if self.fightIsFinished(fight):
            # Récupération du winner id et création variable looser is
            winner_id = self.getWinner(fight)
            looser_id = None

            # Cas d'égalité
            if winner_id is None:
                fight.actionPlayer1 = None
                fight.actionPlayer2 = None
                await utils.send_direct_message(c_player1, f"[{player1.getNbReceiveFights()}] Il y a eu égalité avec **{player2.name}** ! Rejouez.")
                await utils.send_direct_message(c_player2, f"[{player2.getNbReceiveFights()}] Il y a eu égalité **{player1.name}**! Rejouez.")
                
            # Cas le combat est fini !
            else:
                # Get winner and looser
                if winner_id == id_player:
                    looser_id = id_player2
                else:
                    looser_id = id_player

                # Get players
                winner_player = self.dataManager.getPlayerById(winner_id)
                looser_player = self.dataManager.getPlayerById(looser_id)

                # Update fight
                fight.winner = winner_player

                # Augmenter les compteurs win et loose
                winner_player.nbWin += 1
                looser_player.nbLoose += 1

                # Gérer les win et loose consécutives
                if winner_player.nbLooseCons > 0:
                    winner_player.nbWinCons = 0
                    winner_player.nbLooseCons = 0
                winner_player.nbWinCons += 1
                if winner_player.nbWinCons > winner_player.nbWinConsMax:
                    winner_player.nbWinConsMax = winner_player.nbWinCons
                
                if looser_player.nbWinCons > 0:
                    looser_player.nbWinCons = 0
                    looser_player.nbLooseCons = 0
                looser_player.nbLooseCons += 1
                if looser_player.nbLooseCons  > looser_player.nbLooseConsMax:
                    looser_player.nbLooseConsMax = looser_player.nbLooseCons

                self.dataManager.endFight(fight)
                self.dataManager.syncRanking()

                # On prépare les messages de win et de loose
                win_message = f"[{winner_player.getNbReceiveFights()}] Vous avez vaincu **{looser_player.name}** !"
                loose_message = f"[{looser_player.getNbReceiveFights()}] Vous avez perdu contre le joueur {winner_player.name} !"

                # Envoyer le message à la bonne personne
                if winner_id == id_player:
                    await utils.send_message(channel, win_message)
                    await utils.send_direct_message(c_player2, loose_message)
                else:
                    await utils.send_message(channel, loose_message)
                    await utils.send_direct_message(c_player2, win_message)
                
                # Management of WallOfPFC
                await self.__wallOfPFC.onWin(fight)

        else:
            await utils.send_direct_message(c_player2, f"[{player2.getNbReceiveFights()}] **{player.name}** a fait son choix")
            await utils.send_direct_message(c_player1, f"[{player1.getNbReceiveFights()}] Nous avons bien reçu votre action")

    async def listPlayers(self, channel=None):
        '''
        Liste les joueurs enregistrés
        '''
        players = self.dataManager.players
        message = "Liste des joueurs : \n"
        for player in players:
            message += player.name
            if player.actif:
                message += ":v:"
            else:
                message += " :sleeping:"
            message += "\n"
        await utils.send_message(channel, message)

    async def listCurrentFights(self, channel=None):
        '''
        Donne la liste des combats en cours à l'utilisateur
        '''
        fights = self.dataManager.getCurrentFights()
        message = "Liste des combats : \n"
        for fight in fights:
            player1 = self.dataManager.getPlayerById(fight.player1.idPlayer)
            player2 = self.dataManager.getPlayerById(fight.player2.idPlayer)

            message += f"{player1.name} versus {player2.name}\n"
        
        await utils.send_message(channel, message)
            
    async def becomePassif(self, id_joueur, channel=None):
        '''
            Devenir passif pour ne plus être attaqué
        '''
        # Récupération du joueur
        player = self.dataManager.getPlayerById(id_joueur)

        # Est-ce que le joueur existe ? 
        if player is None:
            raise exceptions.PlayerNotRegistered()

        # Est-ce que le joueur est actif ?
        if player.actif:
            player.actif = False
            await utils.send_message(channel, "Tu es bien passé en mode passif ! Utilises la commande !actif pour redevenir attaquable. https://thumbs.gfycat.com/PoliteClearBlackfish-size_restricted.gif")
        else:
            raise exceptions.AlreadyPassif()

    async def becomeActif(self, id_joueur, channel=None):
        '''
            Devenir actif pour être à nouveau attaqué
        '''
        # Récupération du joueur
        player = self.dataManager.getPlayerById(id_joueur)

        # Est-ce que le joueur existe ? 
        if player is None:
            raise exceptions.PlayerNotRegistered()

        # Est-ce que le joueur est actif ? 
        if not player.actif:
            player.actif = True
            await utils.send_message(channel, "Tu es bien passé en mode actif ! Utilises la commande !passif pour ne plus être attaqué. https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR5olQJ0iCPut7COcWGoAePC36usg_uE3O8xCYcnp03EPuFz4f9w&s")
        else:
            raise exceptions.AlreadyActif()

    async def cancelFight(self, id_player, client=None, channel=None):
        '''
        '''
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier existence du joueur
        if player is None:
            raise exceptions.PlayerNotRegistered()
        
        # Est-ce qu'il a bien envoyé un combat ?
        if player.sentFight is None:
            raise exceptions.PlayerHasNotSentFight()
        
        # Est-ce que le player 2 existe dans le discord ?
        c_player = None
        if client is not None:
            c_player2 = client.get_user(player.sentFight.player2.idPlayer)
            if c_player2 is None:
                raise exceptions.BugDiscordCommunication()
        
        player.sentFight.cancel = True
        player.sentFight.player2.removeReceiveFight(player.sentFight)
        await utils.send_direct_message(c_player2, f"Le combat avec {player.name} a été annulé.")
        player.sentFight = None
        await utils.send_message(channel, "On a bien supprimé ton combat ! Retourne te battre moussaillon ! https://media.giphy.com/media/ihMKNwb2yPEbWJiAmn/giphy.gif")

    async def changeName(self, name, new_name, channel):
        # Chercher le player avec le nom donné
        player = self.dataManager.getPlayerByName(name)

        # Est-ce que le joueur existe ?
        if player is None:
            raise exceptions.PlayerNotFound(name)

        # Est-ce que le nouveau nom n'existe pas déjà ?
        player_new = self.dataManager.getPlayerByName(new_name)

        if player_new is not None:
            raise exceptions.NameExists(new_name)
        
        # Modifier son nom
        player.name = new_name
        await utils.send_message(channel, f"Le nom du joueur {name} a bien été remplacé par {new_name}")

    async def help(self, channel):

        message = "\n".join([
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

        await utils.send_message(channel, message)

    async def listRanking(self, channel=None):
        '''
            Permet à l'utilisateur de faire lister le classement
        '''
        message = "Le classement : \n"
        for i, player in enumerate(self.dataManager.ranking):
            message += f"({i}) {player.name} avec {player.score} pts\n"
        await utils.send_message(channel, message)

    async def initFights(self, channel=None):
        # Cancel fights
        self.dataManager.fights = []
        
        for key, player in self.dataManager.playersIndexed.items():
            player.inFight = False
        await channel.send("Les combats sont bien réinitialisés !")
        print("Fights init done !")
    
    async def showActifs(self, guild, channel=None):
        message = "Liste des joueurs actifs \n"
        for player in self.dataManager.players:
            c_player = guild.get_member(player.idPlayer)
            print(c_player.status)
            if player.actif and c_player.status == discord.Status.online:
                message += f"{player.name} avec {player.score} pts :v:\n"
        await utils.send_message(channel, message)

    async def nextFights(self, id_player, channel=None):
        # Récupérer le player
        player = self.dataManager.getPlayerById(id_player)

        # Est-ce que le joueur existe ?
        if player is None:
            raise exceptions.PlayerNotRegistered()

        # Lister les combats
        message = "Combat envoyé : "
        if player.sentFight is None:
            message += "Aucun\n"
        else:
            message += f"**{player.sentFight.player2.name}** "
            if player.sentFight.alreadyVote(player):
                message += ":ok_hand:"
            message += "\n"
                
        
        message += "\nCombats reçus :\n"
        if len(player.receiveFights) == 0:
            message += "Il n'y a pas de combats"
        for i, fight in enumerate(player.receiveFights):
            message += f"[{i}] {fight.player1.name} "
            if fight.alreadyVote(player):
                message += ":ok_hand:"
            message += "\n"

        await utils.send_message(channel, message)

    async def showPlayerStats(self, name, channel=None):
        '''
            name : nom du joueur
        '''
        # Récupérer le joueur
        player = self.dataManager.getPlayerByName(name)

        # Est-ce que le joueur existe ?
        if player is None:
            raise exceptions.Player2DoesNotExist(name)
            
        # Afficher les stats
        # Retourner les stats du joueur
        actif_message = "actif" if player.actif else "passif"
        message = "\n".join([
            f"Statistiques de **{name}** : ",
            f"win : {player.nbWin}",
            f"loose : {player.nbLoose}",
            f"Wins consécutives MAX : {player.nbWinConsMax}",
            f"Looses consécutives MAX: {player.nbLooseConsMax}",
            f"score : {player.score}",
            f"état du compte : {actif_message}",
        ])
        await utils.send_message(channel, message)

        

    # Utils
    def fightIsFinished(self, fight):
        '''
            Vérifie si les deux actions ont été remplies et retourne True si le combat est fini, False dans le cas contraire.
        '''
        return not (fight.actionPlayer1 is None or fight.actionPlayer2 is None)
    
    def getWinner(self, fight):
        '''
            action_1: action du player 1
            action_2: action du player 2

            return : return None if not ended

                the id of winner
        '''
        act1 = fight.actionPlayer1
        act2 = fight.actionPlayer2
        key_idj = fight.player1.idPlayer
        key_idj2 = fight.player2.idPlayer
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

    # Load and save methods
    def load_game(self):
        '''
        Charger les données du jeu
        '''
        if os.path.isfile(self.PICKLE_FILE):
            with open(self.PICKLE_FILE, "rb") as f:
                print("Chargement des données")
                self.__dataManager = pickle.load(f)
        self.__dataManager.syncRanking()
        
    def save_game(self):
        '''
        Sauvegarde les données du jeu
        '''
        print("sauvegarde des données")
        with open(self.PICKLE_FILE, "wb") as f:
            pickle.dump(self.__dataManager, f)

