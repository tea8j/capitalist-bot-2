import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')





@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=">helpme for help"))

token = open('token.txt', 'r')
bot.run(token.read())