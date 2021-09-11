# bot.py
import os
import pandas as pd 
import time 
import json

import validators

from csv import writer
from datetime import datetime
import youtube_dl

import psycopg2
from sqlalchemy import create_engine

import discord
from discord.ext import commands

from dotenv import load_dotenv
import re

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
LINKS = os.getenv('LINKS')
VC_CHANNEL = int(os.getenv('VC_ID'))

bot = commands.Bot(command_prefix='!')


DATABASE_URL = os.environ['DATABASE_URL_SQL']
engine = create_engine(DATABASE_URL, echo = False)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=os.getenv('STATUS_MESSAGE')))

@bot.command(name='serena')
@commands.cooldown(1, 5, commands.BucketType.user)
async def on_message(ctx, *, arg):

    url = ctx.message.content
    url = url.strip('!serena ')

    splitted_msg = arg.split(" ")
    text = ""

    yt_links = json.loads(LINKS)

    for key, value in yt_links.items():
        if(splitted_msg[0] == key):
            url = value

    if(splitted_msg[0] == 'help'):
        text = os.getenv('HELPER_MESSAGE')
        text += "\nMes commandes audio :\n"

        for key, value in yt_links.items():
            text += key + "\n"
        

        await ctx.send(text)

    elif(splitted_msg[0] == 'rules34'):
        for i in range(0, 3):
            await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    elif(validators.url(url)):
        voice_channel = bot.get_channel(VC_CHANNEL)
        await voice_channel.connect()

        server = ctx.message.guild
        voice_channel = server.voice_client

        filename = await YTDLSource.from_url(url, loop=bot.loop)
        voice_channel.play(discord.FFmpegPCMAudio(source=filename))

        while voice_channel.is_playing():
            time.sleep(1)
        await voice_channel.disconnect()

    else:
        channel_id = ""
        if(int(splitted_msg[-1])):
            nb_times = int(splitted_msg[-1])
        else:
            nb_times = 1

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

    
    

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

bot.run(TOKEN)