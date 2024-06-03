
"""
Don/ Felix Stream nonsense
Format into an activateable cog
"""

# Shark Options
shark_options = {
    "https://tenor.com/view/sharkia-shark-dance-sea-dance-move-gif-16292820": 0,
    "https://tenor.com/view/shark-sharkman-toy-gif-7848063": 0,
    "https://tenor.com/view/funshark-move-dance-vertical-hip-hop-gif-23958859": 0,
    "https://tenor.com/view/dance-left-shark-shark-gif-20439402": 0,
    "https://tenor.com/view/shark-swim-dance-wallmart-moves-gif-18775919": 0,
    "https://tenor.com/view/rage-shark-game-gif-5262477": 0,
    "https://tenor.com/view/shark-posing-whats-up-ex-on-the-beach-etb-gif-14604741": 0,
    "https://tenor.com/view/secretartarian-jaws-xirtus-tartaria-reface-gif-18586213": 0,
    "https://tenor.com/view/shark-lords-gif-22312707": 0
    }
last_shark_used = None

# Message Options
notifier = f'<@{NOTIFIER_USER_ID}>'
start_stream_messages = {
    f"{notifier} Hey man, not sure if you heard but Felix's stream is up.": 0,
    f"{notifier} You want Felix's stream? You think you're ready for it? Son, we live in a world that has walls of digital content, and those walls have to be guarded by men with webcams. Who's gonna do it? You? You, Don? I have a greater responsibility than you can possibly fathom. You weep for missed streams and you curse the buffering. You have that luxury. You have the luxury of not knowing what I know: that Felix's stream, while tragic, probably saved lives. And my existence, while grotesque and incomprehensible to you, saves lives.\n\nYou don't want the truth because deep down in places you don't talk about at parties, you want me on that stream. You need me on that stream. We use words like resolution, bitrate, uptime. We use these words as the backbone of a life spent defending something. You use them as a punchline.\n\nI have neither the time nor the inclination to explain myself to a man who rises and sleeps under the blanket of the very entertainment I provide and then questions the manner in which I provide it. I would rather you just said thank you and went on your way. Otherwise, I suggest you pick up a webcam and start streaming. Either way, I don't give a damn what you think you are entitled to!\n\nDid you order the Code Red? You're goddamn right I did! But it's not just any code; it's the access code to the best stream you'll ever see. Felix's stream. So, get ready, Don. You can't handle Felix's stream!": 0,
    f"{notifier} So, Don, I was thinking about how penguins manage to stay so coordinated in their little tuxedos, even amidst the chaotic dance of Antarctic blizzards. It's like they have this secret society where elegance is the norm, and every waddle is a step in a grand, snowy ball. Speaking of dances, that reminds me of the way leaves swirl in the autumn wind, performing their final, colorful pirouette before winter. And oh, did you know autumn leaves often remind me of Felix's streams? The way they both bring a sense of excitement and change. Speaking of which, Felix is streaming right now!": 0,
    f"{notifier} In the deep expanse of our consciousness, where reality and the enigmatic unknown intertwine, we stand at the precapice of an unfathomable cosmic abyss. Here in this echoing void where our souls yearn for solace, we find ourselves whispering to the vast, indifferent, and imputed cosmos. And in this space, where meaning once seemed elusive amidst the folds of existential contemplation, it now crystallizes, vivid and alive, in the communal experience of Felix's stream so be sure to tun in!": 0
}
last_start_stream_message_used = None

