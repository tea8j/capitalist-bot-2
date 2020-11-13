import discord
from discord.ext import commands
import os

# sets command prefix
bot = commands.Bot(command_prefix='>')


# FUNCTIONS
async def add_bal(amount, id):
    try:
        os.mkdir(id)
    except OSError:
        print('')
    try:
        bal = open(id + '/bal.txt', 'r')
    except OSError:
        bal = open(id + '/bal.txt', 'a+')
        bal.write('0')
        bal.close()
        bal = open(id + '/bal.txt', 'r')
    tempbal = bal.read()
    bal.close()
    bal = open(id + '/bal.txt', 'w')
    bal.write(str(int(tempbal) + int(amount)))


async def bald(id):
    try:
        os.mkdir(id)
    except OSError:
        print('')
    try:
        bal = open(id + '/bal.txt', 'r')
    except OSError:
        bal = open(id + '/bal.txt', 'a+')
        bal.write('0')
        bal.close()
        bal = open(id + '/bal.txt', 'r')
    balnum = bal.read()
    print(bal.read())
    return balnum


# COMMANDS
@bot.command()  # command to check balance
async def bal(ctx):
    balnum = await bald(str(ctx.author.id))
    if balnum == '0':
        await ctx.send('yikes he\'s poor')
    await ctx.send('you have ' + balnum + '$')


# tells you when ready and changes discord activity
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="space movie 1992"))


# is for reading token & starting bot
token = open('token.txt', 'r')
bot.run(token.read())
