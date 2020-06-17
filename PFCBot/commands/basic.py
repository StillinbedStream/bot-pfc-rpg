from discord.ext import commands
from PFCBot.commands.converters import is_name
from PFCBot.core.engine import GameManager
import asyncio
import discord

class BasicCommands(commands.Cog):
    '''
    Basic Play regroupe toutes les commandes les plus basiques : 
    - register
    - attack
    - cancel
    - show-actifs
    - ranking
    - players
    - mystats
    '''
    def __init__(self, bot, game_manager: GameManager):
        self.bot = bot
        self.game_manager = game_manager

    
    # Enregistrement d'un joueur
    @commands.command(name='register')
    @commands.dm_only()
    async def register(self, ctx, name: is_name):
        if name.lower()=="idolon" or name.lower()=="stillinbed" and ctx.message.author.id != 143773155549380608:
            return
        await self.game_manager.register(ctx.message.author.id, name, ctx.channel)
        self.game_manager.save_game()

    @register.error
    async def info_error_register(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)

    @commands.command(name='attack', aliases=['a'])
    @commands.dm_only()
    async def attack(self, ctx, name_player2: is_name = "", provoc: str = "", provoc_image: str=""):
        message = ctx.message
        if name_player2 == "":
            await self.game_manager.attackRandomPlayer(message.author.id, channel=message.channel)
            return
        
        # Attaque
        player2 = self.game_manager.dataManager.getPlayerByName(name_player2)
        if player2 == None:
            await message.channel.send(f"Le joueur {name_player2} n'existe pas, comme ton charisme ! https://gifimage.net/wp-content/uploads/2017/08/popopo-gif-1.gif")
        else:
            await self.game_manager.attack(message.author.id, player2.idPlayer, provoc, provoc_image, channel=message.channel)
    



    # Liste des joueurs
    @commands.command(name='players')
    @commands.dm_only()
    async def list_players(self, ctx):
        await self.game_manager.listPlayers(ctx.message.author.id, ctx.channel)
    


    @commands.command(name='mystats', aliases=['ms'])
    @commands.dm_only()
    async def mystats(self, ctx):
        await self.game_manager.mystats(ctx.message.author.id, ctx.channel)

    
    

    @commands.command(name='ranking')
    @commands.dm_only()
    async def ranking(self, ctx):
        await self.game_manager.listRanking(ctx.message.author.id, ctx.channel)



    @commands.command(name='passif')
    @commands.dm_only()
    async def passif(self, ctx):
        await self.game_manager.becomePassif(ctx.message.author.id, ctx.channel)
        self.game_manager.save_game()


    @commands.command(name='actif')
    @commands.dm_only()
    async def actif(self, ctx):
        await self.game_manager.becomeActif(ctx.message.author.id, ctx.channel)

    @commands.command(name='cancel')
    @commands.dm_only()
    async def cancel(self, ctx):
        await self.game_manager.cancelFight(ctx.message.author.id, ctx.channel)

    @commands.command(name='show-actifs')
    @commands.dm_only()
    async def show_actifs(self, ctx):
        await self.game_manager.showActifs(ctx.message.author.id, ctx.channel)

    @commands.command(name='myfights', aliases=["mf"])
    @commands.dm_only()
    async def myfights(self, ctx):
        await self.game_manager.nextFights(ctx.message.author.id, ctx.channel)
        
    
    
    @commands.command(name='show-stats')
    @commands.dm_only()
    async def showStats(self, ctx, name_player2: str):
        await self.game_manager.showPlayerStats(name_player2, ctx.channel)

    @commands.Cog.listener()
    @commands.dm_only()
    async def on_message(self, message):
        lock = asyncio.Lock()
        async with lock:
            if message.author == self.bot.user:
                return
            
            # Dans le cas où on est dans un MP (DM)
            if isinstance(message.channel, discord.DMChannel):
                
                
                choices={
                    "pierre": "pierre",
                    "feuille": "feuille",
                    "ciseaux": "ciseaux",
                    "p":"pierre",
                    "f":"feuille",
                    "c":"ciseaux",
                    "✊": "pierre",
                    "✋": "feuille",
                    "✌️": "ciseaux"
                }

                action = message.content.lower()
                if action in choices.keys():
                    action = choices[action]
                    await self.game_manager.actionPlayer(message.author.id, action, message.channel)
                    return self.game_manager.save_game()


            elif message.content.startswith("!") :
                await message.channel.send(f"Pour jouer au jeu, il faut m'envoyer un Direct Message (DM) <@{self.bot.user.id}>")
            
            #await self.bot.process_commands(message)


    
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        '''
        payload.guild_id == None
        payload.user_id # Pour vérifier que c'est bien l'utilisateur
        payload.message_id # Pour vérifier que c'est bien sur un message d'un fight.
        name
        '''
        if payload.guild_id == None and payload.user_id != self.bot.user.id:
            
            # Envoie la réaction
            actions = {
                "✊": "pierre",
                "✋": "feuille",
                "✌️": "ciseaux"
            }

            player_c = self.bot.get_user(payload.user_id)
            if player_c.dm_channel is None:
                await player_c.create_dm()
            player_c.dm_channel
            
            
            if payload.user_id != self.bot.user.id and payload.emoji.name in actions:
                # On vérifie si c'est un message d'un fight.
                fight = self.game_manager.dataManager.getFightByMessageId(payload.message_id)
                if fight is None:
                    return
                action = actions[payload.emoji.name]
                
                await self.game_manager.actionPlayerOnFight(payload.user_id, fight, action, self.bot.get_channel(player_c.dm_channel))
            
            if payload.user_id != self.bot.user.id and payload.emoji.name == "❌":
                fight = self.game_manager.dataManager.getFightByMessageId(payload.message_id)
                if fight is None:
                    return
                
                if fight.player1.idPlayer == payload.user_id and fight.player1.sentFight is  fight:
                    await self.game_manager.cancelFight(payload.user_id, self.bot.get_channel(payload.channel_id))
