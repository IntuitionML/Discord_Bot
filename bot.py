'''
Bot Current:
- View channel for post with instagram.com/p/ or /reel/ and download/post the movie from the link


Bot Goal:
- LLM research assistant, web search to collect data and info on user topic and post findings.
- YT transcriber/ summarizer



Discord Interactions (Slash command suggestions)
https://stackoverflow.com/questions/75551524/how-do-i-create-slash-commands-in-discord-py
'''


import discord
from discord import Interaction
from discord.ext import commands
from discord import app_commands



import os
from dotenv import load_dotenv, find_dotenv

import yaml

# Set credentials
load_dotenv(find_dotenv())
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Configure discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents, heartbeat_timeout=0, description="A silly little bot that can do some silly little things.\n\n Use the prefix '/' with a command below.")



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.hybrid_command(name="ping")
async def ping(ctx):
    """ - Perform a health check"""
    with open('allowed_channels.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    allowed_channels = data['allowed_channels']
    if ctx.channel.id not in allowed_channels:
        return
    await ctx.send(f"Bot online.\nChannel ID: {ctx.channel.id}")


@bot.hybrid_command(name="allow")
@commands.guild_only()
@commands.is_owner()
async def allow(ctx):
    """ - Allow the bot to view messages in this channel"""
    with open('allowed_channels.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    if ctx.channel.id not in data['allowed_channels']:
        data['allowed_channels'].append(ctx.channel.id)
        with open('allowed_channels.yaml', 'w') as file:
            yaml.dump(data, file)
        await ctx.send(f'Channel {ctx.channel.id} allowed.')
    else:
        await ctx.send(f'Channel {ctx.channel.id} already allowed.')

@bot.hybrid_command()
@commands.guild_only()
@commands.is_owner()
async def deny(ctx):
    """ - Remove the bot's ability to view messages in this channel"""
    with open('allowed_channels.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    if ctx.channel.id in data['allowed_channels']:
        data['allowed_channels'].remove(ctx.channel.id)
        with open('allowed_channels.yaml', 'w') as file:
            yaml.dump(data, file)
        await ctx.send(f'Channel {ctx.channel.id} denied.')
    else:
        await ctx.send(f'Channel {ctx.channel.id} not in allowed list.')


# Loop through cogs and load them.
@bot.event
async def setup_hook():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        await bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded Cog: {filename[:-3]}")
    else:
        print("Unable to load pycache folder.")



# Sync Command Tree. Needed for Hybrid commands (Slash Commands)
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx):
    synced = await ctx.bot.tree.sync()
    await ctx.send (f"Synced {len(synced)} commands to current guild")
    print(f"Synced: {synced}")
    return


bot.run(DISCORD_TOKEN)