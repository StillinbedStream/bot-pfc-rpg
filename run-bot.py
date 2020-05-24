
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

from discord.ext import commands
from discord import Message



# TODO: - Système de connexion données - Tester les fonctionnalités
# TODO: - Savoir combien de combats il nous reste à répondre

load_dotenv() # Load les variables d'ENV depuis .env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')
WALL_OF_EPICNESS = os.getenv('WALL_OF_EPICNESS')
GUILD_ID = int(os.getenv("GUILD_ID"))
CHAN_INFORMATION = int(os.getenv("CHAN_INFORMATION"))

print("chan_info: ", CHAN_INFORMATION)
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
    await gameManager.load_game()
    if CHAN_INFORMATION > 1:
        print(f"Chan INFORMATION {CHAN_INFORMATION}")
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
async def addWin(ctx, name_player2: is_name, nb_add: int):
    gameManager = system["gameManager"]
    player = gameManager.dataManager.getPlayerByName(name_player2)
    if player is None:
        await ctx.send(f"Le joueur {name_player2} n'existe pas.")
    else:
        player.nbWin += nb_add
        await gameManager.dataManager.syncRanking()
        await ctx.send(f"On a bien ajouté les {nb_add} victoires")


@bot.command(name="mobile")
@commands.dm_only()
async def mobile(ctx):
    gameManager = system["gameManager"]
    message = ctx.message

    await gameManager.mobile(message.author.id, message.channel)
    

@bot.command(name="addpapoules")
@commands.dm_only()
async def addpapoules(ctx, name_player2: is_name, nb_add: int):
    gameManager = system["gameManager"]
    message = ctx.message
    if message.author.id == 143773155549380608:
        await gameManager.addCoins(name_player2, nb_add, message.channel)



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
            if message.content.lower() in ["pierre", "feuille", "ciseaux", "p", "f", "c"]:
                choices={"p":"pierre", "f":"feuille", "c":"ciseaux"}
                action = message.content.lower()
                if action in choices:
                    action = choices[action]
                
                await gameManager.actionPlayer(message.author.id, action, message.channel)
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

bot.run(TOKEN)