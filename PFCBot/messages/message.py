
import discord
import exceptions

# La fonction pour envoyer des messages
async def send_message(message, channel=None):
    if message.player is not None and message.player.actif is False:
        return None
    
    if message.channel is None:
        if channel is None:
            raise exceptions.channelUndefined()
        else:
            message.channel = channel
    return await message.channel.send(message.content, embed=message.embed)



async def edit_message(message_to_edit, new_message, channel=None):
    '''

    '''
    return await message_to_edit.edit(content=new_message.content, embed=new_message.embed)
    



# Classe mère des messages
class Message(discord.Message):
    '''
        Cette classe permet d'encapsuler des informations pour 
        envoyer des messages à un joueur. On profite de la puissance
        que nous offre discord.Message.
    '''
    __content = ""
    __channel = None
    __embed = None
    __player = None

    def __init__(self):
        self.__content = ""
        self.__channel = None
        self.__embed = None
        self.__player = None
    
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @property
    def channel(self):
        return self.__channel
    
    @channel.setter
    def channel(self, channel):
        self.__channel = channel
    
    @property
    def embed(self):
        return self.__embed
    
    @embed.setter
    def embed(self, embed):
        self.__embed = embed

    @property
    def player(self):
        return self.__player
    
    async def direct_message_to_player(self, player, client):
        '''
            Méthode chainable qui permet de configurer le joueur auquel on 
            souhaite envoyer un message.
        '''
        c_player = client.get_user(player.idPlayer)
        self.__player = player
        if c_player is None:
            print("On a un c_player None")
            return self
        else:
            return await self.direct_message(c_player)

    async def direct_message(self, user):
        '''
            Méthode chainable qui permet de configurer le message pour 
            être envoyé en direct message
        '''
        if user.dm_channel is None:
            await user.create_dm()
        if user.dm_channel is None:
            print("ON a encore un problème ! ")
        self.channel = user.dm_channel
        return self

    async def setPlayer(self, player):
        self.__player = player
        return self
