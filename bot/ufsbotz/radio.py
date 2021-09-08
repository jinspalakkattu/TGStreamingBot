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
import sys
import ffmpeg
import asyncio
import subprocess
from signal import SIGINT
from config import Config, Database
from pyrogram import Client as ufs, filters
from pyrogram.types import Message
from bot.ufsbotz.player import ydl, group_call_factory

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
USERNAME = Config.BOT_USERNAME
VIDEO_CALL = Database.VIDEO_CALL
RADIO_CALL = Database.RADIO_CALL
FFMPEG_PROCESSES = Database.FFMPEG_PROCESSES


@ufs.on_message(filters.command(["radio", f"radio@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def radio(client, m: Message):
    if not ' ' in m.text:
        await m.reply_text("❗ __Send Me An Live Radio Link / YouTube Live Video Link To Start Radio Streaming!__")
        return

    text = m.text.split(' ', 1)
    query = text[1]
    input_filename = f'radio-{CHAT_ID}.raw'
    msg = await m.reply_text("🔄 `Processing ...`")

    vid_call = VIDEO_CALL.get(CHAT_ID)
    if vid_call:
        await VIDEO_CALL[CHAT_ID].stop()
        VIDEO_CALL.pop(CHAT_ID)
        await asyncio.sleep(3)

    process = FFMPEG_PROCESSES.get(CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
            await asyncio.sleep(3)
        except Exception as e:
            print(e)
            pass

    regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
    match = re.match(regex, query)
    if match:
        try:
            meta = ydl.extract_info(query, download=False)
            formats = meta.get('formats', [meta])
            for f in formats:
                ytstreamlink = f['url']
            station_stream_url = ytstreamlink
        except Exception as e:
            await msg.edit(f"❌ **YouTube Download Error!** \n\n`{e}`")
            print(e)
            return
    else:
        station_stream_url = query
        print(station_stream_url)

    process = (
        ffmpeg.input(station_stream_url)
        .output(input_filename, format='s16le', acodec='pcm_s16le', ac=2, ar='48k')
        .overwrite_output()
        .run_async()
    )
    FFMPEG_PROCESSES[CHAT_ID] = process

    if CHAT_ID in RADIO_CALL:
        await asyncio.sleep(1)
        await msg.edit(f"📻 **Started [Radio Streaming]({query})!**", disable_web_page_preview=True)
        await asyncio.sleep(2)
        await m.delete()
        await msg.delete()
    else:
        await msg.edit("🔄 `Starting Radio Stream ...`")
        await asyncio.sleep(2)
        group_call = group_call_factory.get_file_group_call(input_filename)
        try:
            await group_call.start(CHAT_ID)
            RADIO_CALL[CHAT_ID] = group_call
            await msg.edit(f"📻 **Started [Radio Streaming]({query})!**", disable_web_page_preview=True)
            await asyncio.sleep(2)
            await m.delete()
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
