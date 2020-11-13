import discord
from discord.ext import commands
import os
from datetime import date

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
@bot.command()
async def bal(ctx):  # command to check balance
    balnum = await bald(str(ctx.author.id))
    if balnum == '0':
        await ctx.send('yikes he\'s poor')
    await ctx.send('you have ' + balnum + '$')


@bot.command()
async def daily(ctx):  # command to get a daily allowance
    today = date.today()
    today2 = str(today.strftime("%Y%m%d"))
    try:
        os.mkdir(str(ctx.author.id))
    except OSError:
        print('')
    day = open(str(ctx.author.id) + '/daily.txt', 'a+')
    day.close()
    day = open(str(ctx.author.id) + '/daily.txt', 'r')
    maybetoday = day.read()
    if maybetoday == today2:
        await ctx.send('it hasn\'t been a day dumbass')
    else:
        await add_bal('2500', str(ctx.author.id))
        await ctx.send('I gotchu fam')
    day.close()
    day = open(str(ctx.author.id) + '/daily.txt', 'w')
    day.write(today2)


@bot.command()
async def grant(ctx, id, amount):  # admin command to grant money
    if ctx.author.id == 295349622765912086:
        await add_bal(str(amount), str(id))
        await ctx.send('granted ' + str(amount) + '$ to id ' + str(id))


# tells you when ready and changes discord activity
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="space movie 1992"))


# is for reading token & starting bot
token = open('token.txt', 'r')
bot.run(token.read())
