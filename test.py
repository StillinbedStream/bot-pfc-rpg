
from engine import GameManager

import asyncio


async def main():
    gameManager = GameManager()
    await gameManager.register(1023, "idolon")
    await gameManager.register(4302, "fluttershy")
    await gameManager.register(23048, "fluttershy")
    await gameManager.register(1023, "trucmachinchose")
    await gameManager.register(1023, "idolon")
    await gameManager.attack(1023, 4302)
    await gameManager.attack(1023, 4302)
    await gameManager.attack(4302, 1023)
    await gameManager.listCurrentFights()

    await gameManager.actionPlayer(1023, "pierre")
    await gameManager.actionPlayer(1023, "pierre")
    await gameManager.actionPlayer(1023, "ciseaux")
    await gameManager.actionPlayer(4302, "ciseaux")
    await gameManager.attack(4302, 1023)

    await gameManager.listCurrentFights()
    await gameManager.mystats(1023)
    await gameManager.mystats(4302)

    await gameManager.listRanking()




loop = asyncio.get_event_loop()
loop.run_until_complete(main())
