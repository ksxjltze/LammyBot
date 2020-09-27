# bot.py
import os
import asyncio
from datetime import datetime, date, timedelta

from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.target_channel_id = 0

@tasks.loop(hours=24)
async def called_once_a_day():
    if bot.target_channel_id == 0:
        channel = get(bot.get_all_channels(), name='general')
        bot.target_channel_id = channel.id
        print(f"Setting reminder channel to general channel ({channel.id})")

    the_time = datetime.now()

    colosseum_time = datetime(the_time.year, the_time.month, the_time.day, 20)
    time_until_colosseum = colosseum_time - the_time
    time_offset = timedelta(minutes=5)
    time_until_message = time_until_colosseum - time_offset

    hours = time_until_message.total_seconds()//3600
    minutes = (time_until_message.total_seconds()//60) % 60
    seconds = round(time_until_message.total_seconds() - hours * 3600 - minutes * 60)
    print("Reminder Set.")
    print("Waiting for {0:.0f} hours, {1:.0f} minutes, {2} seconds.".format(hours, minutes, seconds))

    await asyncio.sleep(time_until_message.total_seconds())
    message_channel = bot.get_channel(target_channel_id)
    await message_channel.send("@here 5min")

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("\nReady.")
    
@bot.command(name="toggle")
async def toggle_reminders(ctx):
    print(f"Got channel {ctx.channel}")
    if called_once_a_day.is_running():
        called_once_a_day.cancel()
        print("Reminders disabled.")
        await ctx.channel.send("Colosseum reminders are now off.")
    else:
        active = True
        called_once_a_day.start()
        print("Reminders enabled.")
        await ctx.channel.send("Colosseum reminders are now on.")

@bot.command(name="setchannel")
async def set_reminder_channel(ctx, str_channel_id):
    if str_channel_id is None:
        message_channel = ctx.channel
    else:
        channel_id = int(str_channel_id[2:-1])
        message_channel = bot.get_channel(channel_id)

    bot.target_channel_id = message_channel.id
    await ctx.channel.send(f"Reminders have been set to Channel #{message_channel.name}.")
    print(f"Target channel changed to #{message_channel.name} ({message_channel.id})")
    
called_once_a_day.start()
bot.run(TOKEN)