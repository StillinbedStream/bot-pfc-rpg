
import os
import random
import discord
import asyncio 
import exceptions
from PFCBot.core import wall

from discord.ext import commands
from dotenv import load_dotenv
from PFCBot.core.engine import GameManager
from PFCBot.commands.converters import is_name
from PFCBot.messages.message import send_message
from PFCBot.messages.player import PlayerNotRegistered

from discord import Message

from PFCBot.commands.admin import AdminCommands 


# TODO: - Système de connexion données - Tester les fonctionnalités
# TODO: - Savoir combien de combats il nous reste à répondre

load_dotenv() # Load les variables d'ENV depuis .env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')
WALL_OF_EPICNESS = os.getenv('WALL_OF_EPICNESS')
GUILD_ID = int(os.getenv("GUILD_ID"))
CHAN_INFORMATION = int(os.getenv("CHAN_INFORMATION"))

# Préparation client et variables
bot = commands.Bot(command_prefix="!")
bot.add_cog(AdminCommands(bot))




system = {
    "gameManager": None
}

# -- ON READY
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Une fois qu'on est co, on crée le jeu
    wall_of_epicness_channel = bot.get_channel(int(WALL_OF_EPICNESS))
    if wall_of_epicness_channel is None:
        raise Exception("On n'a pas trouvé le channel wall of PFC")

    gameManager = GameManager(wall.WallOfPFC(wall_of_epicness_channel), bot, bot.get_guild(GUILD_ID))
    await gameManager.load_game()
    if CHAN_INFORMATION > 1:
        await gameManager.init_messages(CHAN_INFORMATION)
    
    system["gameManager"] = gameManager






# -- Caritatif commands
@bot.command(name="leplusbeau")
@commands.dm_only()
async def leplusbeau(ctx):
    await ctx.send("Le plus beau c'est <@289061712043442176>")



# -- COMMANDS
@bot.command(name='quit')
@commands.dm_only()
async def quit(ctx):
    message = ctx.message
    if message.author.id == 143773155549380608:
        await bot.close()

