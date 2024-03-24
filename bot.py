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

import asyncio
from datetime import datetime, timedelta, time
import random
import csv

import logging

import os
from dotenv import load_dotenv, find_dotenv

import yaml

# Set credentials
load_dotenv(find_dotenv())
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")



# Configure discord
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents, heartbeat_timeout=60, description="A silly little bot that can do some silly little things.\n\n Use the prefix '/' with a command below.")

# Setup logging
logging_handler = logging.FileHandler(filename='events.log', encoding='utf-8', mode='w')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    logging.info(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='🌽Online🌽'))
    #await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='🥳Online🥳'))
    

@bot.hybrid_command(name="ping")
async def ping(ctx):
    """ - Perform a health check"""
    if bot_can_see(ctx):
        await ctx.send(f"Bot online.\nLatency: {bot.latency * 1000:.2f} ms")

## What's that around the corner?
        
def get_random_game_url():
    url_file = "cleaned_urls.csv"
    urls = []
    with open(url_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if the row is not empty
                urls.append(row[0])  # Assume URL is in the first column
    if urls:
        return random.choice(urls)  # Return a random URL from the list
    else:
        return "https://www.xgames.com/events/x-games-ventura-2024"  # Return default xgames site if the list is empty
@bot.hybrid_command(name="corner")        
@commands.guild_only()
#@commands.is_owner()
async def corner(ctx):
    """ - What's that coming around the corner?"""
    # channels:
    # my general: 1153527336927498302
    # my bot testing: 1153527406888484935
    # final channel: 1214734255880413215
    corner_channels = [1153527336927498302, 1153527406888484935, 1214734255880413215, 1150889688538808394]   
    if ctx.channel.id not in corner_channels:
        return

    target_date = datetime.combine(datetime(2024, 6, 27), time(10, 0))
    time_now = datetime.now()
    time_left = target_date - time_now
    days, total_seconds = time_left.days, time_left.seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    # get very important url
    #url_the_game = get_random_game_url()
    #print(f"-----CHECK-----------{url_the_game}") # check

    # make x games man
    author = ctx.guild.get_member(160112526745403392)
    if author:
        embed_author_name = author.display_name
        print(f"-------------------------------Using Display Name: {embed_author_name}")
        embed_author_icon_url = author.guild_avatar.url if author.avatar else "https://pbs.twimg.com/profile_images/1283874111081664515/hxnHB9Gu_400x400.jpg" # xgame man default avatar
    else: # fallback in case issue
        author = await bot.fetch_user(160112526745403392)
        embed_author_name = author.name
        print(f"-------------------------------Using account Name: {embed_author_name}")
        embed_author_icon_url = author.avatar.url if author.avatar else "https://pbs.twimg.com/profile_images/1283874111081664515/hxnHB9Gu_400x400.jpg" # xgame man default avatar
    
    # Create embed message ref: https://plainenglish.io/blog/send-an-embed-with-a-discord-bot-in-python
    embed = discord.Embed(
        title=f"Something is around the corner!", url=get_random_game_url(),
        description=f"Only **{days} days, {hours} hours, {minutes} minutes, and {seconds:.0f} seconds** until we find out what it is!!!",
        color = 15014199 # int value for "X games logo red" Hex:E51937
    )
    embed.set_author(name=embed_author_name, url=get_random_game_url(), icon_url=embed_author_icon_url)
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_banners/18954398/1707222290/1500x500")

    await ctx.send(embed=embed)



@bot.hybrid_command(name="add")
@commands.guild_only()
# @commands.is_owner()
# @commands.has_permissions(administrator=True)
async def add(ctx):
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

@bot.hybrid_command(name="remove")
@commands.guild_only()
# @commands.is_owner()
# @commands.has_permissions(administrator=True)
async def remove(ctx):
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
    print("====================== Sync attempt ======================")
    synced = await ctx.bot.tree.sync()
    await ctx.send (f"Synced {len(synced)} commands to current guild")
    print(f"Synced: {synced}")
    logging.info(f"Synced: {synced}")
    return

bot.run(DISCORD_TOKEN, log_handler=logging_handler, log_level=logging.DEBUG)