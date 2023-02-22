import os
import discord
import requests
import json
import random
# import asyncio
import humanfriendly
from datetime import datetime, timedelta, timezone
from discord.ext import commands
from googleapiclient.discovery import build

client = commands.Bot(command_prefix="=", intents=discord.Intents.all(), help_command=None)    # set prefix, and allow bot to accept all events
start_time = datetime.utcnow()  # Record the time the bot was started

# Functions begin from here
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reference: https://www.youtube.com/watch?v=ovT9GQ-0mlU
# async def schedule_daily_message():
#     now = datetime.now()
#     then = now.replace(hour=23, minute=0)
#     wait_time = (then-now).total_seconds()
#     await asyncio.sleep(wait_time)
#     channel = client.get_channel(int(os.getenv('CHANNEL_ID')))
#     await channel.send("Hey summoners, LoLdle has refreshed!\nhttps://loldle.net/")

@client.event   # discord.py wrapper function
async def on_ready():
    await client.tree.sync()
    print('Connected to bot: {}'.format(client.user.name))
    await client.change_presence(activity=discord.Streaming(name='Variety', url='https://www.twitch.tv/'))
    # await schedule_daily_message()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# =calc command
@client.command(name='calc')
async def calc(ctx, expression=''):   # calc read as a string
    try:
        result = eval(expression)
        embed = discord.Embed(title=expression, color=0xFF9900)
        embed.add_field(name=result, value='', inline=False)
        await ctx.send(embed=embed)
    except (SyntaxError, NameError) as error:
        embed = discord.Embed(title="Usage: `=calc`", color=0xFF9900)
        embed.add_field(name="", value="Syntax: `=calc <expression>`\nExample: `=calc 2*2/10-(10-4)` --> `(-5.6)`\nDon't forget, no spaces!", inline=False)
        await ctx.send(embed=embed)

# =coinflip command 
@client.command(name='coinflip')
async def coinflip(ctx):
    coin = random.randint(0, 1)
    
    if coin == 0:
        embed = discord.Embed(
            description="Heads!",
            color=0xFF9900
        )
    else:
        embed = discord.Embed(
        description="Tails!",
        color=0xFF9900
    )
    await ctx.message.reply(embed=embed)

# =dice command
@client.command(name='dice')
async def dice(ctx, amount=None, sides=None):
    try:
        amount = int(amount)
        sides = int(sides)
        total = 0
        embed = discord.Embed(title=f"Roll (x{amount}) D{sides} Dice", color=0xFF9900)
        for i in range(amount):
            total += random.randint(0, sides)
        embed.add_field(name="", value=f'Total:\t**{total}**', inline=False)
    except:
        embed = discord.Embed(title=f"Usage: `=dice`", color=0xFF9900)
        embed.add_field(name=f"", value='Syntax: `=dice <# of dices> <# of sides>`\nExample: `=dice 2 8`', inline=False)
        
    await ctx.send(embed=embed)

# =dog command
@commands.command(name='dog')
async def dog(ctx, breed=""):
    if len(breed) <= 0:
        endpoint = "https://dog.ceo/api/breeds/image/random/"
        embed = discord.Embed(title='Random Dog', color=0xFF9900)
    else:
        endpoint = f"https://dog.ceo/api/breed/{breed}/images/random/"
        embed = discord.Embed(title=f"A {breed}!", color=0xFF9900)
    
    response = requests.get(endpoint)
    data = json.loads(response.content)
    image_url = data["message"]

    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

# =github command
@client.command(name='github')
async def github(ctx):
    await ctx.send("`For source code, commands, and releases:` \nhttps://github.com/Julellisg/Gamious-Bot")

# =help command
@client.command(name='help')
async def help(ctx):
    rules = """
    `=calc <expression>`: calculates any math expression using `eval()`
    `=coinflip`: sends \"Heads!\" or \"Tails!\".
    `=dice <# dices> <# sides>`: returns total of dice roll.
    `=dog` or `=dog <breed>`: sends a picture of a random/chosen breed of dog.
    `=github`: links to the github origin page
    `=help`: basically gives list of commands.
    `/loldle`: sends the LoLdle link.
    `=ping` or `/ping`: returns \"pong!\" with latency.
    `=poll -question -option 1 -option2`: spaced apart using `-` with 2-10 option limit.
    `=profile @mention`: returns the discord avatar of the @mention'd user.
    `=sort`: sorts a set of numbers/words in order.
    `=sortr`: sorts a set of numbers/words in reverse-order.
    `=uptime`: send current uptime of the bot since it has gone online.
    `=yt <search query>`: returns 5 results of a given search query, otherwise an empty search returns 5 random videos.
    """
    embed = discord.Embed(title="Help / Commands", color=0xFF9900)
    embed.add_field(name='', value=rules, inline=False)

    await ctx.send(embed=embed, allowed_mentions=None)