@bot.command(name='init-fights')
@commands.dm_only()
async def init_fights(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    if message.author.id == 143773155549380608:
        await gameManager.initFights(message.channel)
        gameManager.save_game()

@bot.command(name='change-name')
@commands.dm_only()
async def change_name(ctx, name, new_name: is_name):
    gameManager = system["gameManager"]
    message = ctx.message
    #if name == "" or new_name == "":
    #    await ctx.message.channel.send("Les noms données ne doivent pas dépasser les 25 caractères. Les caractères spéciaux sont interdits.")
    #    pass
    if message.author.id == 143773155549380608:
        await gameManager.changeName(name, new_name, message.channel)

# Liste des joueurs
@bot.command(name='players')
@commands.dm_only()
async def list_players(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.listPlayers(message.author.id, message.channel)


# Enregistrement d'un joueur
@bot.command(name='register')
@commands.dm_only()
async def register(ctx, name: is_name):
    #if name == "":
    #    await ctx.message.channel.send("Le nom que vous donnez ne doit pas dépasser les 25 caractères et les caractères spéciaux sont interdits.")
    #    pass
    if name=="idolon" and ctx.message.author.id != 143773155549380608:
        return
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.register(message.author.id, name, message.channel)
    gameManager.save_game()



@bot.command(name='attack')
@commands.dm_only()
async def attack(ctx, name_player2: is_name = "", provoc: str = "", provoc_image: str=""):
    
    gameManager = system["gameManager"]
    message = ctx.message
    if name_player2 == "":
        await gameManager.attackRandomPlayer(message.author.id, message.channel)
        return
    
    # Attaque
    player2 = gameManager.dataManager.getPlayerByName(name_player2)
    if player2 == None:
        await message.channel.send(f"Le joueur {name_player2} n'existe pas, comme ton charisme ! https://gifimage.net/wp-content/uploads/2017/08/popopo-gif-1.gif")
    else:
        await gameManager.attack(message.author.id, player2.idPlayer, provoc, provoc_image, message.channel)
    #elif len(splited) == 1:
    #await gameManager.attackRandomPlayer(message.author.id, message.channel)



# Current fights
@bot.command(name='current-fights')
@commands.dm_only()
async def current_fights(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.listCurrentFights(message.channel)


@bot.command(name='mystats')
@commands.dm_only()
async def mystats(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.mystats(message.author.id, message.channel)


@bot.command(name='ranking')
@commands.dm_only()
async def ranking(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.listRanking(message.author.id, message.channel)


@bot.command(name='passif')
@commands.dm_only()
async def passif(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.becomePassif(message.author.id, message.channel)
    gameManager.save_game()



@bot.command(name='actif')
@commands.dm_only()
async def actif(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.becomeActif(message.author.id, message.channel)

@bot.command(name='cancel')
@commands.dm_only()
async def cancel(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.cancelFight(message.author.id, message.channel)

@bot.command(name='show-actifs')
@commands.dm_only()
async def show_actifs(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.showActifs(message.author.id, message.channel)


@bot.command(name='myfights')
@commands.dm_only()
async def myfights(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.nextFights(message.author.id, message.channel)
    

@bot.command(name='show-stats')
@commands.dm_only()
async def showStats(ctx, name_player2: str):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.showPlayerStats(name_player2, message.channel)


@bot.command(name='s0cattack')
@commands.dm_only()
async def s0command(ctx, name_player2: str):
    gameManager = system["gameManager"]
    message = ctx.message
    #await gameManager.s0command(message.author.id, name_player2, message.channel)
    await gameManager.use_spell('s0cattack', message.author.id, message.channel, name_player2)

@bot.command(name="fallellyss")
@commands.dm_only()
async def fallelyss(ctx, name_player2: is_name):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.fallEllyss(message.author.id, name_player2, message.channel)


@bot.command(name='signature')
@commands.dm_only()
async def signature(ctx, signature: str, signature_image: str = ""):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.signature(message.author.id, signature, signature_image, message.channel)


@bot.command(name='mysignature')
@commands.dm_only()
async def mysignature(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.mysignature(message.author.id, message.channel)


@bot.command(name="addwin")
@commands.dm_only()
@commands.is_owner()
async def addWin(ctx, name_player2: is_name, nb_add: int):
    gameManager = system["gameManager"]
    player = gameManager.dataManager.getPlayerByName(name_player2)
    if player is None:
        await ctx.send(f"Le joueur {name_player2} n'existe pas.")
    else:
        player.nbWin += nb_add
        await gameManager.update_ranking()
        await ctx.send(f"On a bien ajouté les {nb_add} victoires")


@bot.command(name="mobile")
@commands.dm_only()
async def mobile(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.mobile(message.author.id, message.channel)
    

@bot.command(name="addpapoules")
@commands.dm_only()
@commands.is_owner()
async def addpapoules(ctx, name_player2: is_name, nb_add: int):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.addCoins(name_player2, nb_add, message.channel)


@bot.command(name="set-chan-info")
@commands.dm_only()
@commands.is_owner()
async def setChannelInformation(ctx, channel_id: int):
    gameManager = system["gameManager"]
    channel = gameManager.dataManager.setChannelInformationWithId(channel_id)
    if channel is None:
        await ctx.channel.send("Le channel d'information n'a pas été trouvé dans la guilde.")
    else:
        await ctx.channel.send("Le channel d'information a bien été configuré")


@bot.command(name="reset-fights")
@commands.dm_only()
@commands.is_owner()
async def resetFights(ctx):
    gameManager = system["gameManager"]
    gameManager.dataManager.resetFights()
    await ctx.channel.send("Les combats ont bien été reset ! ")

    
@bot.command(name="set-pillow-knight-role")
@commands.dm_only()
@commands.is_owner()
async def pillowKnightRoleId(ctx, role_id: int):
    gameManager = system["gameManager"]
    try:
        await gameManager.dataManager.setPillowKnightRoleId(role_id)
        await ctx.channel.send("Le rôle a bien été modifié !")
    except Exception as e:
        await ctx.channel.send("Un problème est survenu, le rôle n'a pas été modifié. L'identifiant fourni est sûrement invalide.")
        print(e)

@bot.command(name="check-pillow-knight-role")
@commands.dm_only()
@commands.is_owner()
async def checkPillowKnightRole(ctx):
    gameManager = system["gameManager"]
    pillow_knight_role = gameManager.guild.get_role(gameManager.dataManager.pillowKnightRoleId)
    if pillow_knight_role is None:
        await ctx.channel.send("Le rôle n'a pas été trouvé")
    else:
        await ctx.channel.send(f"On a bien trouvé le rôle Pillow Knight : {pillow_knight_role.name}")


@bot.command(name="identity")
@commands.is_owner()
async def identity(ctx, name: is_name):
    gameManager = system["gameManager"]
    player = gameManager.dataManager.getPlayerByName(name)

    if player is None:
        await ctx.channel.send("Le joueur n'a pas été trouvé")
    else:
        await ctx.channel.send(f"Le joueur {name} est le suivant : <@{player.idPlayer}>")

@bot.event
async def on_disconnect():
    print("Déconnexion du BOT")
    gameManager = system["gameManager"]
    gameManager.save_game()

@bot.event
async def on_message(message):
    lock = asyncio.Lock()
    async with lock:

        gameManager = system["gameManager"]
        if message.author == bot.user:
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
                await gameManager.actionPlayer(message.author.id, action, message.channel)
                return gameManager.save_game()


        elif message.content.startswith("!") :
            await message.channel.send(f"Pour jouer au jeu, il faut m'envoyer un Direct Message (DM) <@{bot.user.id}>")
        
        await bot.process_commands(message)





@change_name.error
async def info_error_change_name(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(error)
    else:
        await ctx.send(error)

@register.error
async def info_error_register(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(error)



@bot.event
async def on_raw_reaction_add(payload):
    '''
    payload.guild_id == None
    payload.user_id # Pour vérifier que c'est bien l'utilisateur
    payload.message_id # Pour vérifier que c'est bien sur un message d'un fight.
    name
    '''
    gameManager = system["gameManager"]

    if payload.guild_id == None and payload.user_id != bot.user.id:
        
        # Envoie la réaction
        actions = {
            "✊": "pierre",
            "✋": "feuille",
            "✌️": "ciseaux"
        }

        player_c = bot.get_user(payload.user_id)
        if player_c.dm_channel is None:
            await player_c.create_dm()
        player_c.dm_channel
        
        
        if payload.user_id != bot.user.id and payload.emoji.name in actions:
            # On vérifie si c'est un message d'un fight.
            fight = gameManager.dataManager.getFightByMessageId(payload.message_id)
            if fight is None:
                return
            action = actions[payload.emoji.name]
            
            await gameManager.actionPlayerOnFight(payload.user_id, fight, action, bot.get_channel(player_c.dm_channel))
        
        if payload.user_id != bot.user.id and payload.emoji.name == "❌":
            fight = gameManager.dataManager.getFightByMessageId(payload.message_id)
            if fight is None:
                return
            
            if fight.player1.idPlayer == payload.user_id and fight.player1.sentFight is fight:
                await gameManager.cancelFight(payload.user_id, bot.get_channel(payload.channel_id))

bot.run(TOKEN)
