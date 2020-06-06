# Official modules
import os
import discord
import pickle
import asyncio
from random import choice

# Personal modules
from PFCBot.core.data import DataManager
import exceptions
import json

# Import des messages
from PFCBot.messages.message import send_message
from PFCBot.messages.message import edit_message
from PFCBot.messages.s0cattack import *
from PFCBot.messages.player import *
from PFCBot.messages.fights import *
from PFCBot.messages.discord_related import *
from PFCBot.messages.others import *
from PFCBot.messages.lists import *
from PFCBot.messages.coins import *
from PFCBot.messages.FallEllyss import *

from PFCBot.core.spell import SpellFactory

def compute_score_player(player):
    '''
    Compute score from player information.
    '''
    return (player.nbWin * 20 - player.nbLoose * 5
            - player.receivedTokens * 5 - player.sentTokens * 1)


# -- GAME MANAGER
class GameManager:
    '''
        Cette classe gère tous les aspects du jeu. Il permet aussi d'envoyer des messages.
    '''
    

    PICKLE_FILE = "data.cornichon"
    DATA_FILE = "data.cornichon.json"

    def __init__(self, wallOfPFC, client=None, guild=None):
        self.__dataManager = DataManager()
        self.__dataManager.wallOfPFC = wallOfPFC
        self.__dataManager.client = client
        self.__dataManager.guild = guild
        
        self.__wallOfPFC = wallOfPFC
        self.__client = client
        self.__guild = guild
    
    # Properties
    @property
    def dataManager(self):
        return self.__dataManager
    
    @property
    def client(self):
        return self.__client
    
    @property
    def guild(self):
        return self.__guild
    


    # Commands
    async def register(self, id_joueur, name, channel=None):
        '''
        Enregistrer un membre dans le jeu
        '''
        
        # Vérifier que le joueur n'existe pas déjà, soit son ID, soit son name, hein FlutterShy !
        player = self.__dataManager.getPlayerById(id_joueur)
        if player is not None:
            return await send_message(PlayerAlreadyRegistered(player, channel))
        
        if self.__dataManager.getPlayerByName(name) is not None:
            return await send_message(NameExists(name, channel))

        message = await self.__dataManager.createPlayer(id_joueur, name)

        if message is None:
            return await send_message(RegisterDone(channel))
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
            return await send_message(PlayerNotRegistered(channel))

        # Est-ce que le joueur 2 existe dans la BDD
        player2 = self.dataManager.getPlayerById(id_joueur2)
        if player2 is None: 
            return await send_message(Player2NotRegistered(channel))

        # Est-ce que le joueur 2 est le joueur 1?
        if player2.idPlayer == player1.idPlayer:
            return await send_message(AttackMySelf(channel))

        # Est-ce que joueur 1 est passif ?
        if player1.actif is False:
            return await send_message(PlayerPassif(channel))

        # Est-ce que joueur 2 est passif ?
        if player2.actif is False:
            return await send_message(Player2Passif(channel))

        # Est-ce que les joueurs 1 et 2 ne se sont pas déjà rencontrés
        player1.synchroniseTimePlayerEncountered()
        enc_1 = player1.playerAlreadyEncountered(player2)
        if enc_1 is not None:
            return await send_message(AlreadyEncountered(player2, int(enc_1.seconds / 60), enc_1.seconds % 60, channel))
        
        # Est-ce que le player 2 existe dans le discord ?
        if self.__client is not None:
            c_player2 = self.__client.get_user(id_joueur2)
            if c_player2 is None:
                return await send_message(BugDiscordCommunication(channel))
        
        # Est-ce que le joueur 1 a déjà attaqué quelqu'un
        if player1.sentFight is None:
            fight = self.dataManager.createFight(player1, player2)

            sentMessagePlayer1 = await send_message(await SentInvite(player1, player2).direct_message(c_player1))
            fight.messagePlayer1 = sentMessagePlayer1 

            if provoc != "":
                await send_message(await Provoc(player1, provoc, provoc_image).direct_message(c_player2))
            
            sentMessagePlayer2 = await send_message(await YouAreAttacked(player1, player2).direct_message(c_player2))
            fight.messagePlayer2 = sentMessagePlayer2

            player1.addPlayerEncountered(player2)
            player2.addPlayerEncountered(player1)
            self.dataManager.indexFight(fight)

            
            await sentMessagePlayer1.add_reaction("✊")
            await sentMessagePlayer1.add_reaction("✋")
            await sentMessagePlayer1.add_reaction("✌️")
            await sentMessagePlayer1.add_reaction("❌")

            await sentMessagePlayer2.add_reaction("✊")
            await sentMessagePlayer2.add_reaction("✋")
            await sentMessagePlayer2.add_reaction("✌️")
        else:
            await send_message(await AlreadySentFight(player1.sentFight).direct_message(c_player1))

    async def attackRandomPlayer(self, id_player, channel=None):
        # Choisir un joueur aléatoirement
        players = [player_ for player_ in self.dataManager.players.copy() if player_.actif and self.__guild.get_member(player_.idPlayer) is not None and self.__guild.get_member(player_.idPlayer).status == discord.Status.online and player_.idPlayer != id_player]
        player2 = choice(players)

        # On crée le fight
        await self.attack(id_player, player2.idPlayer, "", "", channel)

    async def mystats(self, id_player, channel=None):
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier que l'utilisateur existe bien
        if player is None:
            return await send_message(PlayerNotRegistered(channel))

        await send_message(MyStats(player), channel)

    async def actionPlayerOnFight(self, id_player, fight, action, channel=None):

        # Chercher son combat
        player = self.dataManager.getPlayerById(id_player)
        
        if player is None:
            return await send_message(PlayerNotRegistered(channel))
        
        # Si on a déjà fait des choix partout
        if fight is None:
            return await send_message(AlreadyVotedAll(channel))
        
        # Est-ce que le fight est déjà fini ?
        if fight.cancel or fight.winner is not None:
            return
        
        # Est-ce qu'on n'a pas déjà voté ?
        if fight.alreadyVote(player):
            return

        # Créer le DM de Joueur 1
        c_player1 = None
        if self.__client is not None:
            c_player1 = self.__client.get_user(player.idPlayer)
        

        action_to_emot = {
            "pierre": "✊",
            "feuille": "✋",
            "ciseaux": "✌️"
        }
        
        # Sinon on peut ajouter l'action
        if fight.player1.idPlayer == id_player:
            # Envoyé au joueur qui joue
            message_player = await fight.messagePlayer1
            message_player.embeds[0].description += f"\n\n **Vous avez joué** {action_to_emot[action]}"
            await message_player.edit(embed=message_player.embeds[0])

            # Envoyé à l'autre joueur
            message_player = await fight.messagePlayer2
            message_player.embeds[0].description += f"\n\n **L'autre joueur a fait son choix**"
            await message_player.edit(embed=message_player.embeds[0])


            fight.actionPlayer1 = action

        else:
            # Envoyé au joueur qui joue
            message_player = await fight.messagePlayer2
            message_player.embeds[0].description += f"\n\n **Vous avez joué** {action_to_emot[action]}"
            await message_player.edit(embed=message_player.embeds[0])
            
            # Envoyé à l'autre joueur
            message_player = await fight.messagePlayer1
            message_player.embeds[0].description += f"\n\n **L'autre joueur a fait son choix**"
            await message_player.edit(embed=message_player.embeds[0])

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

        # Créer le DM de Joueur 2
        c_player2 = None
        if self.__client is not None:
            c_player2 = self.__client.get_user(player2.idPlayer)
        
        
        # Match terminé maintenant ?
        if fight.isFinished():
            # Récupération du winner id et création variable looser is
            winner_id = fight.computeWinner()
            looser_id = None

            # Cas d'égalité
            if winner_id is None:
                fight.actionPlayer1 = None
                fight.actionPlayer2 = None

                message_player1 = await fight.messagePlayer1
                message_player1.embeds[0].description += f"\n\n **Egalité, veuillez rejouer.** :arrows_counterclockwise:"
                await message_player1.edit(embed=message_player1.embeds[0])

                message_player2 = await fight.messagePlayer2
                message_player2.embeds[0].description += f"\n\n **Egalité, veuillez rejouer.** :arrows_counterclockwise:"
                await message_player2.edit(embed=message_player2.embeds[0])

                #await send_message(await Equality(player1, player2).direct_message(c_player1))
                #await send_message(await Equality(player2, player1).direct_message(c_player2))
                
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

                await self.dataManager.endFight(fight)
                await self.update_ranking()

                # Envoyer le message à la bonne personne
                if winner_id == id_player:
                    if winner_player.signature != "":
                        await send_message(await SignatureWinMessage(winner_player, looser_player).direct_message(c_player2))
                else:
                    if winner_player.signature != "":
                        await send_message(await SignatureWinMessage(winner_player, looser_player).direct_message(c_player1))
                
                message_winner = await fight.messageWinner
                message_winner.embeds[0].description += f"\n\n **Tu as gagné contre {looser_player.name} !** :partying_face:"

                message_looser = await fight.messageLooser
                message_looser.embeds[0].description += f"\n\n **Tu as perdu contre {winner_player.name} !** :poop: "

                await message_winner.edit(embed=message_winner.embeds[0])
                await message_looser.edit(embed=message_looser.embeds[0])
                

                # Management of WallOfPFC
                await self.__wallOfPFC.onWin(fight)
        pass

    async def actionPlayer(self, id_player, action, channel=None):
        '''
        Réaliser l'action 'pierre' 'feuille' ou 'ciseaux' du joueur
        dans son combat.
        '''
        # Chercher son combat
        player = self.dataManager.getPlayerById(id_player)
        
        if player is None:
            return await send_message(PlayerNotRegistered(channel))
        
        # A quel combat doit-on faire un choix ?
        fight = None
        if (player.sentFight is not None) and (not player.sentFight.alreadyVote(player)):
            fight = player.sentFight
        else:
            fight = player.getCurrentReceivedFight()
        
        await self.actionPlayerOnFight(id_player, fight, action)
    
    async def listPlayers(self, id_player, channel=None):
        '''
        Liste les joueurs enregistrés
        '''
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifie que le joueur existe
        if player is None:
            return await send_message(PlayerNotRegistered(channel))
        
        players = self.dataManager.players
        await send_message(ListPlayers(player, players, self.guild, channel))

    async def listCurrentFights(self, channel=None):
        '''
        Donne la liste des combats en cours à l'utilisateur
        '''
        fights = self.dataManager.getCurrentFights()
        
        await send_message(ListCurrentFights(fights), channel)
            
    async def becomePassif(self, id_joueur, channel=None):
        '''
            Devenir passif pour ne plus être attaqué
        '''
        # Récupération du joueur
        player = self.dataManager.getPlayerById(id_joueur)

        # Est-ce que le joueur existe ? 
        if player is None:
            return await send_message(PlayerNotRegistered(channel))

        # Est-ce que le joueur est actif ?
        if player.actif:
            player.actif = False
            await send_message(BecomePassif(channel))
        else:
            await send_message(AlreadyPassif(channel))

    async def becomeActif(self, id_joueur, channel=None):
        '''
            Devenir actif pour être à nouveau attaqué
        '''
        # Récupération du joueur
        player = self.dataManager.getPlayerById(id_joueur)

        # Est-ce que le joueur existe ? 
        if player is None:
            return await send_message(PlayerNotRegistered(channel))

        # Est-ce que le joueur est actif ? 
        if not player.actif:
            player.actif = True
            return await send_message(BecomeActif(channel))
        else:
            return await send_message(AlreadyActif(channel))

    async def cancelFight(self, id_player, channel=None):
        '''
        '''
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier existence du joueur
        if player is None:
            return await send_message(PlayerNotRegistered(channel))
        
        # Est-ce qu'il a bien envoyé un combat ?
        if player.sentFight is None:
            return await send_message(PlayerHasNotSentFight(channel))
        
        # Est-ce que le player 2 existe dans le discord ?
        if self.__client is not None:
            c_player2 = self.__client.get_user(player.sentFight.player2.idPlayer)
            if c_player2 is None:
                return await send_message(BugDiscordCommunication())
        
        fight_to_cancel = player.sentFight
        await self.dataManager.endFight(fight_to_cancel)

        # Editer le message de l'expéditeur (sender)
        message_player1 = await fight_to_cancel.messagePlayer1
        if message_player1 is not None:
            message_player1.embeds[0].description += f"\n\n **Tu as annulé le duel ! :x:**"
            await message_player1.edit(embed=message_player1.embeds[0])

        # Editer le message du receptionneur (receiver)
        message_player2 = await fight_to_cancel.messagePlayer2
        if message_player2 is not None:
            message_player2.embeds[0].description += f"\n\n **Le combat a été annulé ! :x:**"
            await message_player2.edit(embed=message_player2.embeds[0])


    async def changeName(self, name, new_name, channel=None):
        # Chercher le player avec le nom donné
        player = self.dataManager.getPlayerByName(name)

        # Est-ce que le joueur existe ?
        if player is None:
            return await send_message(PlayerNotFound(name, channel))

        # Est-ce que le nouveau nom n'existe pas déjà ?
        player_new = self.dataManager.getPlayerByName(new_name)

        if player_new is not None:
            return await send_message(NameExists(new_name, channel))
        
        # Modifier son nom
        self.dataManager.changeName(player, new_name)
        await send_message(NameChanged(name, new_name, channel))

    async def help(self, channel):
        await send_message(Help(channel))

    async def listRanking(self, id_player, channel=None):
        '''
            Permet à l'utilisateur de faire lister le classement
        '''
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifie que le joueur existe
        if player is None:
            return await send_message(PlayerNotRegistered(channel))

        await send_message(Ranking(player, self.dataManager.ranking, self.__guild, channel))

    async def initFights(self, channel=None):
        # Cancel fights
        self.dataManager.fights = []
        
        for player in self.dataManager.players:
            player.initFights()
        
        await send_message(FightsInit(channel))
    
    async def showActifs(self, id_player, channel=None):
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifie que le joueur existe
        if player is None:
            return await send_message(PlayerNotRegistered(channel))
        
        await send_message(ShowActifs(player, self.dataManager.players, self.__guild, channel))

    async def nextFights(self, id_player, channel=None):
        # Récupérer le player
        player = self.dataManager.getPlayerById(id_player)

        # Est-ce que le joueur existe ?
        if player is None:
            return await send_message(PlayerNotRegistered(channel))

        print("Next fights : " + player.receivedFightsIds())
        await send_message(NextFights(player, channel))

    async def showPlayerStats(self, name, channel=None):
        '''
            name : nom du joueur
        '''
        # Récupérer le joueur
        player = self.dataManager.getPlayerByName(name)

        # Est-ce que le joueur existe ?
        if player is None:
            return await send_message(Player2DoesNotExist(channel))
        
        await send_message(PlayerStats(player, channel))
        
    async def use_spell(self, spell, id_player, channel=None, *args):
        
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)
        
        # Vérifier que le joueur existe
        if player is None:
            return await send_message(PlayerNotRegistered(channel))
        
        spell = SpellFactory().getSpell(spell)
        spell.user = player
        spell.arguments = spell.Arguments(*args)
        spell.gameManager = self
        spell.dataManager = self.dataManager
        if await spell.checkUsable(channel):
            await spell.use(channel)
        
    async def fallEllyss(self, id_player, name_player2, channel=None):
        # Variables
        nbFightsEffect = 5
        price = 15

        # Récupérer le joueur 1
        player1 = self.dataManager.getPlayerById(id_player)

        # Vérifier que le joueur 1 existe
        if player1 is None:
            return await send_message(PlayerNotRegistered(channel))
        
        # Récupérer le joueur 2
        player2 = self.dataManager.getPlayerByName(name_player2)

        # Vérifier que le joueur 2 existe
        if player2 is None:
            return await send_message(Player2DoesNotExist(name_player2))

        # last fights of player 2
        fights = self.dataManager.getLastWinsOfPlayer(player2)


        # Si le joueur n'a pas assez de combats de gagnés
        if len(fights) < nbFightsEffect:
            # On doit envoyer un message pour dire que le joueur n'a pas assez de fights gagnés.
            return await send_message(FallEllyssNotEnoughWin(nbFightsEffect, player2, channel))
        
        fights = fights[-nbFightsEffect:]

        # Est-ce que le joueur a assez de papoules ?
        if player1.coins < price:
            return await send_message(NotEnoughCoins(player1, price, channel))



        for fight in fights:
            fight.winner.nbWin -= 1
            fight.looser.nbLoose -= 1
            fight.cancel = True
            # Envoyer un message comme quoi votre fight a été fallEllyssé ?
        
        # On enlève les coins
        player1.coins -= price

        
        await self.update_ranking()
        # Créer le DM de Joueur 1
        c_player2 = None
        if self.__client is not None:
            c_player2 = self.__client.get_user(player2.idPlayer)
        
        # Créer le DM de Joueur 2
        c_player1 = None
        if self.__client is not None:
            c_player1 = self.__client.get_user(player1.idPlayer)
        
        # Envoyer un message au player 1
        await send_message(await FallEllyssDone(player1, player2).direct_message(c_player1))
        # Envoyer un message au player 2
        await send_message(await FallEllyssed(player1, player2).direct_message(c_player2))
        
        await self.__wallOfPFC.onFallEllyss(player1, player2)

    async def signature(self, id_player, signature, signature_image = "", channel=None):
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Est-ce que le joueur existe ?
        if player is None:
            return await send_message(PlayerNotRegistered(channel))
        
        # On peut modifier sa signature
        player.signature = signature
        player.signatureImage = signature_image
        await send_message(SignatureModified(channel))

    async def mysignature(self, id_player, channel=None):
        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Vérifier que le joueur existe
        if player is None:
            return send_message(PlayerNotRegistered(channel))
        
        # Envoyer la signature au joueur
        await send_message(ShowSignature(player, channel))

    async def mobile(self, id_player, channel=None):

        # Récupérer le joueur
        player = self.dataManager.getPlayerById(id_player)

        # Est-ce qu'il existe ?
        if player is None:
            return await send_message(PlayerNotRegistered(channel))
        
        player.mobile = not player.mobile
        await send_message(MobileChanged(player, channel))

    async def addCoins(self, name_player2, nb_add, channel=None):
        # Récupérer le joueur
        player2 = self.dataManager.getPlayerByName(name_player2)

        # Est-ce que le joueur existe ?
        if player2 == None:
            return await send_message(Player2NotRegistered(channel))
        
        # Est-ce que le player 2 existe dans le discord ?
        c_player2 = None
        if self.__client is not None:
            c_player2 = self.__client.get_user(player2.idPlayer)
            if c_player2 is None:
                return await send_message(BugDiscordCommunication(channel))

        # On ajoute les coins 
        player2.coins += nb_add

        await send_message(AddCoinsMessage(player2, nb_add, channel))

        await send_message(await IncreasedCoins(player2, nb_add).direct_message(c_player2))
        
    async def update_ranking(self):
        await self.dataManager.syncRanking()
        await self.update_ranking_message()
    
    # Messages
    async def update_ranking_message(self):
        '''
        This function update the ranking message.
        An other way to programme it could be to have a list of messages to update.
        '''

        # Si le chan information n'est pas modifié, on ne fait rien
        if self.dataManager.channelInformation == None:
            return
        else:
            # Sinon, on vérifie si un identifiant de message existe déjà ou si le message n'est pas dans le chan
            if await self.dataManager.rankingMessage == None:
                # Il faut alors créer le message
                self.dataManager.rankingMessage = await send_message(OfficialRanking(self.dataManager.ranking, self.guild, self.dataManager.channelInformation))
                print("Message envoyé parce qu'il n'existait pas déjà.")
            # Sinon le message existe
            else:
                try:
                    # mettre à jour le message
                    await edit_message(await self.dataManager.rankingMessage, OfficialRanking(self.dataManager.ranking, self.guild))
                    print("Message mis à jour")
                except discord.errors.NotFound as e:
                    print("Le message n'a pas été trouvé !")
                    pass

    async def init_messages(self, id_info_channel):
        await self.update_ranking_message()
        pass

    # Load and save methods
    async def load_game(self):
        '''
        Charger les données du jeu
        '''
        if os.path.isfile(self.DATA_FILE):
            await self.dataManager.load_json(self.DATA_FILE, self.client)
        
    def save_game(self):
        '''
        Sauvegarde les données du jeu
        '''
        self.dataManager.save_json(self.DATA_FILE)


