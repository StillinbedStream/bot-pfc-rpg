
from PFCBot.messages.message import Message
import discord

# List commands
class ListPlayers(Message):
    def __init__(self, players, channel=None):
        self.channel = channel

        self.embed = discord.Embed()
        self.embed.title = f"Liste des joueurs"
        self.embed.description="!show-actifs pour lister les joueurs actifs"
        players_names = ""
        players_status = ""
        for player in players:
            players_names += player.name + "\n"
            if player.actif:
                players_status += ":v:\n"
            else:
                players_status += " :sleeping:\n"


        self.embed.add_field(name="name", value=players_names, inline=True)
        self.embed.add_field(name="status", value=players_status, inline=True)
        self.channel = channel

class ListCurrentFights(Message):
    def __init__(self, fights, channel=None):
        self.embed = discord.Embed()
        self.embed.title = "Liste des combats : "
        for fight in fights:
            message += f"{fight.player1.name} versus {fight.player2.name}\n"
        self.embed.description = message
        self.channel = channel

class Ranking(Message):
    def __init__(self, ranking, channel=None):
        self.embed = discord.Embed()
        self.embed.title = "Le classement :"

        players_ranks = ""
        players_names = ""
        players_scores = ""
        for i, player in enumerate(ranking):
            players_ranks += f"({i})\n"
            players_names += f"{player.name} \n"
            players_scores += f"{player.score} pts\n"
        
        self.embed.add_field(name="rank", value=players_ranks, inline=True)
        self.embed.add_field(name="name", value=players_names, inline=True)
        self.embed.add_field(name="score", value=players_scores, inline=True)
        
        self.channel = channel



class ShowActifs(Message):
    def __init__(self, players, guild, channel):
        self.embed = discord.Embed()
        self.embed.title = f"Liste des actifs"
        self.embed.description = ""

        players_names = ""
        players_scores = ""

        for player in players:
            c_player = guild.get_member(player.idPlayer)
            if c_player is None:
                continue
            if player.actif and c_player.status == discord.Status.online:
                players_names += f"{player.name} \n"
                players_scores += f"{player.score} pts\n"
        
        self.embed.add_field(name="name", value=players_names, inline=True)
        self.embed.add_field(name="score", value=players_scores, inline=True)
        
        #self.embed.add_field(name="\u200b", value="\u200b", inline=True)
        #self.embed.description += f"{player.name} avec  :v:\n"
        
        self.channel = channel
