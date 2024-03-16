import discord
import asyncio
from discord.ext import commands
import datetime

# set bot token
TOKEN = '1'

# set channel id
cID = 1

# store ID of last sent reminder message (for deletion)
lastMsgID = None

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# init bot
bot = commands.Bot(command_prefix='!', intents=intents)

# calc time to next hour
# def calc_next_hour():
#     now = datetime.datetime.now()
#     nextHour = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)
#     return (nextHour - now).total_seconds()

def calc_next_hour():
    now = datetime.datetime.now()
    nextHour = now.replace(hour=(now.hour + 1) % 24, minute=0, second=0, microsecond=0)
    timeToNextHour = (nextHour - now).total_seconds()
    return timeToNextHour # handle wrapping around if function is started at 23:00




# calculate next reminder time
# def calc_next_reminder():
#     now = datetime.datetime.now()
#     return now + datetime.timedelta(minutes=(5 - now.minute % 5)) # every 5 mins 

# def calc_next_reminder():
#     now = datetime.datetime.now()
#     return now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0) # every hour

def calc_next_reminder():
    now = datetime.datetime.now()
    if now.minute < 30:
        return now.replace(minute=30, second=0, microsecond=0)
    else:
        return now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0) # every half hour

# send reminder
async def water_reminder():
    global lastMsgID
    await bot.wait_until_ready()
    channel = bot.get_channel(cID)

    while not bot.is_closed():
        # calc time until first reminder
        nextReminder = calc_next_hour()

        # wait until init reminder
        await asyncio.sleep(nextReminder)
        
        # start sending every 5 mins
        while True:
            # calc time until next reminder
            nextReminderTime = calc_next_reminder()
            nextReminder = (nextReminderTime - datetime.datetime.now()).total_seconds()

            # wait until next reminder
            await asyncio.sleep(nextReminder)
        
            if lastMsgID:
                # try delete previous reminder
                try:
                    last_message = await channel.fetch_message(lastMsgID)
                    await last_message.delete()
                except discord.NotFound:
                    pass  # no msg, do nothing

            # send new reminder msg
            new_message = await channel.send("~ ding ding tea time ~")
            lastMsgID = new_message.id

            #await asyncio.sleep(3600)  # 1 hour || redundant if using next reminder calculator

@bot.event
async def on_ready():
    print(f'{bot.user} is ready to go at a leisurely pace')
    bot.loop.create_task(water_reminder())  # start reminder loop on ready

# run bot
bot.run(TOKEN)