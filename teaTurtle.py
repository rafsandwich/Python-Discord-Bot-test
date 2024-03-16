import discord
import asyncio
from discord.ext import commands

# set bot token
TOKEN = '###'

# init bot
bot = commands.Bot(command_prefix='!')

# on ready
@bot.event
async def on_ready():
    print(f'{bot.user} is logged in and ready')

# hydrate prompt
async def water_reminder():
    await bot.wait_until_ready()
    channel = bot.get_channel(your_channel_id)  # server channel id

    while not bot.is_closed():
        await channel.send("It's time to drink water!")
        await asyncio.sleep(3600)  # 1 hour

# start reminder loop
bot.loop.create_task(water_reminder())

# run bot
bot.run(TOKEN)