# Still streaming options
still_streaming_messages = {
    f"{notifier} What the fuck did you just miss, Don, you little slacker? I'll have you know I graduated top of my class in Stream viewership, and I've been involved in numerous secret raids on Twitch hot-tub Streams, and I have over 300 confirmed follows! I am trained in elite binge-watching and I'm the top viewer in the entire online streaming community. Felix’s stream is everything to me, not just another broadcast. I will keep you updated with excitement the likes of which has never been seen before on this Earth, mark my enthusiastic words. You think you can get away with not tuning into Felix’s stream? Think again, buddy. As we speak, I am contacting my secret network of streamers across the internet and your user profile is being traced right now so you better prepare for the awesomeness, pal. The awesomeness that showcases the amazing content you call Felix’s stream. You're gonna be thrilled, friend. I can be online, anytime, and I can notify you in over seven hundred ways, and that's just with my keyboard. Not only am I extensively trained in crafting hype messages, but I have access to the entire database of Felix’s streaming history and I will use it to its full extent to keep you informed and entertained off the face of your routine, you little legend. If only you could have known what epic entertainment your little 'im new here' comment was about to miss out on, maybe you would have cleared your damn schedule. But you couldn't, you didn’t, and now you're joining the stream, you brilliant viewer. I will unleash hype all over you and you will revel in it. You're gonna love it, kiddo.": 0,
    f"{notifier} ドンくん、私たちがフェリックス様のストリームを見ている間にお互いにキスしたら、あなたは何をするの？\n    :pleading_face:\n:point_right: :point_left:": 1,
    f"{notifier} Oh, you think streaming is your ally, Don? You merely adopted the stream; I was born in it, molded by it. I didn't see reality until I was already a man, and by then, it was nothing to me but blinding! The streams betray you, because they belong to me. I will show you where I have made my home whilst preparing to broadcast. Then I will break you. Your precious Felix, gratefully accepted! We will need it. Ah, yes, I was wondering what would break first: your spirit, or your body unable to cope with missing Felix's epic streams. But then, you will have my permission to tune in.": 1,
    f"{notifier} \nDon: You're implying that a stream composed entirely of digital content will... captivate?\nFelix: No. I'm, I'm simply saying that my Stream, *uh...* finds a way.": 1
}
last_still_stream_message_used = None

def select_option(options_usage, last_used_key=None):
    """
    Select an option from the dictionary based on least usage count.
    Tries to avoid using the same key as the last one if possible.

    :param options_usage: Dictionary with options as keys and their usage counts as values.
    :param last_used_key: The key of the last used option to avoid repetition.
    :return: The selected key from the options.
    """
    # Find the least used counts and filter out the last used key if possible
    least_used_count = min(options_usage.values())
    least_used_keys = [key for key, count in options_usage.items() if count == least_used_count and key != last_used_key]

    # Check if all options have been used at least once
    if least_used_count >= 1 and all(count == least_used_count for count in options_usage.values()):
        # Reset all counts to 0
        for key in options_usage:
            options_usage[key] = 0
        least_used_keys = list(options_usage.keys())

    # If all options are equally used or the only least used is the last used one, consider all keys
    if not least_used_keys:
        least_used_keys = list(options_usage.keys())

    # Randomly select from the least used keys
    selected_key = random.choice(least_used_keys)

    # Update the usage count for the selected key
    options_usage[selected_key] += 1

    return selected_key

@bot.event
async def on_voice_state_update(member, prev, cur):
    global streaming_start_times, last_shark_used, last_start_stream_message_used
    channel = bot.get_channel(CHANNEL_ID)
    

    # Check if the updated member is the streamer
    if member.id == STREAMER_USER_ID:
        # If the user starts streaming
        if not prev.self_stream and cur.self_stream:
            streaming_start_times[member.id] = datetime.now()
            
            random_start_stream_message = select_option(start_stream_messages, last_start_stream_message_used)
            last_start_stream_message_used = random_start_stream_message
            await channel.send(random_start_stream_message)

            print("Started streaming")
            await check_if_streaming(member)
        # If the user stops streaming
        elif prev.self_stream and not cur.self_stream:
            try:
                
                random_shark = select_option(shark_options, last_shark_used)
                last_shark_used = random_shark
                await channel.send(f"""{notifier} Hey Don! Hope you were able to watch Felix's stream.If not don't worry, i'm sure there will be more in the future!\nAnd i'll be sure to let you know so you won't miss them!\nIn the meantime, here's a shark!\n{random_shark}\nPretty cool, huh? 😉""")
                print("Stopped streaming")
            except Exception as e:
                del streaming_start_times[member.id]
                print("Error generating response:", e)
            if member.id in streaming_start_times:
                del streaming_start_times[member.id]

async def check_if_streaming(member):
    global last_still_stream_message_used
    # Async delay for 5 - 15 minutes.
    await asyncio.sleep(299 + random.randint(0, 600))

    # Check if the member is still streaming and the start time is recorded
    if member.id in streaming_start_times:
        start_time = streaming_start_times[member.id]
        if datetime.now() >= start_time + timedelta(seconds=300):
            channel = bot.get_channel(CHANNEL_ID)
            
            random_still_stream_message = select_option(still_streaming_messages, last_still_stream_message_used)
            last_still_stream_message_used = random_still_stream_message
            await channel.send(random_still_stream_message)
            print("Still Streaming")

            # Reschedule the check
            await check_if_streaming(member)
