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

from config import Config
from pyrogram.types import Message
from pyrogram import Client as ufs, filters
from tgbot.utility import get_playlist_str, get_admins, is_admin, \
    restart_playout, skip, pause, resume, volume, get_buttons

admin_filter = filters.create(is_admin)


@ufs.on_message(
    filters.command(["player", f"player@{Config.BOT_USERNAME}"]) & (filters.chat(Config.CHAT_ID) | filters.private))
async def player(client, message):
    pl = await get_playlist_str()
    if message.chat.type == "private":
        await message.reply_text(
            pl,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=await get_buttons()
        )
    else:
        if Config.msg.get('playlist') is not None:
            await Config.msg['playlist'].delete()
        Config.msg['playlist'] = await message.reply_text(
            pl,
            disable_web_page_preview=True,
            parse_mode="Markdown",
            reply_markup=await get_buttons()
        )


@ufs.on_message(filters.command(["skip", f"skip@{Config.BOT_USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def skip_track(_, m: Message):
    if not Config.playlist:
        await m.reply("Playlist is Empty.\nLive Streaming.")
        return
    if len(m.command) == 1:
        await skip()
    else:
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            for i in items:
                if 2 <= i <= (len(Config.playlist) - 1):
                    Config.playlist.pop(i)
                    await m.reply(f"Successfully Removed From Playlist- {i}. **{Config.playlist[i][1]}**")
                else:
                    await m.reply(f"You Cant Skip First Two Songs- {i}")
        except (ValueError, TypeError):
            await m.reply_text("Invalid input")
    pl = await get_playlist_str()
    if m.chat.type == "private":
        await m.reply_text(pl, disable_web_page_preview=True, reply_markup=await get_buttons())
    elif not Config.LOG_GROUP and m.chat.type == "supergroup":
        await m.reply_text(pl, disable_web_page_preview=True, reply_markup=await get_buttons())


@ufs.on_message(filters.command(["pause", f"pause@{Config.BOT_USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def pause_playing(_, m: Message):
    if Config.PAUSE:
        return await m.reply("Already Paused")
    if not Config.CALL_STATUS:
        return await m.reply("Not Playing Anything.")
    await m.reply("Paused Video Call")
    await pause()


@ufs.on_message(filters.command(["resume", f"resume@{Config.BOT_USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def resume_playing(_, m: Message):
    if not Config.PAUSE:
        return await m.reply("Nothing Paused To Resume")
    if not Config.CALL_STATUS:
        return await m.reply("Not Playing Anything.")
    await m.reply("Resumed Video Call")
    await resume()


@ufs.on_message(filters.command(['volume', f"volume@{Config.BOT_USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def set_vol(_, m: Message):
    if not Config.CALL_STATUS:
        return await m.reply("Not Playing Anything.")
    if len(m.command) < 2:
        await m.reply_text('You Forgot To Pass Volume (1-200).')
        return
    await m.reply_text(f"Volume Set To {m.command[1]}")
    await volume(int(m.command[1]))


@ufs.on_message(filters.command(["replay", f"replay@{Config.BOT_USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def replay_playout(client, m: Message):
    if not Config.CALL_STATUS:
        return await m.reply("Not Playing Anything.")
    await m.reply_text(f"Replaying From Beginning")
    await restart_playout()
