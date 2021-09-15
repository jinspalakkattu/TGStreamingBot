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
import json
from config import Config
from pyrogram.types import Message
from pyrogram import Client as ufs, filters
from tgbot.utility import get_buttons, is_admin, get_playlist_str, shuffle_playlist, import_play_list

admin_filter = filters.create(is_admin)


@ufs.on_message(filters.command(["export", f"export@{Config.BOT_USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def export_play_list(client, message: Message):
    if not Config.playlist:
        await message.reply_text("Playlist Is Empty")
        return
    file = f"{message.chat.id}_{message.message_id}.json"
    with open(file, 'w+') as outfile:
        json.dump(Config.playlist, outfile, indent=4)
    await client.send_document(chat_id=message.chat.id, document=file, file_name="PlayList.json",
                               caption=f"Playlist\n\nNumber Of Songs: <code>{len(Config.playlist)}</code>"
                                       f"\n\nJoin [𝙐𝙁𝙎 𝘽𝙤𝙩𝙯](https://t.me/joinchat/7qlEga5lO0o2MTg0)")
    try:
        os.remove(file)
    except:
        pass


@ufs.on_message(filters.command(["import", f"import@{Config.BOT_USERNAME}"]) & admin_filter & (
        filters.chat(Config.CHAT_ID) | filters.private))
async def import_playlist(client, m: Message):
    if m.reply_to_message is not None and m.reply_to_message.document:
        if m.reply_to_message.document.file_name != "PlayList.json":
            k = await m.reply(
                "Invalid PlayList File Given. Use @GetPlayListBot To Get A Playlist File. Or Export Your Current "
                "Playlist Using /export.")
            return
        myplaylist = await m.reply_to_message.download()
        status = await m.reply("Trying To Get Details From Playlist.")
        n = await import_play_list(myplaylist)
        if not n:
            await status.edit("Errors Occurred While Importing Playlist.")
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
        await m.reply(
            "No PlayList File Given. Use @GetPlayListBot  Or Search For A Playlist In @DumpPlaylist To Get A Playlist "
            "File.")
