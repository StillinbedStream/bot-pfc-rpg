
import utils
from PFCBot.messages.message import Message, send_message

class WallOfPFC:
    
    def __init__(self, channel):
        self.__channel = channel
        self.__tiers = sorted([5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], reverse=True)

    async def onWin(self, fight):
        '''
            Cette méthode est appelée dans le cas 
            d'une victoire pour faire remonter des infos.
            (ex : un joueur a plus de 10 victoires d'affilé)
        '''

        # Si le winner a 5 victoires consécutives
        if fight.winner.nbWinCons == 5:
            message = Message()
            message.channel = self.__channel
            message.content = f"<@!{fight.winner.idPlayer}> {fight.winner.name} a gagné 5 parties consécutives ! :raised_hands:"
            await send_message(message)
        
        # Si le looser a 5 défaites consécutives
        if fight.looser.nbLooseCons == 5:
            message = Message()
            message.channel = self.__channel
            message.content = f"<@!{fight.looser.idPlayer}> {fight.looser.name} a perdu 5 parties consécutives ! :thumbsdown:"
            await send_message(message)
        
        # Si c'est notre première victoire 
        if fight.winner.nbWin == 1:
            message = Message()
            message.channel = self.__channel
            message.content = f"<@!{fight.winner.idPlayer}> {fight.winner.name} a gagné sa première victoire ! :baby:"
            await send_message(message)
        
        # Si on atteind un certain nombre de wins:
        for tier in self.__tiers:
            if fight.winner.nbWin == tier:
                message = Message()
                message.channel = self.__channel
                message.content = f"<@!{fight.winner.idPlayer}> {fight.winner.name} a atteind {tier} victoires ! <:stilli2Kawaii:701093440582189056> :muscle:"
                await send_message(message)
        
        # TODO: Si quelqu'un a perdu plus de X fois contre quelqu'un d'autres
    
    async def onRankSync(self, old_ranking, ranking):
        # Est-ce que le player est passé premier ?
            if old_ranking[0] is not ranking[0]:
                message = Message()
                message.channel = self.__channel
                message.content = f"<@!{ranking[0].idPlayer}> est passé premier ! <:stilli2Saintcoussin:707413286848692224> :first_place:"
                await send_message(message)
    
        
    async def onFallEllyss(self, sender, receiver):
        # Si le winner a 5 victoires consécutives
        message = Message()
        message.channel = self.__channel
        message.content = f"<@!{sender.idPlayer}> a FallEllyssé <@!{receiver.idPlayer}> ! <:sip:710591429151555725>"
        await send_message(message)
        