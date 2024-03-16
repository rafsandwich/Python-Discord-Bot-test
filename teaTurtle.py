import discord
import asyncio
from discord.ext import commands

# set bot token
TOKEN = '1'

# set channel id
cID = 1

# store ID of last sent reminder message (for deletion)
last_message_id = None

intents = discord.Intents.default()
intents.messages = True

# init bot
bot = commands.Bot(command_prefix='!', intents=intents)

# on ready
async def water_reminder():
    global last_message_id
    await bot.wait_until_ready()
    channel = bot.get_channel(cID)

    while not bot.is_closed():
        if last_message_id:
            # delete previous reminder
            try:
                last_message = await channel.fetch_message(last_message_id)
                await last_message.delete()
            except discord.NotFound:
                pass  # no msg, do nothing

        # send new reminder msg
        new_message = await channel.send("It's time to drink water!")
        last_message_id = new_message.id

        await asyncio.sleep(3600)  # 1 hour

# asynchronous main function
async def main():
    # start reminder loop
    bot.loop.create_task(water_reminder())

    # run bot
    await bot.start(TOKEN)

# run main func
asyncio.run(main())