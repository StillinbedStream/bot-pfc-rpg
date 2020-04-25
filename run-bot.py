
import os
import random
import discord
import asyncio 
import exceptions
import wall

from discord.ext import commands
from dotenv import load_dotenv
from engine import GameManager


from discord.ext import commands
from discord import Message

# TODO: - Système de connexion données - Tester les fonctionnalités
# TODO: - Savoir combien de combats il nous reste à répondre

load_dotenv() # Load les variables d'ENV depuis .env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')
WALL_OF_EPICNESS = os.getenv('WALL_OF_EPICNESS')
GUILD_ID = int(os.getenv("GUILD_ID"))

# Préparation client et variables
bot = commands.Bot(command_prefix="!")




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
    gameManager.load_game()
    system["gameManager"] = gameManager








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
async def change_name(ctx, name: str, new_name: str):
    gameManager = system["gameManager"]
    message = ctx.message
    if message.author.id == 143773155549380608:
        await gameManager.changeName(name, new_name, message.channel)

# Liste des joueurs
@bot.command(name='players')
@commands.dm_only()
async def list_players(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.listPlayers(message.channel)
    gameManager.save_game()


# Enregistrement d'un joueur
@bot.command(name='register')
@commands.dm_only()
async def register(ctx, name: str):
    if len(name) > 15:
        return
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.register(message.author.id, name, message.channel)
    gameManager.save_game()



@bot.command(name='attack')
@commands.dm_only()
async def attack(ctx, name_player2: str = "", provoc: str = ""):
    
    if name_player2 == "":
        return
    if len(name_player2) > 15:
        return
    
    # Attaque
    gameManager = system["gameManager"]
    message = ctx.message
    player2 = gameManager.dataManager.getPlayerByName(name_player2)
    if player2 == None:
        await message.channel.send(f"Le joueur {name_player2} n'existe pas, comme ton charisme ! https://gifimage.net/wp-content/uploads/2017/08/popopo-gif-1.gif")
    else:
        await gameManager.attack(message.author.id, player2.idPlayer, provoc, message.channel)
    gameManager.save_game()
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
    await gameManager.listRanking(message.channel)


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
    gameManager.save_game()


@bot.command(name='cancel')
@commands.dm_only()
async def cancel(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.cancelFight(message.author.id, message.channel)
    gameManager.save_game()

@bot.command(name='show-actifs')
@commands.dm_only()
async def show_actifs(ctx):
    gameManager = system["gameManager"]
    message = ctx.message
    await gameManager.showActifs(message.channel)
    gameManager.save_game()


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
    await gameManager.s0command(message.author.id, name_player2, message.channel)



#@bot.command(name='help')
# @commands.dm_only()
# async def help(ctx):
#     gameManager = system["gameManager"]
#     message = ctx.message
#     await gameManager.help(message.channel)



# !quit command
            

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

            # choose action
            if message.content.lower() in ["pierre", "feuille", "ciseaux"]:
                 await gameManager.actionPlayer(message.author.id, message.content, message.channel)
                 return gameManager.save_game()

            if message.content == "!test":
                print("Player dict: ", gameManager.dataManager.getPlayerById(message.author.id).dump_dict())
                return
            #     embed = discord.Embed()
            #     embed.title = "Simple test !"
            #     embed.type = "rich"
            #     embed.description = "Un petite description"
            #     embed.add_field(name="Message", value="Enregistrements", inline=True)
            #     embed.add_field(name="Function", value="Des trucs de ouf", inline=True)
            #     embed.add_field(name="Message", value="Enregistrements", inline=False)
            #     return await message.channel.send(embed=embed)
        await bot.process_commands(message)


bot.run(TOKEN)