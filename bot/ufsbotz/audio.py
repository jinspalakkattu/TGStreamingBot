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
from asyncio import sleep
from pyrogram.types import Message
from bot.ufsbotz.misc import USERNAME
from bot.config import Config, Sql as db
from pyrogram import Client as ufs, filters
from bot.ufsbotz.video import ydl, group_call

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
VIDEO_CALL = db.VIDEO_CALL
AUDIO_CALL = db.AUDIO_CALL


@ufs.on_message(filters.command(["play", f"play@{USERNAME}"]) & filters.user(ADMINS) & filters.chat(CHAT_ID) | filters.private)
async def play(client, m: Message):
    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply_text(
            "❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Audio To Start Audio Streaming !__")

    elif ' ' in m.text:
        text = m.text.split(' ', 1)
        query = text[1]
        chat_id = m.chat.id
        msg = await m.reply_text("🔄 `Processing ...`")

        vid_call = VIDEO_CALL.get(chat_id)
        if vid_call:
            await VIDEO_CALL[chat_id].stop()
            VIDEO_CALL.pop(chat_id)
            await sleep(3)

        aud_call = AUDIO_CALL.get(chat_id)
        if aud_call:
            await AUDIO_CALL[chat_id].stop()
            AUDIO_CALL.pop(chat_id)
            await sleep(3)

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, query)
        if match:
            await msg.edit("🔄 `Starting YouTube Playback ...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                        ytstreamlink = f['url']
                ytstream = ytstreamlink
            except Exception as e:
                await msg.edit(f"❌ **YouTube Download Error !** \n\n`{e}`")
                print(e)
                return
            await sleep(2)
            try:
                await group_call.join(chat_id)
                await group_call.start_audio(ytstream, repeat=False)
                AUDIO_CALL[chat_id] = group_call
                await msg.edit(f"▶️ **Started [YouTube Playback]({query}) !**", disable_web_page_preview=True)
                await asyncio.sleep(2)
                await m.delete()
                await msg.delete()
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
        else:
            await msg.edit("🔄 `Starting Radio Stream ...`")
            livestream = query
            await sleep(2)
            try:
                await group_call.join(chat_id)
                await group_call.start_audio(livestream, repeat=False)
                AUDIO_CALL[chat_id] = group_call
                await msg.edit(f"▶️ **Started [Radio Streaming]({query}) !**", disable_web_page_preview=True)
                await asyncio.sleep(2)
                await m.delete()
                await msg.delete()
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")

    elif media.audio or media.document:
        chat_id = m.chat.id
        msg = await m.reply_text("🔄 `Downloading ...`")
        audio = await client.download_media(media)
        await msg.edit("🔄 `Processing ...`")
        await sleep(2)

        vid_call = VIDEO_CALL.get(chat_id)
        if vid_call:
            await VIDEO_CALL[chat_id].stop()
            VIDEO_CALL.pop(chat_id)
            await sleep(3)

        aud_call = AUDIO_CALL.get(chat_id)
        if aud_call:
            await AUDIO_CALL[chat_id].stop()
            AUDIO_CALL.pop(chat_id)
            await sleep(3)

        try:
            await group_call.join(chat_id)
            await group_call.start_audio(audio, repeat=False)
            AUDIO_CALL[chat_id] = group_call
            await msg.edit(f"▶️ **Started [Audio Streaming](https://t.me/lnc3f3r) !**",
                           disable_web_page_preview=True)
            await asyncio.sleep(2)
            await m.delete()
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")

    else:
        await m.reply_text(
            "❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Audio To Start Audio Streaming !__")


@ufs.on_message(filters.command(["restart", f"restart@{USERNAME}"]) & filters.user(ADMINS) & filters.chat(CHAT_ID) | filters.private)
async def restart(client, m: Message):
    k = await m.reply_text("🔄 `Restarting ...`")
    await sleep(3)
    os.execl(sys.executable, sys.executable, *sys.argv)
    try:
        await k.edit("✅ **Restarted Successfully! \nJoin !**")
    except:
        pass
