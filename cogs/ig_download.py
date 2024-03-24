import discord
from discord.ext import commands

import instaloader
from instaloader import Post
from instaloader.exceptions import QueryReturnedBadRequestException
import os
import re

import difflib

import logging
import asyncio
import yaml
    
class IGDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    # Check message has IG URL
    @commands.Cog.listener()
    async def on_message(self, message):

        # ======================================
        # rewrite to not check on every message!!
        # =======================================
        with open('allowed_channels.yaml', 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        allowed_channels = data['allowed_channels']
        if message.channel.id not in allowed_channels:
            return
        

        # Init ig_url_match
        ig_url_match = re.search(r'((http://|https://)?(www\.)?instagram\.com(/reel/|/p/)[^\s]+)', message.content)
        keyword_user = None
        # check message matches ig url and extract keyword
        message_parts = message.content.split()
        if len(message_parts) >= 2:
            # Update keyword_user if additional parts in message
            keyword_user = ' '.join(message_parts[1:])
            print(f"Checking URL:\n{message.content}")



        # if message is IG url
        if ig_url_match:
            ig_url = ig_url_match.group(1)
            try:
                await self.download_and_send_video(message, ig_url, keyword_user)
            except QueryReturnedBadRequestException as e:
                if e.response.status_code == 401:
                    await message.reply("Error: JSON Query to graphql/query: HTTP error code 401..")
            except Exception as e:
                await message.reply(f"An unexpected error occurred: {e}")



    async def download_and_send_video(self, message, ig_url, user_keyword=None):
        
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

        # load keywords and channels from config
        with open('cs_video_config.yml') as file:
            keywords = yaml.safe_load(file)
        cs_info_channel = 1178165325599096893 # cs_info channel: 1178165325599096893  test channel: 1153527336927498302

        if message.channel.id == cs_info_channel and user_keyword:
                
            # Find closest match to keyword from user provided keyword
            closest_matches = difflib.get_close_matches(user_keyword.lower(), keywords['cs_channels'].keys(), n=1, cutoff=0.6)
            if closest_matches:
                matched_keyword = closest_matches[0]
                channel_id = keywords['cs_channels'][matched_keyword]
                channel = self.bot.get_channel(int(channel_id))
                if channel:
                    await asyncio.gather(
                        processing_message.delete(),
                        channel.send(f"Matched keyword '{matched_keyword}' for video:", files=file_payload, mention_author=False)
                    )
                else: # Fallback if no channel found for keyword
                    fallback_channel = self.bot.get_channel(cs_info_channel)
                    if fallback_channel:
                        await asyncio.gather(
                            processing_message.delete(),
                            fallback_channel.send(f"Post {post.url} but matched keyword '{matched_keyword}' has no associated channel.", files=file_payload, mention_author=False)
                        )
            else: # No close match for keyword
                fallback_channel = self.bot.get_channel(cs_info_channel)
                if fallback_channel:
                    await asyncio.gather(
                        processing_message.delete(),
                        fallback_channel.send(f"Post {post.url} but no close match for keyword '{user_keyword}'.", files=file_payload, mention_author=False)
                    )
        elif file_payload: # No keyword or in other channel
            await asyncio.gather(
                processing_message.delete(),
                message.reply(files=file_payload, mention_author=False)
            )
       
            
        # Clean up temp folder Consider a try: except block?
        for file in file_payload:
            try:
                os.remove(file.fp.name)
            except Exception as e:
                logging.error(f"Error deleting file {file.fp.name}: {e}")
    

    # Convert ig url to "shortcode"
    def get_shortcode(self, ig_url):
        match = re.search(r'/p/([^/]+)|/reel/([^/?]+)', ig_url)
        if match:
            return match.group(1) or match.group(2)
        
async def setup(bot):
    await bot.add_cog(IGDownloader(bot))
    