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

import re
import asyncio
from asyncio import sleep
from logger import LOGGER
from datetime import datetime
from youtube_dl import YoutubeDL
from pyrogram.types import Message
from config import Config, Sql as db
from youtube_search import YoutubeSearch
from pyrogram import Client as ufs, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.utility import download, get_admins, is_admin, get_buttons, get_link, import_play_list, leave_call, play, \
    get_playlist_str, send_playlist, shuffle_playlist, start_stream, stream_from_link

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
USERNAME = Config.BOT_USERNAME
VIDEO_CALL = db.VIDEO_CALL
AUDIO_CALL = db.AUDIO_CALL

ydl_opts = {
    "quiet": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)

admin_filter = filters.create(is_admin)


@ufs.on_message(
    filters.command(["stream", f"stream@{USERNAME}"]) & filters.user(ADMINS) & filters.chat(CHAT_ID) | filters.private)
async def stream(client, m: Message):
    if Config.ADMIN_ONLY == "Y":
        admins = await get_admins(Config.CHAT_ID)
        if m.from_user.id not in admins:
            await m.reply_sticker("CAACAgUAAxkBAAEBpyZhF4R-ZbS5HUrOxI_MSQ10hQt65QACcAMAApOsoVSPUT5eqj5H0h4E")
            return

    type = ""
    yturl = ""
    ysearch = ""
    if m.reply_to_message and m.reply_to_message.video:
        msg = await m.reply_text("🔄  **Processing ...**")
        type = 'video'
        m_video = m.reply_to_message.video
    elif m.reply_to_message and m.reply_to_message.document:
        msg = await m.reply_text("🔄  **Processing ...**")
        m_video = m.reply_to_message.document
        type = 'video'
        if not "video" in m_video.mime_type:
            rtn = await msg.edit("The Given File Is Invalid")
            await asyncio.sleep(3)
            await m.delete()
            await rtn.delete()
            return
    else:
        if m.reply_to_message:
            link = m.reply_to_message.text
            regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
            match = re.match(regex, link)
            if match:
                type = "youtube"
                yturl = link
        elif " " in m.text:
            text = m.text.split(" ", 1)
            query = text[1]
            regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
            match = re.match(regex, query)
            if match:
                type = "youtube"
                yturl = query
            else:
                type = "query"
                ysearch = query
        else:
            await m.reply_text("You Didn't Gave Me Anything To Play.Reply To A Video Or A Youtube Link.")
            return
    user = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    if type == "video":
        now = datetime.now()
        nyav = now.strftime("%d-%m-%Y-%H:%M:%S")
        data = {1: m_video.file_name, 2: m_video.file_id, 3: "telegram", 4: user, 5: f"{nyav}_{m_video.file_size}"}
        Config.playlist.append(data)
        await msg.edit("Media added to playlist")
    if type == "youtube" or type == "query":
        if type == "youtube":
            msg = await m.reply_text("🔄 **Start Fetching Video From YouTube...**")
            url = yturl
        elif type == "query":
            try:
                msg = await m.reply_text("🔄 **Start Fetching Video From YouTube...**")
                ytquery = ysearch
                results = YoutubeSearch(ytquery, max_results=1).to_dict()
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
            except Exception as e:
                rtn = await msg.edit("Song Not Found.\nTry Inline Mode..")
                LOGGER.error(str(e))
                await asyncio.sleep(3)
                await rtn.delete()
                return
        else:
            return
        ydl_opts = {
            "geo-bypass": True,
            "nocheckcertificate": True
        }
        ydl = YoutubeDL(ydl_opts)
        try:
            info = ydl.extract_info(url, False)
        except Exception as e:
            LOGGER.error(e)
            await msg.edit(
                f"YouTube Download Error ❌\nError:- {e}"
            )
            LOGGER.error(str(e))
            return
        title = info["title"]
        now = datetime.now()
        nyav = now.strftime("%d-%m-%Y-%H:%M:%S")
        data = {1: title, 2: url, 3: "youtube", 4: user, 5: f"{nyav}_{m.from_user.id}"}
        Config.playlist.append(data)
        await msg.edit(f"[{title}]({url}) Added To Playlist", disable_web_page_preview=True)
    if len(Config.playlist) == 1:
        m_status = await msg.edit("Downloading & Processing...")
        await download(Config.playlist[0], m_status)
        await play()
        await m_status.delete()
    else:
        await send_playlist()
    pl = await get_playlist_str()
    if m.chat.type == "private":
        await m.reply(pl, reply_markup=await get_buttons(), disable_web_page_preview=True)
    elif not Config.LOG_GROUP and m.chat.type == "supergroup":
        await m.reply(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
    for track in Config.playlist[:2]:
        await download(track)


@ufs.on_message(filters.command(["leave", f"leave@{USERNAME}"]) & admin_filter | filters.private)
async def leave_voice_chat(_, m: Message):
    if not Config.CALL_STATUS:
        return await m.reply("Not Joined Any Voice Chat.")
    await leave_call()
    await m.reply("Successfully Left Video Chat.")
    await asyncio.sleep(2)
    await m.delete()


@ufs.on_message(filters.command(["shuffle", f"shuffle@{USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def shuffle_play_list(client, m: Message):
    if not Config.CALL_STATUS:
        msg = await m.reply("Not Joined Any Voice Chat.")
        await asyncio.sleep(2)
        await msg.delete()
        await m.delete()
        return
    else:
        if len(Config.playlist) > 2:
            msg = await m.reply_text(f"Playlist Shuffled.")
            await shuffle_playlist()
            await asyncio.sleep(2)
            await msg.delete()
            await m.delete()
            return
        else:
            msg = await m.reply_text(f"You Cant Shuffle Playlist With Less Than 3 Songs.")
            await asyncio.sleep(3)
            await msg.delete()
            await m.delete()
            return


@ufs.on_message(filters.command(["clearplaylist", f"clearplaylist@{USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def clear_play_list(client, m: Message):
    if not Config.CALL_STATUS:
        msg = await m.reply("Not Joined Any Voice Chat.")
        await asyncio.sleep(2)
        await msg.delete()
        await m.delete()
        return
    if not Config.playlist:
        msg = await m.reply("Playlist Is Empty. May Be Live Streaming.")
        await asyncio.sleep(2)
        await msg.delete()
        await m.delete()
        return
    Config.playlist.clear()
    msg = await m.reply_text(f"Playlist Cleared.")
    await start_stream()
    await asyncio.sleep(2)
    await msg.delete()
    await m.delete()
    return


@ufs.on_message(filters.command(["yplay", f"yplay@{USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def yt_play_list(client, m: Message):
    if m.reply_to_message is not None and m.reply_to_message.document:
        if m.reply_to_message.document.file_name != "YouTube_PlayList.json":
            msg = await m.reply(
                "Invalid PlayList File Given. Use @GetPlayListBot  Or Search For A Playlist In @DumpPlaylist To Get A "
                "Playlist File.")
            await asyncio.sleep(5)
            await msg.delete()
            await m.delete()
            return
        ytplaylist = await m.reply_to_message.download()
        status = await m.reply("Trying To Get Details From Playlist.")
        n = await import_play_list(ytplaylist)
        if not n:
            await status.edit("Errors Occurred While Importing Playlist.")
            await asyncio.sleep(3)
            await status.delete()
            await m.delete()
            return
        if Config.SHUFFLE:
            await shuffle_playlist()
        pl = await get_playlist_str()
        if m.chat.type == "private":
            await status.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
        elif not Config.LOG_GROUP and m.chat.type == "supergroup":
            await status.edit(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
        else:
            await status.delete()
    else:
        msg = await m.reply(
            "No playList File Given. Use @GetPlayListBot  Or Search For A Playlist In @DumpPlaylist To Get A Playlist "
            "File.")
        await asyncio.sleep(3)
        await msg.delete()
        await m.delete()
        return


@ufs.on_message(filters.command(["stream", f"stream@{USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def stream(client, m: Message):
    if m.reply_to_message:
        link = m.reply_to_message.text
    elif " " in m.text:
        text = m.text.split(" ", 1)
        link = text[1]
    else:
        return await m.reply("Provide A Link To Stream!")
    regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
    match = re.match(regex, link)
    if match:
        stream_link = await get_link(link)
        if not stream_link:
            msg = await m.reply("This Is An Invalid Link.")
            await asyncio.sleep(3)
            await msg.delete()
            await m.delete()
            return
    else:
        stream_link = link
    msg = await m.reply(f"▶ Started [Streaming]({stream_link}).", disable_web_page_preview=True)
    await stream_from_link(stream_link)
    await asyncio.sleep(3)
    await msg.delete()
    await m.delete()
    return


admincmds = ["yplay", "leave", "pause", "resume", "skip", "restart", "volume", "shuffle", "clearplaylist", "export",
             "import", "update", 'replay', 'logs', 'stream', f'stream@{USERNAME}',
             f'logs@{USERNAME}', f"replay@{USERNAME}", f"yplay@{USERNAME}",
             f"leave@{USERNAME}", f"pause@{USERNAME}", f"resume@{USERNAME}",
             f"skip@{USERNAME}", f"restart@{USERNAME}", f"volume@{USERNAME}",
             f"shuffle@{USERNAME}", f"clearplaylist@{USERNAME}", f"export@{USERNAME}",
             f"import@{USERNAME}", f"update@{USERNAME}"]


@ufs.on_message(filters.command(admincmds) & ~filters.user(ADMINS) & filters.chat(CHAT_ID))
async def notforu(_, m: Message):
    k = await _.send_cached_media(chat_id=m.chat.id,
                                  file_id="CAACAgUAAxkBAAEBpyZhF4R-ZbS5HUrOxI_MSQ10hQt65QACcAMAApOsoVSPUT5eqj5H0h4E",
                                  caption="You Are Not Authorized", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('⚡️Join Here', url='https://t.me/joinchat/7qlEga5lO0o2MTg0')]]))

    await sleep(5)
    await k.delete()
    try:
        await m.delete()
    except:
        pass

allcmd = ["play", "player", f"play@{USERNAME}", f"player@{USERNAME}"] + admincmds


@ufs.on_message(filters.command(allcmd) & ~filters.chat(Config.CHAT_ID) & filters.group)
async def not_chat(_, m: Message):
    buttons = [
        [
            InlineKeyboardButton("📣 CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
            InlineKeyboardButton("👥 SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
        ],
        [
            InlineKeyboardButton("🤖 MAKE YOUR OWN BOT 🤖", url="https://github.com/jinspalakkattu/TGStreamingBot"),
        ]
    ]
    await m.reply_text(
        text="**Sorry, You Can't Use This Bot In This Group 🤷‍♂️! But You Can Make Your Own Bot Like This From The ["
             "Source Code](https://github.com/jinspalakkattu/TGStreamingBot) Below 😉!**",
        reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
