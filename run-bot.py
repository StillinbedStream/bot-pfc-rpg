# bot.py
import os
import random
import discord
import asyncio 
import exceptions

from discord.ext import commands
from dotenv import load_dotenv

from engine import GameManager

# TODO:  - Système de connexion données - Tester les fonctionnalités


load_dotenv() # Load les variables d'ENV depuis .env
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv('DISCORD_GUILD')
ID_CHANNEL = os.getenv('ID_CHANNEL')


gameManager = GameManager()
client = discord.Client()

data = {
    "users": {},
    "combats": [],
    "ids": {
        "combats": 0
    }
}

gameManager.load_game()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_disconnect():
    print("Déconnexion du BOT")
    gameManager.save_game()

@client.event
async def on_message(message):

    lock = asyncio.Lock()

    async with lock:
        try:

            if message.author == client.user:
                return

            # Dans le cas où on est dans un MP (DM)
            if isinstance(message.channel, discord.DMChannel):

                # !quit command
                if message.content == "!quit" and message.author.id == 143773155549380608:
                    await client.close()

                # !quit command
                if message.content == "!init-fights" and message.author.id == 143773155549380608:
                    await gameManager.initFights(message.channel)
                
                # !rename player command
                if message.content.startswith("!change-name") and message.author.id == 143773155549380608:
                    splited = message.content.split(" ")
                    if splited[0] == "!change-name" and len(splited) > 2:
                        name = splited[1]
                        new_name = splited[2]
                        await gameManager.changeName(name, new_name, message.channel)


                # choose action
                if message.content.lower() in ["pierre", "feuille", "ciseaux"]:
                    await gameManager.actionPlayer(message.author.id, message.content, message.channel, client)

                # Enregistrement d'un joueur
                if message.content.startswith("!register"):
                    splited = message.content.split(" ")
                    if splited[0] == "!register":
                        if len(splited) > 1:
                            name = splited[1]
                            await gameManager.register(message.author.id, name, message.channel)
                        else:
                            await message.channel.send("Il faut écrire !register [mon pseudo] imbécile ! (sans le imbécile, imbécile)")

                    
                
                # Liste des joueurs
                if message.content == "!players":
                    await gameManager.listPlayers(message.channel)
                

                # Attaque
                if message.content.startswith("!attack"):
                    splited = message.content.split(" ")
                    if splited[0] == "!attack":
                        if len(splited) > 1:
                            name_player2 = splited[1]
                            player2 = gameManager.dataManager.getPlayerByName(name_player2)
                            if player2 == None:
                                await message.channel.send(f"Le joueur {name_player2} n'existe pas, comme ton charisme ! https://gifimage.net/wp-content/uploads/2017/08/popopo-gif-1.gif")
                            else:
                                await gameManager.attack(message.author.id, player2.idPlayer, client)


                # Current fights
                if message.content == "!current-fights":
                    await gameManager.listCurrentFights(message.channel)
            
                # Mes statistiques
                if message.content == "!mystats":
                    await gameManager.mystats(message.author.id, message.channel)

                # Classement
                if message.content == "!ranking":
                    await gameManager.listRanking(message.channel)
                
                # Devenir passif
                if message.content == "!passif":
                    await gameManager.becomePassif(message.author.id, message.channel)
                
                # Devenir actif
                if message.content == "!actif":
                    await gameManager.becomeActif(message.author.id, message.channel)

                # Arrêter son combat
                if message.content == "!cancel":
                    await gameManager.cancelFight(message.author.id, message.channel)
                
                # Montrer les actifs
                if message.content == "!show-actifs":
                    await gameManager.showActifs(message.channel)

                if message.content == "!show-availables":
                    await gameManager.showAvailables(message.channel)
                
                # Message d'aide
                if message.content == "!help":
                    await gameManager.help(message.channel)
        except exceptions.ExceptionToUser as e:
            print(e.stringOutput)
            if e.messageToUser.channel is None:
                await message.channel.send(e.messageToUser.content)
            else:
                await e.messageToUser.channel.send(e.messageToUser.content)

client.run(TOKEN)