# /loldle command
@client.tree.command(name="loldle", description="Sends the link to LoLdle.")
async def loldle(interaction: discord.Interaction):
    await interaction.response.send_message("https://loldle.net/")

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
            title="Usage: `=poll`", 
            description="Syntax: `=poll -question -option1 -option2` ... (2-10 options)\nExample: `=poll -Is a hotdog a sandwhich? -Yes -No`",
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
        embed.add_field(name="", value=f'{emoji}\t{option}', inline=False)

    # print the embedded message and react onto the message using emojis
    message = await ctx.send(embed=embed)
    for i, option in enumerate(substring[1:]):
        emoji = emojis[i]
        await message.add_reaction(emoji)

# =profile command
@client.command(name='profile')
async def profile(ctx, member: discord.Member):
    member_name = member.name +"#"+ member.discriminator
    pfp_url = member.avatar.url # retrieves avatar url of @mention user
    embed = discord.Embed(
        title="Avatar",
        description=member_name,
        color=0xFF9900
    )
    embed.set_image(url=pfp_url)
    await ctx.message.reply(embed=embed)

# =sort command
@client.command(name='sort')
async def sort(ctx, *unsorted):
    sorted_list = list(unsorted)    # converts a tuple to a list
    sorted_list.sort()              # sort the list
    embed = discord.Embed(color=0xFF9900)
    result = ""
    for i in sorted_list:
        result += i+" "
    embed.add_field(name='', value=result, inline=False)
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
    embed.add_field(name='', value=result, inline=False)
    await ctx.send(embed=embed)

# =uptime command
@client.command(name='uptime')
async def uptime(ctx):
    total_time = datetime.utcnow() - start_time
    hours, remainder = divmod(int(total_time.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(
        title=f"Uptime: {days}d, {hours}h, {minutes}m, {seconds}s",
        color=0xFF9900
    )
    await ctx.send(embed=embed)

# =yt command
@client.command(name="yt")
async def yt(ctx, *query):
    query = ' '.join(query)
    youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API'))

    # creates search request to YT Data API using the given info
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=5
    ).execute()

    video_ids = []
    video_titles = []
    video_authors = []
    video_viewcount = []
    video_thumbnail = []

    # processes the results of the YouTube search query (the amount of them are predetermined)
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':                  # just to find only youtube videos
            video_ids.append(search_result['id']['videoId'])                # video ID
            video_titles.append(search_result['snippet']['title'])          # video title
            video_authors.append(search_result['snippet']['channelTitle'])  # video channel title/author
            video_thumbnail.append(search_result['snippet']['thumbnails']['medium']['url']) # thumbnail url, medium size
            video_statistics = youtube.videos().list(
                part='statistics',
                id=search_result['id']['videoId']
            ).execute()['items'][0]['statistics']
            video_viewcount.append(video_statistics['viewCount'])           # video view count

    video_links = [f'https://www.youtube.com/watch?v={video_id}' for video_id in video_ids] # appends all the video links

    # Starts appending them to an embed message then resets per video/per loop
    for i in range(len(video_links)):
        embed = discord.Embed(title=f'YouTube Search', color=0xFF0000)

        long_title=f"{i+1}. {video_titles[i]}"
        short_title=long_title[:256]
        embed.add_field(name='', value=short_title, inline='False')
        if len(short_title) == 0:
            embed.add_field(name='', value=long_title, inline='False')

        long_title=f"By: {video_authors[i]}\t|\tViews: {humanfriendly.format_number(video_viewcount[i])}"
        short_title=long_title[:256]
        embed.add_field(name='', value=short_title, inline='False')
        if len(short_title) == 0:
            embed.add_field(name='', value=long_title, inline='False')

        long_title=f"{video_links[i]}"
        tb_url = ""
        short_title=long_title[:256]
        embed.add_field(name='', value=short_title, inline='False')
        if len(short_title) == 0:
            embed.add_field(name='', value=long_title, inline='False')

        long_title=f"{video_thumbnail[i]}"
        short_title=long_title[:256]
        embed.set_thumbnail(url=short_title)

        await ctx.send(embed=embed)

client.add_command(dog)
client.run(os.getenv('DISCORD_TOKEN'))