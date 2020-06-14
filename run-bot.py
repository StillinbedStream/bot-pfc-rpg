
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
from PFCBot.commands.basic import BasicCommands
from PFCBot.commands.profil import ProfilCommands
from PFCBot.commands.spells import SpellsCommands
from PFCBot.commands.fun import FunCommands

load_dotenv() # Load les variables d'ENV depuis .env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv("GUILD_ID"))

# Préparation client et variables
print(GUILD_ID)
bot = commands.Bot(command_prefix="!")
gameManager = GameManager(bot)


# Ajout des cogs
bot.add_cog(AdminCommands(bot, gameManager))
bot.add_cog(BasicCommands(bot, gameManager))
bot.add_cog(ProfilCommands(bot, gameManager))
bot.add_cog(SpellsCommands(bot, gameManager))
bot.add_cog(FunCommands(bot))


# -- ON READY
@bot.event
async def on_ready():
    gameManager.guild = bot.get_guild(GUILD_ID)
    await gameManager.load_game()
    await gameManager.init_messages()
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_disconnect():
    print("Déconnexion du BOT")
    global gameManager
    gameManager.save_game()
    print("Les données ont été sauvegardées")


bot.run(TOKEN)
