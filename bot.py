import os
import discord
from discord.ext import commands


client = commands.Bot(command_prefix="=", intents=discord.Intents.all())    # set prefix, and allow bot to accept all events

@client.event   # discord.py wrapper function
async def on_ready():
    await client.tree.sync()
    print('Connected to Discord')

# Ping command but using slash
@client.tree.command(name="ping", description="Sends the bot's latency in milliseconds (ms).")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"ping! *{round(client.latency*1000)}ms*")

# Ping command 
@client.command()
async def ping(ctx):                    # when someone says "ping"
    latency = round(client.latency * 1000)
    await ctx.message.reply(f'pong! *{latency}ms*')

# Poll command
@client.command()
async def poll(ctx, *message):
    # check if empty first
    if len(message) <= 2:
        embed = discord.Embed(
            title="Usage:", 
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

# Retrieve user profile picture
@client.command()
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

client.run(os.getenv('DISCORD_TOKEN'))