# Discord_Bot
A Discord bot designed to provide some simple functionalities. 

Built using discord.py

## Current Features
ig_download: Review a chosen channel or channels for instagram posts with a reel or video and repost the downloaded video.

## Setup
- Create a `.env` file with your discord token in the following format:
```
DISCORD_TOKEN=MTE1MzEyO...
```
- Manually add your discord channel's ID to the `allowed_channels.yaml` file or use `/allow` in the channel you want the bot to have access to. 
    - Use `/deny` to remove the bot's access to a channel
- Run the bot with `python bot.py`
- Use `/sync` in any channel to sync the `/` commands so they show up in the command suggestion pop-up.
- Now the bot will monitor a channel for posts with instagram.com `\p\` or `\reel\` and reply with a video contained in the link.

### Prerequisites
- Discord bot token

### Installation
1. Clone this repository:
```bash
git clone https://github.com/Coding4Humans/Discord_Bot.git
cd Discord_Bot
```

### Install  Dependencies
```
pip install -r requirements.txt
```
### Cogs
This bot uses cogs to organize command groups and event listeners. Place your cog files in the cogs directory.

### Contact
For any inquiries, please open an issue or contact the repository owner.

