import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Connected to Discord')

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")     # ctx.author.send = returns the message to their DMs

client.run(os.getenv('DISCORD_TOKEN'))