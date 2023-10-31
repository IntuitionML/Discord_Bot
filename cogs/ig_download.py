import discord
from discord.ext import commands

import instaloader
from instaloader import Post
import os
import re

import asyncio
import yaml
    
class IGDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Check message has IG URL
    @commands.Cog.listener()
    async def on_message(self, message):
        with open('allowed_channels.yaml', 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        allowed_channels = data['allowed_channels']
        if message.channel.id not in allowed_channels:
            return
        ig_url_match = re.search(r'((http://|https://)?(www\.)?instagram\.com(/reel/|/p/)[^\s]+)', message.content)
        print("Checking URL")
        if ig_url_match:
            ig_url = ig_url_match.group(1)
            await self.download_and_send_video(message, ig_url)
    
    async def download_and_send_video(self, message, ig_url):
        # init reply
        processing_message = await message.channel.send('Processing')
        # await channel.typing()                                    Would really like to get this working in the future
                
        # Get shortcode
        shortcode = self.get_shortcode(ig_url)
        print(f"Downloading shortcode: {shortcode}")
        # Get Instaloader instance
        L = instaloader.Instaloader()
        # Only download video
        L.download_pictures = False
        L.download_videos = True
        L.download_video_thumbnails = False
        L.download_geotags = False
        L.download_comments = False
        L.save_metadata = False
        # Special requierment to avoid downloading caption as .txt
        L.post_metadata_txt_pattern = ""
        # Specify filename pattern
        L.filename_pattern = "{shortcode}"

        # Get Post object from URL shortcode
        post = Post.from_shortcode(L.context, shortcode)

        # Download content of Post object to temp folder
        L.download_post(post, target="temp")
        video_path = f'temp/{shortcode}.mp4'
        with open(video_path, 'rb') as video_file:
            await asyncio.gather(
                processing_message.delete(), 
                message.reply(file=discord.File(video_file))
            )
        os.remove(video_path)                                 # delete IG video after poasted,

        
    # Convert all ig url to "shortcode"
    def get_shortcode(self, ig_url):
        match = re.search(r'/p/([^/]+)|/reel/([^/?]+)', ig_url)
        if match:
            return match.group(1) or match.group(2)
        
async def setup(bot):
    await bot.add_cog(IGDownloader(bot))
    