import discord
import asyncio
from discord.ext import commands

# set bot token
TOKEN = '1'

# set channel id
cID = 1

# store ID of last sent reminder message (for deletion)
lastMsgID = None

intents = discord.Intents.default()
intents.messages = True

# init bot
bot = commands.Bot(command_prefix='!', intents=intents)

# send reminder
async def water_reminder():
    global lastMsgID
    await bot.wait_until_ready()
    channel = bot.get_channel(cID)

    while not bot.is_closed():
        if lastMsgID:
            # delete previous reminder
            try:
                last_message = await channel.fetch_message(lastMsgID)
                await last_message.delete()
            except discord.NotFound:
                pass  # no msg, do nothing

        # send new reminder msg
        new_message = await channel.send("~ ding ding tea time ~")
        lastMsgID = new_message.id

        await asyncio.sleep(36)  # 1 hour

@bot.event
async def on_ready():
    print(f'{bot.user} is ready to go at a leisurely pace')
    bot.loop.create_task(water_reminder())  # start reminder loop on ready

# run bot
bot.run(TOKEN)