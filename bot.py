# bot.py
import os
import asyncio
from datetime import datetime, date, timedelta

from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
target_channel_id = 743370043508916236

@tasks.loop(hours=24)
async def called_once_a_day():
    the_time = datetime.now()

    colosseum_time = datetime(the_time.year, the_time.month, the_time.day, 20)
    time_until_colosseum = colosseum_time - the_time
    time_offset = timedelta(minutes=5)
    time_until_message = time_until_colosseum - time_offset

    hours = time_until_message.total_seconds()//3600
    minutes = (time_until_message.total_seconds()//60) % 60
    seconds = round(time_until_message.total_seconds() - hours * 3600 - minutes * 60)
    print("Waiting for {0:.0f} hours, {1:.0f} minutes, {2} seconds.".format(hours, minutes, seconds))

    await asyncio.sleep(time_until_message.total_seconds())
    message_channel = bot.get_channel(target_channel_id)
    print(f"Got channel {message_channel}")
    await message_channel.send("@here 5min")

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")
    
called_once_a_day.start()
bot.run(TOKEN)