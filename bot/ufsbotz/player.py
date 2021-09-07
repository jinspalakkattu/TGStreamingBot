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
import time
import ffmpeg
import asyncio
from os import path
from asyncio import sleep
from config import Config
from bot.ufsbotz.nopm import User
from youtube_dl import YoutubeDL
from pyrogram import Client as ufs, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
USERNAME = Config.BOT_USERNAME

STREAM = {6}
VIDEO_CALL = {}

ydl_opts = {
    "geo_bypass": True,
    "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)
group_call_factory = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)


@ufs.on_message(filters.command(["stream", f"stream@{USERNAME}"]) & filters.user(ADMINS) & (
        filters.chat(CHAT_ID) | filters.private))
async def stream(client, m: Message):
    if 1 in STREAM:
        if CHAT_ID in VIDEO_CALL:
            await VIDEO_CALL[CHAT_ID].stop()
            VIDEO_CALL.pop(CHAT_ID)
            try:
                STREAM.remove(1)
            except:
                pass
            try:
                STREAM.add(0)
            except:
                pass
        # await m.reply_text("🤖 **Please Stop The Existing Stream!**")
        # return

    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply_text(
            "❗ __Send Me An YouTube Video Link / Live Stream Link / Reply To An Video To Start Streaming!__")

    elif ' ' in m.text:
        msg = await m.reply_text("🔄 `Processing ...`")
        text = m.text.split(' ', 1)
        query = text[1]
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, query)
        if match:
            await msg.edit("🔄 `Starting YouTube Stream ...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                    ytstreamlink = f['url']
                ytstream = ytstreamlink
            except Exception as e:
                await msg.edit(f"❌ **YouTube Download Error!** \n\n`{e}`")
                print(e)
                return
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(CHAT_ID)
                await group_call.start_video(ytstream)
                VIDEO_CALL[CHAT_ID] = group_call
                # await msg.edit(f"▶️ **Started [YouTube Streaming]({query})!**", disable_web_page_preview=True)
                await m.delete()
                await msg.delete()
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
        else:
            await msg.edit("🔄 `Starting Live Stream ...`")
            livestream = query
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(CHAT_ID)
                await group_call.start_video(livestream)
                VIDEO_CALL[CHAT_ID] = group_call
                # await msg.edit(f"▶️ **Started [Live Streaming]({query})!**", disable_web_page_preview=True)
                await m.delete()
                await msg.delete()
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")

    elif media.video or media.document:
        msg = await m.reply_text("🔄 `Downloading ...`")
        video = await client.download_media(media)
        await sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(CHAT_ID)
            await group_call.start_video(video)
            VIDEO_CALL[CHAT_ID] = group_call
            # await msg.edit("▶️ **Started Video Streaming!**")
            await m.delete()
            await msg.delete()
            try:
                STREAM.remove(0)
            except:
                pass
            try:
                STREAM.add(1)
            except:
                pass
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
    else:
        await m.reply_text(
            "❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Video To Start Streaming!__")
        return


@ufs.on_message(filters.command(["endstream", f"endstream@{USERNAME}"]) & filters.user(ADMINS) & (
        filters.chat(CHAT_ID) | filters.private))
async def endstream(client, m: Message):
    if 0 in STREAM:
        await m.reply_text("🤖 **Please Start An Stream First!**")
        return

    msg = await m.reply_text("🔄 `Processing ...`")
    if CHAT_ID in VIDEO_CALL:
        await VIDEO_CALL[CHAT_ID].stop()
        VIDEO_CALL.pop(CHAT_ID)
        await msg.edit("⏹️ **Stopped Video Streaming!**")
        await asyncio.sleep(2)
        await m.delete()
        await msg.delete()
        try:
            STREAM.remove(1)
        except:
            pass
        try:
            STREAM.add(0)
        except:
            pass
    else:
        await msg.edit("🤖 **Please Start An Stream First!**")


admincmds = ["stream", "radio", "stopradio", "endstream", f"stream@{USERNAME}", f"radio@{USERNAME}",
             f"stopradio@{USERNAME}", f"endstream@{USERNAME}"]


@ufs.on_message(filters.command(admincmds) & ~filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private))
async def notforu(_, m: Message):
    k = await m.reply_sticker("CAACAgUAAxkBAAEBpyZhF4R-ZbS5HUrOxI_MSQ10hQt65QACcAMAApOsoVSPUT5eqj5H0h4E")
    await sleep(5)
    await k.delete()
    try:
        await m.delete()
    except:
        pass


allcmd = ["start", "help", f"start@{USERNAME}", f"help@{USERNAME}"] + admincmds


@ufs.on_message(filters.command(allcmd) & filters.group & ~filters.chat(CHAT_ID))
async def not_chat(_, m: Message):
    buttons = [
        [
            InlineKeyboardButton("CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
            InlineKeyboardButton("SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
        ],
        [
            InlineKeyboardButton("🤖 MAKE YOUR OWN BOT 🤖", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
        ]
    ]
    await m.reply_text(
        text="**Sorry, You Can't Use This Bot In This Group 🤷‍♂️! But You Can Make Your Own Bot Like This From The ["
             "Source Code](https://t.me/joinchat/6YRhp5LyjXNkNGY0) Below 😉!**",
        reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
