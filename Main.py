# created by tea8j on github, if this was reposted elsewhere, tell me.
# credits to magic turtle#6942 on discord for help testing and brainstorming
import discord
from discord import Embed, Color
from discord.ext import commands
import os
from datetime import date
import pickle
import random

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


async def converttostr(input_seq, seperator):
    try:
        final_str = seperator.join(input_seq)
    except TypeError:
        final_str = 'Nothing'
    return final_str


async def giveitem(id, item):
    await mkdir(str(id))
    temp = open(id + '/inventory.txt', 'a+')
    temp.close()
    with open(str(id) + '/inventory.txt', 'rb') as fp:
        try:
            load = pickle.load(fp)
        except EOFError:
            load = ['temp']
        if load == ['temp']:
            load.remove('temp')
            load.append(str(item))
        else:
            load.append(str(item))
        with open(str(id) + '/inventory.txt', 'wb') as file:
            pickle.dump(load, file)


async def buyitem(id, item, cost):
    if int(await getval(id, 'bal', '0')) > int(cost) - 1:
        temp = open(id + '/inventory.txt', 'a+')
        temp.close()
        with open(str(id) + '/inventory.txt', 'rb') as fp:
            try:
                load = pickle.load(fp)
            except EOFError:
                load = ['temp']
            if not load:
                load = ['temp']
            length = float(len(load))
            maxinv = float(await getval(str(id), 'maxinv', 50))
            if round(maxinv) <= length:
                return 'inventory full (' + str(int(length)) + '/' + str(round(maxinv)) + ')'
            else:
                if load == ['temp']:
                    load.remove('temp')
                    load.append(str(item))
                else:
                    load.append(str(item))
                with open(str(id) + '/inventory.txt', 'wb') as file:
                    pickle.dump(load, file)
                await addval(str(id), bal, '-' + cost)
                return str(item) + ' bought for ' + str(cost) + '$'
    else:
        return 'I diagnose you with poor'


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
async def pets(ctx):
    temp = open(str(ctx.author.id) + '/petlist.txt', 'a+')
    temp.close()
    temp = open(str(ctx.author.id) + '/activepets.txt', 'a+')
    temp.close()
    with open(str(ctx.author.id) + '/petlist.txt', 'rb') as fp:
        list = pickle.load(fp)
        stringlist = await converttostr(list, ', ')
        await ctx.send('archived pets: ' + stringlist)
    with open(str(ctx.author.id) + '/activepets.txt', 'rb') as fp:
        list = pickle.load(fp)
        stringlist = await converttostr(list, ', ')
        await ctx.send('active pets: ' + stringlist)


@bot.command()
async def shop(ctx):
    with open('shop.txt', 'r') as shop:
        await ctx.send(shop.read())


@bot.command()
async def buy(ctx, item=None):
    if not item:
        with open('shop.txt', 'r') as shop:
            await ctx.send(shop.read())
    else:
        if item == 'donald_trump_plushie':
            await ctx.send(await buyitem(str(ctx.author.id), 'donald_trump_plushie', '1000'))
            await ctx.send(':flag_us:')
        if item == 'bronze_donald_trump_plushie':
            await ctx.send(await buyitem(str(ctx.author.id), 'bronze_donald_trump_plushie', '10000'))
            await ctx.send(':flag_us:')
        if item == 'silver_donald_trump_plushie':
            await ctx.send(await buyitem(str(ctx.author.id), 'silver_donald_trump_plushie', '100000'))
            await ctx.send(':flag_us:')
        if item == 'gold_donald_trump_plushie':
            await ctx.send(await buyitem(str(ctx.author.id), 'gold_donald_trump_plushie', '1000000'))
            await ctx.send(':flag_us:')


@bot.command()
async def inv(ctx):
    with open(str(ctx.author.id) + '/inventory.txt', 'rb') as fp:
        list = pickle.load(fp)
        stringlist = await converttostr(list, ', ')
        await ctx.send(stringlist)


