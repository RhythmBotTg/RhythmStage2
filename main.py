
import re
import glob
from plugins import *
from lib import config
from pyrogram.client import Client
from pyrogram.types.messages_and_media import Message

rhythm = Client(config.SESSION,api_id=int(config.API_ID),api_hash=config.API_HASH ,bot_token=config.TOKEN)



@rhythm.on_message()
async def main(bot:Client,msg:Message) :
    chat_type = str(msg.chat.type)

    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    spotify_regex = (
            r'(https?://)?(open\.)?'
            '(spotify)\.(com)/'
            '(track|album|playlist)'
            )



#Regex
    spotify_match = re.match(spotify_regex, msg.text)
    youtube_regex_match = re.match(youtube_regex, msg.text)




    if spotify_match :
        await spotify.spotify(bot,msg)

    elif youtube_regex_match:
        await youtube.yt_mp3(bot,msg)
    else :
        await getsong.searchNget(bot,msg)

    if chat_type.split(".")[1] == "PRIVATE" :
        pass
print("started")
rhythm.run()