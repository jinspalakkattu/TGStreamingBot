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
import time
import ffmpeg
import asyncio
import subprocess
from asyncio import sleep
from youtube_dl import YoutubeDL
from bot.ufsbotz.nopm import User
from pyrogram.types import Message
from bot.ufsbotz.misc import USERNAME
from pytgcalls import GroupCallFactory
from bot.config import Config, Sql as db
from pyrogram import Client as ufs, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
VIDEO_CALL = db.VIDEO_CALL
AUDIO_CALL = db.AUDIO_CALL


ydl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)
group_call = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()


@ufs.on_message(filters.command(["stream", f"stream@{USERNAME}"]) & filters.user(ADMINS) & filters.chat(CHAT_ID) | filters.private)
async def stream(client, m: Message):
    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply_text(
            "❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Video To Start Video Streaming !__")

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
        match = re.match(regex,query)
        if match:
            await msg.edit("🔄 `Starting YouTube Stream ...`")
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
                await group_call.start_video(ytstream, with_audio=True, repeat=False)
                VIDEO_CALL[chat_id] = group_call
                await msg.edit(f"▶️ **Started [YouTube Streaming]({query}) !**", disable_web_page_preview=True)
                await sleep(2)
                await m.delete()
                await msg.delete()
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
        else:
            await msg.edit("🔄 `Starting Live Stream ...`")
            livestream = query
            await sleep(2)
            try:
                await group_call.join(chat_id)
                await group_call.start_video(livestream, with_audio=True, repeat=False)
                VIDEO_CALL[chat_id] = group_call
                await msg.edit(f"▶️ **Started [Live Streaming]({query}) !**", disable_web_page_preview=True)
                await sleep(2)
                await m.delete()
                await msg.delete()
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")

    elif media.video or media.document:
        chat_id = m.chat.id
        msg = await m.reply_text("🔄 `Downloading ...`")
        video = await client.download_media(media)
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
            await group_call.start_video(video, with_audio=True, repeat=False)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit(f"▶️ **Started [Video Streaming](https://t.me/lnc3f3r) !**",
                           disable_web_page_preview=True)
            await sleep(2)
            await m.delete()
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured !** \n\nError: `{e}`")

    else:
        await m.reply_text(
            "❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Video To Start Video Streaming!__")


@ufs.on_message(filters.command(["pause", f"pause@{USERNAME}"]) & filters.user(ADMINS) & filters.chat(CHAT_ID) | filters.private)
async def pause(_, m: Message):
    chat_id = m.chat.id

    if chat_id in AUDIO_CALL:
        await AUDIO_CALL[chat_id].set_audio_pause(True)
        await m.reply_text("⏸ **Paused Audio Streaming !**")
        await sleep(2)
        await m.delete()

    elif chat_id in VIDEO_CALL:
        await VIDEO_CALL[chat_id].set_video_pause(True)
        await m.reply_text("⏸ **Paused Video Streaming !**")
        await sleep(2)
        await m.delete()

    else:
        await m.reply_text("❌ **Noting Is Streaming !**")
        await sleep(2)
        await m.delete()


@ufs.on_message(filters.command(["resume", f"resume@{USERNAME}"]) & filters.user(ADMINS) & filters.chat(CHAT_ID) | filters.private)
async def resume(_, m: Message):
    chat_id = m.chat.id

    if chat_id in AUDIO_CALL:
        await AUDIO_CALL[chat_id].set_audio_pause(False)
        await m.reply_text("▶️ **Resumed Audio Streaming !**")
        await sleep(2)
        await m.delete()

    elif chat_id in VIDEO_CALL:
        await VIDEO_CALL[chat_id].set_video_pause(False)
        await m.reply_text("▶️ **Resumed Video Streaming !**")
        await sleep(2)
        await m.delete()

    else:
        await m.reply_text("❌ **Noting Is Streaming !**")
        await sleep(2)
        await m.delete()


@ufs.on_message(filters.command(["endstream", f"endstream@{USERNAME}"]) & filters.user(ADMINS) & filters.chat(CHAT_ID) | filters.private)
async def endstream(client, m: Message):
    msg = await m.reply_text("🔄 `Processing ...`")
    chat_id = m.chat.id

    if chat_id in AUDIO_CALL:
        await AUDIO_CALL[chat_id].stop()
        AUDIO_CALL.pop(chat_id)
        await msg.edit("⏹️ **Stopped Audio Streaming !**")
        await sleep(2)
        await m.delete()
        await msg.delete()

    elif chat_id in VIDEO_CALL:
        await VIDEO_CALL[chat_id].stop()
        VIDEO_CALL.pop(chat_id)
        await msg.edit("⏹️ **Stopped Video Streaming !**")
        await sleep(2)
        await m.delete()
        await msg.delete()

    else:
        await msg.edit("🤖 **Please Start An Stream First !**")
        await sleep(2)
        await m.delete()
        await msg.delete()


admincmds=["stream", "play", "pause", "resume", "endstream", "restart", f"restart@{USERNAME}", f"stream@{USERNAME}", f"play@{USERNAME}", f"pause@{USERNAME}", f"resume@{USERNAME}", f"endstream@{USERNAME}"]


@ufs.on_message(filters.command(admincmds) & ~filters.user(ADMINS) & filters.chat(CHAT_ID))
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
            InlineKeyboardButton("🤖 MAKE YOUR OWN BOT 🤖", url="https://github.com/jinspalakkattu/TGStreamingBot"),
        ]
    ]
    await m.reply_text(
        text="**Sorry, You Can't Use This Bot In This Group 🤷‍♂️! But You Can Make Your Own Bot Like This From The ["
             "Source Code](https://github.com/jinspalakkattu/TGStreamingBot) Below 😉!**",
        reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


# pytgcalls handlers

@group_call.on_audio_playout_ended
async def audio_ended_handler(_, __):
    await group_call.stop()
    print("[INFO] - AUDIO_CALL ENDED !")


@group_call.on_video_playout_ended
async def video_ended_handler(_, __):
    await group_call.stop()
    print("[INFO] - VIDEO_CALL ENDED !")