import discord
from discord.ext import commands

import instaloader
from instaloader import Post
from instaloader.exceptions import QueryReturnedBadRequestException
import os
import re

import logging
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
            
            try:
                await self.download_and_send_video(message, ig_url)
            
            except QueryReturnedBadRequestException as e:
                if e.response.status_code == 401:
                    await message.reply("Error: JSON Query to graphql/query: HTTP error code 401..")
            except Exception as e:
                await message.reply(f"An unexpected error occurred: {e}")


            # put error handling here?
    
    async def download_and_send_video(self, message, ig_url):
        # init reply
        processing_message = await message.channel.send('Processing')
        # await channel.typing()                                    Would really like to get this working in the future
                
        # Get shortcode
        shortcode = self.get_shortcode(ig_url)
        
        # Get Instaloader instance
        L = instaloader.Instaloader()
        # Only download video
        L.download_pictures = True
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
        target_path = 'temp'

        # Download post videos
        file_payload = []       
        for filename in os.listdir(target_path):
            if filename.startswith(f'{shortcode}'):
                file_path = os.path.join(target_path, filename)
                file_payload.append(discord.File(file_path))
        print(file_payload)
        # Verify files in payload
        if file_payload:
            await asyncio.gather(
                processing_message.delete(),
                message.reply(files=file_payload, mention_author=False)
            )
        elif not file_payload:
            logging.error(f"No files in found in .\{file_path}\nResult: {file_payload}")
            await asyncio.gather(
                message.reply(f"Bot encountered an error"),
                processing_message.delete()
            )
        
        # Clean up temp folder Consider a try: except block?
        for file in file_payload:
            os.remove(file.fp.name)

    # Convert ig url to "shortcode"
    def get_shortcode(self, ig_url):
        match = re.search(r'/p/([^/]+)|/reel/([^/?]+)', ig_url)
        if match:
            return match.group(1) or match.group(2)
        
async def setup(bot):
    await bot.add_cog(IGDownloader(bot))
    