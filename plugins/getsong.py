import os
import asyncio
from lib import config
from time import sleep
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
import spotipy
from pydub import AudioSegment
from pyrogram import Client
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram.types.messages_and_media import Message


credentials = SpotifyClientCredentials(client_id=config.CLIENT_ID,client_secret=config.SECRET)
sp = spotipy.Spotify(client_credentials_manager=credentials)





async def searchNget(bot:Client,msg:Message) :
    chat_id = msg.chat.id
    query = str(msg.text)
    message = await msg.reply("downloading")
    raw_data = sp.search(query)["tracks"]
    fltData = raw_data["items"]
    try :
        link = fltData[0]["external_urls"]["spotify"]
        artist_name = fltData[0]["artists"][0]["name"]
        song_name = fltData[0]["name"]
    except :
        await msg.reply_text("404 song not foᥙnd")
        return
    fltsearch = f"{query} {artist_name}"


    result = YoutubeSearch(fltsearch, max_results=1).to_dict()[0]["url_suffix"]
    video_info = YoutubeDL().extract_info(url =f"https://youtube.com{result}",download=False)
    filename = f"{video_info['title']}"
    options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
            }

    with YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    AudioSegment.from_wav(f"{filename}").export(f"{filename}.mp3", format="mp3")
    await msg.reply_document(f"{filename}.mp3",quote=False)
    await bot.delete_messages(chat_id,message_ids=message.id)
    os.remove(filename)
    os.remove(f"{filename}.mp3")
