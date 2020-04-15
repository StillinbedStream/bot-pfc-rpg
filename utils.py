
async def send_direct_message(player, message):
    if player is None:
        print(message)
    else:
        if player.dm_channel is None:
            await player.create_dm()
        await player.dm_channel.send(message)

async def send_message(channel, message):
    '''
    Envois un message, soit au channel donné, soit en print si le channel est None.
    '''
    if channel is None:
        print(message)
    else:
        await channel.send(message)

