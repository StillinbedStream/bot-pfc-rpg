
import discord
import exceptions

# La fonction pour envoyer des messages
async def send_message(message, channel=None):
    if message.channel is None:
        if channel is None:
            raise exceptions.channelUndefined()
        else:
            message.channel = channel
    await message.channel.send(message.content, embed=message.embed)

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

    def __init__(self):
        self.__content = ""
        self.__channel = None
        self.__embed = None
    
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
    
    async def direct_message(self, user):
        '''
            Méthode chainable qui permet de configurer le message pour 
            être envoyé en direct message
        '''
        if user.dm_channel is None:
            await user.create_dm()
        self.channel = user.dm_channel
        return self
