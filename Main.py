import discord
from discord.ext import commands
import os
from datetime import date

# sets command prefix
bot = commands.Bot(command_prefix='>')


# FUNCTIONS
async def getval(id, file, ifno):
    try:
        os.mkdir(id)
    except OSError:
        print('')
    try:
        bal = open(id + '/' + str(file) + '.txt', 'r')
    except OSError:
        bal = open(id + '/' + str(file) + '.txt', 'a+')
        bal.write(ifno)
        bal.close()
        bal = open(id + '/' + str(file) + '.txt', 'r')
    balnum = bal.read()
    return balnum


async def addval(id, file, add):
    temp = await getval(str(id), file, '0')
    file2 = open(id + '/' + str(file) + '.txt', 'w')
    file2.write(str(int(temp) + int(add)))


# COMMANDS
@bot.command()
async def bal(ctx):  # command to check balance
    balnum = await getval(str(ctx.author.id), 'bal', '0')
    if balnum == '0':
        await ctx.send('yikes he\'s poor')
    await ctx.send('you have ' + balnum + '$')


@bot.command()
async def daily(ctx):  # command to get a daily allowance
    today = date.today()
    today2 = str(today.strftime("%Y%m%d"))
    maybetoday = await getval(str(ctx.author.id), 'daily', '0')
    if maybetoday == today2:
        await ctx.send('it hasn\'t been a day dumbass')
    else:
        await addval(str(ctx.author.id), bal, '2500')
        await ctx.send('I gotchu fam')
    day = open(str(ctx.author.id) + '/daily.txt', 'w')
    day.write(today2)


@bot.command()
async def grant(ctx, id, amount):  # admin command to grant money
    if ctx.author.id == 295349622765912086:
        await addval(str(id), 'bal', str(amount))
        await ctx.send('granted ' + str(amount) + '$ to id ' + str(id))


# tells you when ready and changes discord activity
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="space movie 1992"))


# is for reading token & starting bot
token = open('token.txt', 'r')
bot.run(token.read())
