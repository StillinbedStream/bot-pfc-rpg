from discord.ext import commands
from PFCBot.commands.converters import is_name
from PFCBot.core.engine import GameManager

class AdminCommands(commands.Cog):
    def __init__(self, bot, game_manager: GameManager):
        self.bot = bot
        self.game_manager = game_manager
    
    # -- QUIT
    @commands.command(name='quit')
    @commands.dm_only()
    @commands.is_owner()
    async def quit(self, ctx):
        await self.bot.close()



    # CHANGE NAME
    @commands.command(name='change-name')
    @commands.dm_only()
    @commands.is_owner()
    async def change_name(self, ctx, name, new_name: is_name):
        await self.game_manager.changeName(name, new_name, ctx.message.channel)


    @change_name.error
    async def info_error_change_name(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
        else:
            await ctx.send(error)



    @commands.command(name="addwin")
    @commands.dm_only()
    @commands.is_owner()
    async def addWin(self, ctx, name_player2: is_name, nb_add: int):
        player = self.game_manager.dataManager.getPlayerByName(name_player2)
        if player is None:
            await ctx.send(f"Le joueur {name_player2} n'existe pas.")
        else:
            player.nbWin += nb_add
            await self.game_manager.update_ranking()
            await ctx.send(f"On a bien ajouté les {nb_add} victoires")

    @commands.command(name="addpapoules")
    @commands.dm_only()
    @commands.is_owner()
    async def addpapoules(self, ctx, name_player2: is_name, nb_add: int):
        await self.game_manager.addCoins(name_player2, nb_add, ctx.channel)


    # INIT FIGHTS
    @commands.command(name='init-fights')
    @commands.dm_only()
    @commands.is_owner()
    async def init_fights(self, ctx):
        await self.game_manager.initFights(ctx.message.channel)
        self.game_manager.save_game()

    # RESET FIGHTS
    @commands.command(name="reset-fights")
    @commands.dm_only()
    @commands.is_owner()
    async def resetFights(self, ctx):
        self.game_manager.dataManager.resetFights()
        await ctx.channel.send("Les combats ont bien été reset ! ")

    
    # IDENTITY
    @commands.command(name="identity")
    @commands.is_owner()
    async def identity(self, ctx, name: is_name):
        player = self.game_manager.dataManager.getPlayerByName(name)

        if player is None:
            await ctx.channel.send("Le joueur n'a pas été trouvé")
        else:
            await ctx.channel.send(f"Le joueur {name} est le suivant : <@{player.idPlayer}>")

        
    # SET PILLOW KNIGHT ROLE
    @commands.command(name="set-pillow-knight-role")
    @commands.dm_only()
    @commands.is_owner()
    async def pillowKnightRoleId(self, ctx, role_id: int):
        try:
            await self.game_manager.dataManager.setPillowKnightRoleId(role_id)
            await ctx.channel.send("Le rôle a bien été modifié !")
        except Exception as e:
            await ctx.channel.send("Un problème est survenu, le rôle n'a pas été modifié. L'identifiant fourni est sûrement invalide.")
            print(e)


    # CHECK PILLOW KNIGHT ROLE
    @commands.command(name="check-pillow-knight-role")
    @commands.dm_only()
    @commands.is_owner()
    async def checkPillowKnightRole(self, ctx):
        pillow_knight_role = self.game_manager.guild.get_role(self.game_manager.dataManager.pillowKnightRoleId)
        if pillow_knight_role is None:
            await ctx.channel.send("Le rôle n'a pas été trouvé")
        else:
            await ctx.channel.send(f"On a bien trouvé le rôle *Pillow Knight* : **{pillow_knight_role.name}**")



    
        
    # SET POPULACE ROLE
    @commands.command(name="set-populace-role")
    @commands.dm_only()
    @commands.is_owner()
    async def populaceRoleId(self, ctx, role_id: int):
        try:
            await self.game_manager.dataManager.setPopulaceRoleId(role_id)
            await ctx.channel.send("Le rôle a bien été modifié !")
            print(self.game_manager.dataManager.populaceRoleId)
        except Exception as e:
            await ctx.channel.send("Un problème est survenu, le rôle n'a pas été modifié. L'identifiant fourni est sûrement invalide.")
            print(e)


    # CHECK PILLOW KNIGHT ROLE
    @commands.command(name="check-populace-role")
    @commands.dm_only()
    @commands.is_owner()
    async def checkPopulaceRole(self, ctx):
        populace_role = self.game_manager.guild.get_role(self.game_manager.dataManager.populaceRoleId)
        if populace_role is None:
            await ctx.channel.send("Le rôle n'a pas été trouvé")
        else:
            await ctx.channel.send(f"On a bien trouvé le rôle *Populace* : **{populace_role.name}**")

    # SET CHAN INFO
    @commands.command(name="set-chan-info")
    @commands.dm_only()
    @commands.is_owner()
    async def setChannelInformation(self, ctx, channel_id: int):
        channel = self.game_manager.dataManager.setChannelInformationWithId(channel_id)
        if channel is None:
            await ctx.channel.send("Le channel d'information n'a pas été trouvé dans la guilde.")
        else:
            await ctx.channel.send("Le channel d'information a bien été configuré")


    # SET WALL OF EPICNESS
    @commands.command(name='set-wall-of-epicness')
    @commands.dm_only()
    @commands.is_owner()
    async def setWallOfEpicness(self, ctx, channel_id: int):
        pass
