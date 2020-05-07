# Official modules
import os
import discord
import pickle
import asyncio
from random import choice

# Personal modules
from data import DataManager
import messages
import exceptions
from messages import send_message
import json

# -- GAME MANAGER
class GameManager:
    '''
        Cette classe gère tous les aspects du jeu. Il permet aussi d'envoyer des messages.
    '''
    

    PICKLE_FILE = "data.cornichon"
    DATA_FILE = "data.cornichon.json"

    def __init__(self, wallOfPFC, client=None, guild=None):
        self.__dataManager = DataManager()
        self.__wallOfPFC = wallOfPFC
        self.__client = client
        self.__guild = guild
    
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
            return await send_message(messages.PlayerAlreadyRegistered(player, channel))
        
        if self.__dataManager.getPlayerByName(name) is not None:
            return await send_message(messages.NameExists(name, channel))

        message = self.__dataManager.createPlayer(id_joueur, name)

        if message is None:
            return await send_message(messages.RegisterDone(channel))
        else:
            message.channel = channel
            await send_message(message)

    async def attack(self, id_joueur1, id_joueur2, provoc, provoc_image, channel=None):
        '''
        Attaquer un joueur
        '''
        # On récupère le player 1 du client
        c_player1 = None
        c_player2 = None
        if self.__client is not None:
            c_player1 = self.__client.get_user(id_joueur1)

        # Est-ce que le joueur 1 existe dans BDD ? 
        player1 = self.dataManager.getPlayerById(id_joueur1)
        if player1 is None:
            return await send_message(messages.PlayerNotRegistered(channel))

        # Est-ce que le joueur 2 existe dans la BDD
        player2 = self.dataManager.getPlayerById(id_joueur2)
        if player2 is None: 
            return await send_message(messages.Player2NotRegistered(channel))

        # Est-ce que le joueur 2 est le joueur 1?
        if player2.idPlayer == player1.idPlayer:
            return await send_message(messages.AttackMySelf(channel))

        # Est-ce que joueur 1 est passif ?
        if player1.actif is False:
            return await send_message(messages.PlayerPassif(channel))

        # Est-ce que joueur 2 est passif ?
        if player2.actif is False:
            return await send_message(messages.Player2Passif(channel))

        # Est-ce que les joueurs 1 et 2 ne se sont pas déjà rencontrés
        player1.synchroniseTimePlayerEncountered()
        enc_1 = player1.playerAlreadyEncountered(player2)
        if enc_1 is not None:
            return await send_message(messages.AlreadyEncountered(player2, int(enc_1.seconds / 60), enc_1.seconds % 60, channel))
        
        # Est-ce que le player 2 existe dans le discord ?
        if self.__client is not None:
            c_player2 = self.__client.get_user(id_joueur2)
            if c_player2 is None:
                return await send_message(messages.BugDiscordCommunication(channel))
        
        # Est-ce que le joueur 1 a déjà attaqué quelqu'un
        if player1.sentFight is None:
            self.dataManager.createFight(player1, player2)
            await send_message(await messages.SentInvite(player1, player2).direct_message(c_player1))
            await send_message(await messages.DoTheChoice().direct_message(c_player1))
            if provoc != "":
                await send_message(await messages.Provoc(player1, provoc, provoc_image).direct_message(c_player2))
            await send_message(await messages.YouAreAttacked(player1, player2).direct_message(c_player2))
            await send_message(await messages.DoTheChoice().direct_message(c_player2))
            player1.addPlayerEncountered(player2)
            player2.addPlayerEncountered(player1)
        else:
            await send_message(await messages.AlreadySentFight(player1.sentFight).direct_message(c_player1))

    async def attackRandomPlayer(self, id_player, channel=None):
        # Choisir un joueur aléatoirement
        players = [player_ for player_ in self.dataManager.players.copy() if player_.actif and self.__guild.get_member(player_.idPlayer).status == discord.Status.online and player_.idPlayer != id_player]
        player2 = choice(players)

        # On crée le fight
        await self.attack(id_player, player2.idPlayer, channel)

    async def mystats(self, id_player, channel=None):
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier que l'utilisateur existe bien
        if player is None:
            return await send_message(messages.PlayerNotRegistered(channel))

        await messages.send_message(messages.MyStats(player), channel)

    async def actionPlayer(self, id_player, action, channel=None):
        '''
        Réaliser l'action 'pierre' 'feuille' ou 'ciseaux' du joueur
        dans son combat.
        '''
        # Chercher son combat
        player = self.dataManager.getPlayerById(id_player)
        
        if player is None:
            return await send_message(messages.PlayerNotRegistered(channel))
        
        # A quel combat doit-on faire un choix ?
        fight = None
        if (player.sentFight is not None) and (not player.sentFight.alreadyVote(player)):
            fight = player.sentFight
        else:
            fight = player.getCurrentReceivedFight()
        
        # Si on a déjà fait des choix partout
        if fight is None:
            return await send_message(messages.AlreadyVotedAll(channel))
                
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
        if self.__client is not None:
            c_player2 = self.__client.get_user(player2.idPlayer)
        
        # Créer le DM de Joueur 2
        c_player1 = None
        if self.__client is not None:
            c_player1 = self.__client.get_user(player1.idPlayer)
        
        
        # Match terminé maintenant ?
        if fight.isFinished():
            # Récupération du winner id et création variable looser is
            winner_id = fight.computeWinner()
            looser_id = None

            # Cas d'égalité
            if winner_id is None:
                fight.actionPlayer1 = None
                fight.actionPlayer2 = None
                await send_message(await messages.Equality(player1, player2).direct_message(c_player1))
                await send_message(await messages.Equality(player2, player1).direct_message(c_player2))
                
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
                
                winner_player.coins += 1

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

                # Envoyer le message à la bonne personne
                if winner_id == id_player:
                    await send_message(await messages.WinMessage(winner_player, looser_player).direct_message(c_player1))
                    await send_message(await messages.LooseMessage(winner_player, looser_player).direct_message(c_player2))
                    await send_message(await messages.SignatureWinMessage(winner_player, looser_player).direct_message(c_player2))
                else:
                    await send_message(await messages.WinMessage(winner_player, looser_player).direct_message(c_player2))
                    await send_message(await messages.LooseMessage(winner_player, looser_player).direct_message(c_player1))
                    await send_message(await messages.SignatureWinMessage(winner_player, looser_player).direct_message(c_player1))
                
                # Management of WallOfPFC
                await self.__wallOfPFC.onWin(fight)

        else:
            await send_message(await messages.PlayerMadeChoice(player1, player2).direct_message(c_player2))
            await send_message(await messages.ActionReceived(player2).direct_message(c_player1))

    async def listPlayers(self, channel=None):
        '''
        Liste les joueurs enregistrés
        '''
        players = self.dataManager.players
        await send_message(messages.ListPlayers(players, channel))

    async def listCurrentFights(self, channel=None):
        '''
        Donne la liste des combats en cours à l'utilisateur
        '''
        fights = self.dataManager.getCurrentFights()
        
        await send_message(messages.ListCurrentFights(fights), channel)
            
    async def becomePassif(self, id_joueur, channel=None):
        '''
            Devenir passif pour ne plus être attaqué
        '''
        # Récupération du joueur
        player = self.dataManager.getPlayerById(id_joueur)

        # Est-ce que le joueur existe ? 
        if player is None:
            return await send_message(messages.PlayerNotRegistered(channel))

        # Est-ce que le joueur est actif ?
        if player.actif:
            player.actif = False
            await send_message(messages.BecomePassif(channel))
        else:
            await send_message(messages.AlreadyPassif(channel))

    async def becomeActif(self, id_joueur, channel=None):
        '''
            Devenir actif pour être à nouveau attaqué
        '''
        # Récupération du joueur
        player = self.dataManager.getPlayerById(id_joueur)

        # Est-ce que le joueur existe ? 
        if player is None:
            return await send_message(messages.PlayerNotRegistered(channel))

        # Est-ce que le joueur est actif ? 
        if not player.actif:
            player.actif = True
            return await send_message(messages.BecomeActif(channel))
        else:
            return await send_message(messages.AlreadyActif(channel))

    async def cancelFight(self, id_player, channel=None):
        '''
        '''
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier existence du joueur
        if player is None:
            return await send_message(messages.PlayerNotRegistered(channel))
        
        # Est-ce qu'il a bien envoyé un combat ?
        if player.sentFight is None:
            return await send_message(messages.PlayerHasNotSentFight(channel))
        
        # Est-ce que le player 2 existe dans le discord ?
        if self.__client is not None:
            c_player2 = self.__client.get_user(player.sentFight.player2.idPlayer)
            if c_player2 is None:
                return await send_message(messages.BugDiscordCommunication())
        
        player.sentFight.cancel = True
        player.sentFight.player2.removeReceivedFight(player.sentFight)
        await send_message(await messages.FightCanceledByPlayer1(player).direct_message(c_player2))
        player.sentFight = None
        await send_message(messages.FightCanceled(channel))

    async def changeName(self, name, new_name, channel):
        # Chercher le player avec le nom donné
        player = self.dataManager.getPlayerByName(name)

        # Est-ce que le joueur existe ?
        if player is None:
            return await send_message(messages.PlayerNotFound(name, channel))

        # Est-ce que le nouveau nom n'existe pas déjà ?
        player_new = self.dataManager.getPlayerByName(new_name)

        if player_new is not None:
            return await send_message(messages.NameExists(new_name, channel))
        
        # Modifier son nom
        self.dataManager.__players_ind_name.pop(player.name, None)
        player.name = new_name
        self.dataManager.__players_ind_name[player.name] = player
        await send_message(messages.NameChanged(name, new_name, channel))

    async def help(self, channel):
        await send_message(messages.Help(channel))

    async def listRanking(self, channel=None):
        '''
            Permet à l'utilisateur de faire lister le classement
        '''
        await send_message(messages.Ranking(self.dataManager.ranking, channel))

    async def initFights(self, channel=None):
        # Cancel fights
        self.dataManager.fights = []
        
        for player in self.dataManager.players:
            player.initFights()
        
        await send_message(messages.FightsInit(channel))
    
    async def showActifs(self, channel=None):
        await send_message(messages.ShowActifs(self.dataManager.players, self.__guild, channel))

    async def nextFights(self, id_player, channel=None):
        # Récupérer le player
        player = self.dataManager.getPlayerById(id_player)

        # Est-ce que le joueur existe ?
        if player is None:
            return await send_message(messages.PlayerNotRegistered(channel))

        await send_message(messages.NextFights(player, channel))

    async def showPlayerStats(self, name, channel=None):
        '''
            name : nom du joueur
        '''
        # Récupérer le joueur
        player = self.dataManager.getPlayerByName(name)

        # Est-ce que le joueur existe ?
        if player is None:
            return await send_message(messages.Player2DoesNotExist(channel))
        
        await send_message(messages.PlayerStats(player, channel))

    async def s0command(self, id_player, name_player2, channel=None):

        s0ca_price = 1
        # Est-ce que le joueur 1 existe ?
        player1 = self.dataManager.getPlayerById(id_player)

        # Est-ce que le joueur 1 existe ?
        if player1 is None:
            return await send_message(messages.PlayerNotRegistered(channel))

        # Chercher le joueur 2
        player2 = self.dataManager.getPlayerByName(name_player2)

        # Est-ce que le joueur 2 existe ?
        if player2 is None:
            return await send_message(messages.Player2DoesNotExist(name_player2, channel))

        # Est-ce qu'on a suffisamment de coin pour lancer une s0ckattack ?
        if player1.coins < s0ca_price:
            return await send_message(messages.NotEnoughCoins(s0ca_price, channel))
        # On ajoute les tokens
        player1.sentTokens += 1
        player2.receivedTokens += 1
        
        # Créer le DM de Joueur 1
        c_player2 = None
        if self.__client is not None:
            c_player2 = self.__client.get_user(player2.idPlayer)
        
        # Créer le DM de Joueur 2
        c_player1 = None
        if self.__client is not None:
            c_player1 = self.__client.get_user(player1.idPlayer)

        # Vérifier que le score des joueurs ne puisse pas être négatif
        if player1.score < 0 or player2.score < 0:
            player1.sentTokens -= 1
            player2.receivedTokens -= 1
            await send_message(await messages.TokenNotSentCauseNegativeScore().direct_message(c_player1))
        else:
            player1.coins -= s0ca_price
            await send_message(await messages.TokenSent(player2).direct_message(c_player1))
            await send_message(await messages.TokenReceived(player1).direct_message(c_player2))
        
        self.dataManager.syncRanking()
        
    async def signature(self, id_player, signature, channel=None):
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Est-ce que le joueur existe ?
        if player is None:
            return await send_message(messages.PlayerNotRegistered(channel))
        
        # On peut modifier sa signature
        player.signature = signature
        await send_message(messages.SignatureModified(channel))

    async def mysignature(self, id_player, channel=None):
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier que le joueur existe
        if player is None:
            return send_message(messages.PlayerNotRegistered(channel))
        
        # Envoyer la signature au joueur
        await messages.send_message(messages.ShowSignature(player.signature, channel))



    # Load and save methods
    def load_game(self):
        '''
        Charger les données du jeu
        '''
        if os.path.isfile(self.DATA_FILE):
            self.dataManager.load_json(self.DATA_FILE)
        
    def save_game(self):
        '''
        Sauvegarde les données du jeu
        '''
        self.dataManager.save_json(self.DATA_FILE)


