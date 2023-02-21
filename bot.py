import os
import datetime
import discord
import requests
import json
import random
from discord.ext import commands

client = commands.Bot(command_prefix="=", intents=discord.Intents.all(), help_command=None)    # set prefix, and allow bot to accept all events
start_time = datetime.datetime.utcnow()  # Record the time the bot was started

@client.event   # discord.py wrapper function
async def on_ready():
    await client.tree.sync()
    print('Connected to bot: {}'.format(client.user.name))
    await client.change_presence(activity=discord.Streaming(name='Variety', url='https://www.twitch.tv/'))

# /ping command
@client.tree.command(name="ping", description="Sends the bot's latency in milliseconds (ms).")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"ping! *{round(client.latency*1000)}ms*")

# =ping command 
@client.command(name='ping')
async def ping(ctx):                    # when someone says "ping"
    latency = round(client.latency * 1000)
    await ctx.message.reply(f'pong! *{latency}ms*')

# =poll command
@client.command(name='poll')
async def poll(ctx, *message):
    # check if empty first
    if len(message) <= 2:
        embed = discord.Embed(
            title="Usage: ``=poll``", 
            description="Syntax: ``=poll -question -option1 -option2`` ... (2-10 options)\nExample: ``=poll -Is a hotdog a sandwhich? -Yes -No``",
            color=0xFF9900
        )
        await ctx.message.reply(embed=embed)
        return
    
    emojis = ['\u0031\u20E3', '\u0032\u20E3', '\u0033\u20E3', '\u0034\u20E3', '\u0035\u20E3', '\u0036\u20E3', '\u0037\u20E3', '\u0038\u20E3', '\u0039\u20E3', '\U0001F51F']
    
    # process of simplifying the format 
    message = ' '.join(message)
    substring = message.split('-')
    substring = substring[1:]

    # set up the question
    question = substring[0]
    embed = discord.Embed(
        title=question,
        color=0xFF9900
    )

    # add each of the options into embedded message
    for i, option in enumerate(substring[1:]):
        emoji = emojis[i]
        embed.add_field(name=f"{emoji}\t{option}", value='', inline=False)

    # print the embedded message and react onto the message using emojis
    message = await ctx.send(embed=embed)
    for i, option in enumerate(substring[1:]):
        emoji = emojis[i]
        await message.add_reaction(emoji)

# =profile command
@client.command(name='profile')
async def profile(ctx, member: discord.Member):
    member_name = member.name + member.discriminator
    pfp_url = member.avatar.url # retrieves avatar url of @mention user
    embed = discord.Embed(
        title="Avatar",
        description=member_name,
        color=0xFF9900
    )
    embed.set_image(url=pfp_url)
    await ctx.message.reply(embed=embed)

# =flip command 
@client.command(name='flip')
async def flip(ctx):
    coin = random.randint(0, 1)
    
    if coin == 0:
        embed = discord.Embed(
            title="Heads!",
            color=0xFF9900
        )
    else:
        embed = discord.Embed(
        title="Tails!",
        color=0xFF9900
    )
    await ctx.message.reply(embed=embed)

# =uptime command
@client.command(name='uptime')
async def uptime(ctx):
    total_time = datetime.datetime.utcnow() - start_time
    hours, remainder = divmod(int(total_time.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(
        title=f"Uptime: {days}d, {hours}h, {minutes}m, {seconds}s",
        color=0xFF9900
    )
    await ctx.send(embed=embed)

# =calc command
@client.command(name='calc')
async def calc(ctx, expression):   # calc read as a string
    try:
        result = eval(expression)
        embed = discord.Embed(title=expression, color=0xFF9900)
        embed.add_field(name=result, value='', inline=False)
        await ctx.send(embed=embed)
    except (SyntaxError, NameError) as error:
        embed = discord.Embed(title="Usage: ``=calc``", color=0xFF9900)
        embed.add_field(name="Syntax: ``=calc <expression>``\nExample: ``=calc 2*2/10-(10-4)`` --> ``(-5.6)``\nDon't forget, no spaces!", value='', inline=False)
        await ctx.send(embed=embed)

# =github command
@client.command(name='github')
async def github(ctx):
    await ctx.send("`For source code, commands, and releases:` \nhttps://github.com/Julellisg/Gamious-Bot")

# =help command
@client.command(name='help')
async def help(ctx):
    embed = discord.Embed(title="Help / Commands", color=0xFF9900)
    embed.add_field(name="`=ping` or `/ping`: returns \"pong!\" with latency.", value='', inline=False)
    embed.add_field(name="`=poll -question -option 1 -option2`: spaced apart using `-` with 2-10 option limit.", value='', inline=False)
    embed.add_field(name="`=profile @mention`: returns the discord avatar of the @mention'd user.", value='', inline=False)
    embed.add_field(name="`=flip`: sends \"Heads!\" or \"Tails!\".", value='', inline=False)
    embed.add_field(name="`=uptime`: send current uptime of the bot since it has gone online.", value='', inline=False)
    embed.add_field(name="`=calc <expression>`: calculates any math expression using `eval()`.", value='', inline=False)
    await ctx.send(embed=embed)

# =sort command
@client.command(name='sort')
async def sort(ctx, *unsorted):
    sorted_list = list(unsorted)    # converts a tuple to a list
    sorted_list.sort()              # sort the list
    embed = discord.Embed(color=0xFF9900)
    result = ""
    for i in sorted_list:
        result += i+" "
    embed.add_field(name=result, value='', inline=False)
    await ctx.send(embed=embed)

# =sortr command
@client.command(name='sortr')
async def sortr(ctx, *unsorted):
    sorted_list = list(unsorted)    # converts a tuple to a list
    sorted_list.sort(reverse=True)              # sort the list
    embed = discord.Embed(color=0xFF9900)
    result = ""
    for i in sorted_list:
        result += i+" "
    embed.add_field(name=result, value='', inline=False)
    await ctx.send(embed=embed)

# =dog command
@commands.command(name='dog')
async def dog(ctx, breed=""):
    if len(breed) <= 0:
        endpoint = "https://dog.ceo/api/breeds/image/random/"
    else:
        endpoint = f"https://dog.ceo/api/breed/{breed}/images/random/"
    
    response = requests.get(endpoint)
    data = json.loads(response.content)
    image_url = data["message"]

    embed = discord.Embed(color=0xFF9900)
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)


client.add_command(dog)
client.run(os.getenv('DISCORD_TOKEN'))