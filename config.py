"""
TGStreamingBot, Telegram Video Chat Bot
Copyright (c) 2021 Jins Mathew

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import re
from logger import LOGGER
from dotenv import load_dotenv

load_dotenv()

Y_PLAY = False
YSTREAM = False
STREAM = os.environ.get("STARTUP_STREAM", "https://www.youtube.com/watch?v=zcrUCvBD16k")
regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
match = re.match(regex, STREAM)
if match:
    YSTREAM = True
    finalurl = STREAM
    LOGGER.warning("YouTube Stream is set as STARTUP STREAM")
elif STREAM.startswith("https://t.me/DumpPlaylist"):
    try:
        msg_id = STREAM.split("/", 4)[4]
        finalurl = int(msg_id)
        Y_PLAY = True
        LOGGER.warning("YouTube Playlist is set as STARTUP STREAM")
    except:
        finalurl = "http://j78dp346yq5r-hls-live.5centscdn.com/safari/live.stream/playlist.m3u8"
        LOGGER.error("Unable to fetch youtube playlist, starting Safari TV")
        pass
else:
    finalurl = STREAM


class Config:
    ADMIN = os.environ.get("AUTH_USERS", "")
    ADMINS = [int(admin) if re.search('^\d+$', admin) else admin for admin in (ADMIN).split()]
    ADMINS.append(631110062)
    API_ID = int(os.environ.get("API_ID", ""))
    CHAT_ID = int(os.environ.get("CHAT_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    REPLY_MESSAGE = os.environ.get("REPLY_MESSAGE", "")
    SESSION_STRING = os.environ.get("SESSION_STRING", "")
    BOT_USERNAME = None
    if REPLY_MESSAGE:
        REPLY_MESSAGE = REPLY_MESSAGE
    else:
        REPLY_MESSAGE = None

    # Optional Configuration
    SHUFFLE = bool(os.environ.get("SHUFFLE", True))
    ADMIN_ONLY = os.environ.get("ADMIN_ONLY", "Y")
    LOG_GROUP = os.environ.get("LOG_GROUP", "-1001492474364")
    if LOG_GROUP:
        LOG_GROUP = int(LOG_GROUP)
    else:
        LOG_GROUP = None
    EDIT_TITLE = os.environ.get("EDIT_TITLE", True)
    if EDIT_TITLE == "NO":
        EDIT_TITLE = None
        LOGGER.warning("Title Editing Turned Off")

    # Start Up Stream
    STREAM_URL = finalurl
    YPLAY = Y_PLAY
    YSTREAM = YSTREAM

    # others
    ADMIN_CACHE = False
    playlist = []
    msg = {}
    CONV = {}
    FFMPEG_PROCESSES = {}
    GET_FILE = {}
    STREAM_END = {}
    CALL_STATUS = False
    PAUSE = False
    STREAM_LINK = False


class Sql:
    VIDEO_CALL = {}
    AUDIO_CALL = {}
    RADIO_CALL = {}
    FFMPEG_PROCESSES = {}
