
import utils

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
            await utils.send_message(self.__channel, f"<@!{fight.winner.idPlayer}> {fight.winner.name} a gagné 5 victoires consécutives ! :raised_hands:")
        
        # Si le looser a 5 défaites consécutives
        if fight.looser.nbLooseCons == 5:
            await utils.send_message(self.__channel, f"<@!{fight.looser.idPlayer}> {fight.looser.name} a perdu 5 victoires consécutives ! :thumbsdown:")
        
        # Si c'est notre première victoire 
        if fight.winner.nbWin == 1:
            await utils.send_message(self.__channel, f"<@!{fight.winner.idPlayer}> {fight.winner.name} a gagné sa première victoire ! :baby:")
        
        # Si on atteind un certain nombre de wins:
        for tier in self.__tiers:
            if fight.winner.nbWin == tier:
                await utils.send_message(self.__channel, f"<@!{fight.winner.idPlayer}> {fight.winner.name} a atteind {tier} victoires ! :stillinkawai: :muscle:")
        
        # TODO: Si quelqu'un a perdu plus de X fois contre quelqu'un d'autres








        #  