@bot.command()
async def activepets(ctx, addremovelist=None, pet=None):
    if not addremovelist:
        await ctx.send('USAGE:\n>activepets [add/remove/list] [petname]')
    if addremovelist == 'add':
        temp = open(str(ctx.author.id) + '/petlist.txt', 'a+')
        temp.close()
        with open(str(ctx.author.id) + '/petlist.txt', 'rb') as fp:
            try:
                list = pickle.load(fp)
            except EOFError:
                list = ['if u see this, hello']
        if str(pet) in list:
            await mkdir(str(ctx.author.id))
            maxpets = await getval(str(ctx.author.id), 'maxpets', 3)
            temp = open(str(ctx.author.id) + '/activepets.txt', 'a+')
            temp.close()
            with open(str(ctx.author.id) + '/activepets.txt', 'rb') as fb:
                try:
                    load = pickle.load(fb)
                except EOFError:
                    load = ['temp']
                activepetnum = str(len(load))
            if str(activepetnum) == str(maxpets):
                await ctx.send(
                    'pet inventory full. (' + activepetnum + '/' + maxpets + ') use >activepets remove [pet] to remove a pet from your active pets')
            elif str(pet) in list:
                if load == ['temp']:
                    load.remove('temp')
                with open(str(ctx.author.id) + '/activepets.txt', 'wb') as fb:
                    load.append(str(pet))
                    pickle.dump(load, fb)
                fp.close()
                with open(str(ctx.author.id) + '/petlist.txt', 'wb') as fp:
                    list.remove(str(pet))
                    pickle.dump(list, fp)
                await ctx.send('look at you with your fancy ass ' + str(pet))
        else:
            await ctx.send('you don\'t have that pet :rofl:')
    if addremovelist == 'remove':
        temp = open(str(ctx.author.id) + '/activepets.txt', 'a+')
        temp.close()
        with open(str(ctx.author.id) + '/activepets.txt', 'rb') as fp:
            try:
                list = pickle.load(fp)
            except EOFError:
                list = ['if u see this, hello']
        if str(pet) in list:
            temp = open(str(ctx.author.id) + '/petlist.txt', 'a+')
            temp.close()
            with open(str(ctx.author.id) + '/petlist.txt', 'rb')as fb:
                load = pickle.load(fb)
            with open(str(ctx.author.id) + '/petlist.txt', 'wb') as fb:
                load.append(str(pet))
                pickle.dump(load, fb)
                fp.close()
            with open(str(ctx.author.id) + '/activepets.txt', 'wb') as fp:
                list.remove(str(pet))
                pickle.dump(list, fp)
            await ctx.send('you\'re off to the shadow realm, ' + str(pet))
        else:
            await ctx.send('you don\'t have that pet :rofl:')


@bot.command()
async def reloadpets(ctx):
    await mkdir(ctx.author.id)
    temp = open(str(ctx.author.id) + '/tempreloadpet.txt', 'a+')
    temp.close()
    temp = open(str(ctx.author.id) + '/activepets.txt', 'a+')
    temp.close()
    with open(str(ctx.author.id) + '/activepets.txt', 'rb') as fp:
        temp2 = pickle.load(fp)
        with open(str(ctx.author.id) + '/tempreloadpet.txt', 'rb') as tempreload:
            try:
                tempr = pickle.load(tempreload)
            except EOFError:
                tempr = temp2
        if tempr == temp2:
            with open(str(ctx.author.id) + '/maxinv.txt', 'w') as maxinv:
                maxinv.write('50')
            with open(str(ctx.author.id) + '/dailymultiply.txt', 'w') as daymulti:
                daymulti.write('1')
        if 'turtle' in tempr:
            temp = open(str(ctx.author.id) + '/maxinv.txt', 'a+')
            temp.close()
            with open(str(ctx.author.id) + '/maxinv.txt', 'r') as maxinv:
                maxinvread = maxinv.read()
            with open(str(ctx.author.id) + '/maxinv.txt', 'w') as maxinv:
                maxinv.write(str(float(maxinvread)*1.1))
            tempr.remove('turtle')
            with open(str(ctx.author.id) + '/tempreloadpet.txt', 'wb') as tempreload:
                pickle.dump(tempr, tempreload)
            await reloadpets(ctx)
        elif 'dog' in tempr:
            temp = open(str(ctx.author.id) + '/dailymultiply.txt', 'a+')
            temp.close()
            with open(str(ctx.author.id) + '/dailymultiply.txt', 'r') as daymulti:
                maxinvread = daymulti.read()
            with open(str(ctx.author.id) + '/dailymultiply.txt', 'w') as daymulti:
                daymulti.write(str(float(maxinvread)*1.1))
            tempr.remove('dog')
            with open(str(ctx.author.id) + '/tempreloadpet.txt', 'wb') as tempreload:
                pickle.dump(tempr, tempreload)
            await reloadpets(ctx)
        else:
            await ctx.send('it is done')
            os.remove(str(ctx.author.id) + '/tempreloadpet.txt')

