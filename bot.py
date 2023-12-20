'''
Bot Current:
- View channel for post with instagram.com/p/ or /reel/ and download/post the movie from the link

ToDo:
- Logging via local
- Error Handling 
- In-Discord functionality:
    - Start, Stop, Pause the bot
- Logging
'''


import discord
from discord import Interaction
from discord.ext import commands
from discord import app_commands

import logging

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

# Setup logging
logging_handler = logging.FileHandler(filename='events.log', encoding='utf-8', mode='w')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    logging.info(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='🌽Online🌽'))

@bot.hybrid_command(name="ping")
async def ping(ctx):
    """ - Perform a health check"""
    if bot_can_see(ctx):
        await ctx.send(f"Bot online.\nLatency: {bot.latency * 1000:.2f} ms")


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
        await ctx.send(f'Channel Allowed!')
    else:
        await ctx.send(f'Channel is already allowed.')

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
        await ctx.send(f'Channel denied!')
    else:
        await ctx.send(f'Channel is not in allowed list.')

@bot.hybrid_command()
@commands.guild_only()
@commands.is_owner()
async def test(ctx):
    """ - Test Case"""
    
    if bot_can_see(ctx):
        await ctx.send(f'Test successful')
    else:
        return


def bot_can_see(ctx):
    """
    Determines if the bot has access to the channel that a message or command was posted in.
    
    Parameters:
    - ctx (discord message): The discord message the bot is trying to respond to.
    
    Returns:
    - bool"""
    
    with open('allowed_channels.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    allowed_channels = data['allowed_channels']
    if ctx.channel.id not in allowed_channels:
        return False
    return True


# Load cogs.
@bot.event
async def setup_hook():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        await bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded Cog: {filename[:-3]}")
        logging.info(f"Loaded Cog: {filename[:-3]}")
    else:
        return


# Sync Command Tree. Needed for bot.hybrid_commands (Slash Commands)
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx):
    synced = await ctx.bot.tree.sync()
    await ctx.send (f"Synced {len(synced)} commands to current guild")
    print(f"Synced: {synced}")
    logging.info(f"Synced: {synced}")
    return

bot.run(DISCORD_TOKEN, log_handler=logging_handler, log_level=logging.DEBUG)