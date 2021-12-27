import discord
from discord.ext import commands, tasks
from discord.utils import get
from icecream import ic
from showerHelper import *
from dotenv import load_dotenv
import os

bot = commands.Bot(command_prefix="!") #create bot client

load_dotenv() #load env file
TOKEN = os.getenv("TOKEN") #get token from .env file

@bot.event # Log in
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) #print load message
    await bot.change_presence(activity=discord.Activity(type=2, name='a BANGER')) #set status
    for file in os.listdir('cogs.'): #iterate through cogs and load them
        if '.py' in file:
            bot.load_extension(f"cogs.{file[:-3]}") #load extension

@bot.command(brief='Reload Muscia commands')
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}") #unload extension
    bot.load_extension(f"cogs.{extension}") #load extension

bot.run(TOKEN) #run bot