@bot.command()
async def profile(ctx):
    try:
        mentioned = ctx.message.mentions[0]
    except IndexError:
        mentioned = ctx.author
    bal = await(getval(str(mentioned.id), 'bal', '0'))
    temp = open(str(mentioned.id) + '/petlist.txt', 'a+')
    temp.close()
    temp = open(str(mentioned.id) + '/activepets.txt', 'a+')
    temp.close()
    with open(str(mentioned.id) + '/petlist.txt', 'rb') as fp:
        try:
            list = pickle.load(fp)
        except EOFError:
            list = ['Nothing']
        acpetlist = await converttostr(list, ', ')
    with open(str(mentioned.id) + '/activepets.txt', 'rb') as fp:
        try:
            list = pickle.load(fp)
        except EOFError:
            list = ['Nothing']
        arpetlist = await converttostr(list, ', ')

    temp = open(str(mentioned.id) + '/inventory.txt', 'a+')
    temp.close()
    with open(str(mentioned.id) + '/inventory.txt', 'rb') as fp:
        try:
            list = pickle.load(fp)
        except EOFError:
            list = ['Nothing']
        inventory = await converttostr(list, ', ')

    tags=[]
    with open('developers.txt', 'rb') as fp:
        devs = pickle.load(fp)
    with open('supporters.txt', 'rb') as fp:
        sups = pickle.load(fp)
    with open('brain.txt', 'rb') as fp:
        brain = pickle.load(fp)
    with open('turtle.txt', 'rb') as fp:
        turtle = pickle.load(fp)
    if str(mentioned.id) in devs:
        tags.append('💻')
    if str(mentioned.id) in sups:
        tags.append('💸')
    if str(mentioned.id) in brain:
        tags.append('🧠')
    if str(mentioned.id) in turtle:
        tags.append('🐢')
    tags2 = await converttostr(tags, '')


    embed = Embed(
        title=str(mentioned) + "'s profile",
        colour=Color(0x00FF00),
        description='Balance: ' + bal + '\nActive pets: ' + acpetlist + '\n Archived pets: ' + arpetlist + '\n Inventory: ' + inventory
    )

    embed.set_image(url=mentioned.avatar_url)
    embed.set_footer(text=tags2)
    return await ctx.send(embed=embed)

@bot.command()
async def use(ctx, item):
    temp = open(str(ctx.author.id) + '/inventory.txt', 'a+')
    temp.close()
    with open(str(ctx.author.id) + '/inventory.txt', 'rb') as fp:
        try:
            load = pickle.load(fp)
        except EOFError:
            load = ['temp']
    if str(item) in load:
        if str(item) == 'donald_trump_plushie':
            amount = random.randint(0, 2000)
            await addval(str(ctx.author.id), 'bal', str(amount))
            await ctx.send('you were given ' + str(amount) + '$')
            with open(str(ctx.author.id) + '/inventory.txt', 'wb') as fp:
                pickle.dump(load.remove('donald_trump_plushie'), fp)
    if str(item) in load:
        if str(item) == 'bronze_trump_plushie':
            amount = random.randint(0, 20000)
            await addval(str(ctx.author.id), 'bal', str(amount))
            await ctx.send('you were given ' + str(amount) + '$')
            with open(str(ctx.author.id) + '/inventory.txt', 'wb') as fp:
                pickle.dump(load.remove('bronze_donald_trump_plushie'), fp)
    if str(item) in load:
        if str(item) == 'silver_donald_trump_plushie':
            amount = random.randint(0, 200000)
            await addval(str(ctx.author.id), 'bal', str(amount))
            await ctx.send('you were given ' + str(amount) + '$')
            with open(str(ctx.author.id) + '/inventory.txt', 'wb') as fp:
                pickle.dump(load.remove('silver_donald_trump_plushie'), fp)
    if str(item) in load:
        if str(item) == 'gold_donald_trump_plushie':
            amount = random.randint(0, 2000000)
            await addval(str(ctx.author.id), 'bal', str(amount))
            await ctx.send('you were given ' + str(amount) + '$')
            with open(str(ctx.author.id) + '/inventory.txt', 'wb') as fp:
                pickle.dump(load.remove('gold_donald_trump_plushie'), fp)



# tells you when ready and changes discord activity
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over my slaves"))


# is for reading token & starting bot
token = open('token.txt', 'r')
bot.run(token.read())
