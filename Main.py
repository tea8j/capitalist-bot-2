# created by tea8j on github, if this was reposted elsewhere, tell me.
# credits to magic turtle#6942 on discord for help testing and brainstorming
# TODO: add pet functionality, add inventory system
import discord
from discord.ext import commands
import os
from datetime import date
import pickle

# sets command prefix
bot = commands.Bot(command_prefix='>')


# FUNCTIONS
async def getval(id, file, ifno):
    await mkdir(id)
    try:
        bal = open(id + '/' + str(file) + '.txt', 'r')
    except OSError:
        bal = open(id + '/' + str(file) + '.txt', 'a+')
        bal.write(str(ifno))
        bal.close()
        bal = open(id + '/' + str(file) + '.txt', 'r')
    balnum = bal.read()
    return balnum


async def mkdir(dir):
    try:
        os.mkdir(str(dir))
    except OSError:
        print('')


async def addval(id, file, add):
    temp = await getval(str(id), file, '0')
    file2 = open(id + '/' + str(file) + '.txt', 'w')
    file2.write(str(int(temp) + int(add)))


async def buypetfunc(id, pet, cost):
    if int(await getval(id, 'bal', '0')) > int(cost) - 1:
        temp = open(id + '/petlist.txt', 'a+')
        temp.close()
        with open(str(id) + '/petlist.txt', 'rb') as fp:
            try:
                load = pickle.load(fp)
            except EOFError:
                load = ['temp']
            if load == ['temp']:
                load.remove('temp')
                load.append(str(pet))
            else:
                load.append(str(pet))
            with open(str(id) + '/petlist.txt', 'wb') as file:
                pickle.dump(load, file)
            await addval(str(id), bal, '-' + cost)
            return str(pet) + ' bought for ' + str(cost) + '$'
    else:
        return 'I diagnose you with poor'


def converttostr(input_seq, seperator):
    final_str = seperator.join(input_seq)
    return final_str


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
        temp = (int(1000 * float(await getval(str(ctx.author.id), 'dailymultiply', '1'))))
        await addval(str(ctx.author.id), bal, temp)
        await ctx.send('I gotchu fam')
    day = open(str(ctx.author.id) + '/daily.txt', 'w')
    day.write(today2)


@bot.command()
async def grant(ctx, id, amount):  # admin command to grant money
    if ctx.author.id == 295349622765912086:
        await addval(str(id), 'bal', str(amount))
        await ctx.send('granted ' + str(amount) + '$ to id ' + str(id))


@bot.command()
async def buypet(ctx, pet=None):
    if not pet:
        with open('petshop.txt', 'r') as petshop:
            await ctx.send(petshop.read())
    else:
        if pet == 'turtle':
            await ctx.send(await buypetfunc(str(ctx.author.id), 'turtle', '5000'))
            await ctx.send(':turtle:')
        if pet == 'dog':
            await ctx.send(await buypetfunc(str(ctx.author.id), 'dog', '5000'))
            await ctx.send(':dog:')


@bot.command()
async def petlist(ctx):
    with open(str(ctx.author.id) + '/petlist.txt', 'rb') as fp:
        list = pickle.load(fp)
        stringlist = converttostr(list, ', ')
        await ctx.send(stringlist)


# tells you when ready and changes discord activity
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="space movie 1992"))


# is for reading token & starting bot
token = open('token.txt', 'r')
bot.run(token.read())
