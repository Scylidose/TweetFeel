# bot.py
import os
import pandas as pd 

from csv import writer
from datetime import datetime

import psycopg2
from sqlalchemy import create_engine


import discord
from discord.ext import commands

from dotenv import load_dotenv
import re

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


DATABASE_URL = os.environ['DATABASE_URL_SQL']
engine = create_engine(DATABASE_URL, echo = False)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=os.getenv('STATUS_MESSAGE')))

@bot.command(name='serena')
@commands.cooldown(1, 5, commands.BucketType.user)
async def on_message(ctx, *, arg):
    splitted_msg = arg.split(" ")
    text = ""

    if(splitted_msg[0] == 'help'):
        text = os.getenv('HELPER_MESSAGE')

        await ctx.send(text)
    
    else:
        channel_id = ""
        nb_times = int(splitted_msg[-1])
        real_nb_times = nb_times
        flood_channel_id = discord.utils.get(ctx.guild.channels, name=os.getenv('FLOOD_CHANNEL_NAME'))
        if(flood_channel_id):
            flood_channel_id = flood_channel_id.id
        else:
            flood_channel_id = ""

        current_channel = str(ctx.message.channel)
        

        if splitted_msg[-2].find("#") != -1 and splitted_msg[-2][-1] != "\"":
            channel_id = splitted_msg[-2]
        

        if channel_id != "":
            channel_id = int(str(channel_id).replace('#', '').replace("<", "").replace(">", "").replace(" ", ""))

            channel = bot.get_channel(channel_id)

        if channel_id == "":
            if nb_times > 3 and discord.utils.get(ctx.guild.channels, name=current_channel).id != flood_channel_id:
                nb_times = 3
        else:
            if nb_times > 3 and flood_channel_id != channel_id:
                nb_times = 3

        if nb_times > 50:
            nb_times = 50

        quoted = re.compile('"[^"]*"')
        for value in quoted.findall(arg):
            text += value

        text = text.replace('\"', '')

        dataset = pd.DataFrame(
            {
            'action_mode': 'Ajout',
            'caller': str(ctx.message.author),
            'text': text,
            'nb_times': real_nb_times,
            'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }, index=[0])

        dataset.to_sql('serena', con = engine, if_exists='append')

        for i in range(0, nb_times):
            if channel_id == "":
                await ctx.send(text)
            else:
                await channel.send(text)


bot.run(TOKEN)