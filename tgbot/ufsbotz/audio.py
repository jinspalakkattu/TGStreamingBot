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
from asyncio import sleep
from pyrogram import Client
from script import HELP_TEXT
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from tgbot.utility import get_admins, get_buttons, get_playlist_str, pause, restart_playout, resume, shuffle_playlist, skip

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    admins = await get_admins(CHAT_ID)
    if query.from_user.id not in admins and query.data != "help":
        await query.answer(
            "😒 Played Joji.mp3",
            show_alert=True
        )
        return
    if query.data == "shuffle":
        if not Config.playlist:
            await query.answer("Playlist Is Empty.", show_alert=True)
            return
        await shuffle_playlist()
        await sleep(1)
        pl = await get_playlist_str()

        try:
            await query.message.edit(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "pause":
        if Config.PAUSE:
            await query.answer("Already Paused", show_alert=True)
        else:
            await pause()
            await sleep(1)
        pl = await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                                     disable_web_page_preview=True,
                                     reply_markup=await get_buttons()
                                     )
        except MessageNotModified:
            pass

    elif query.data.lower() == "resume":
        if not Config.PAUSE:
            await query.answer("Nothing Paused To Resume", show_alert=True)
        else:
            await resume()
            await sleep(1)
        pl = await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                                     disable_web_page_preview=True,
                                     reply_markup=await get_buttons()
                                     )
        except MessageNotModified:
            pass

    elif query.data == "skip":
        if not Config.playlist:
            await query.answer("No Songs In Playlist", show_alert=True)
        else:
            await skip()
            await sleep(1)
        pl = await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                                     disable_web_page_preview=True,
                                     reply_markup=await get_buttons()
                                     )
        except MessageNotModified:
            pass
    elif query.data == "replay":
        if not Config.playlist:
            await query.answer("No Songs In Playlist", show_alert=True)
        else:
            await restart_playout()
            await sleep(1)
        pl = await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                                     disable_web_page_preview=True,
                                     reply_markup=await get_buttons()
                                     )
        except MessageNotModified:
            pass

    elif query.data == "help":
        buttons = [
            [
                InlineKeyboardButton("📣 CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
                InlineKeyboardButton("👥 SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
            ],
            [
                InlineKeyboardButton("🤖 MORE BOTS", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
                InlineKeyboardButton("🧩 SOURCE CODE", url="https://github.com/jinspalakkattu/TGStreamingBot"),
            ],
            [
                InlineKeyboardButton("🏠 HOME", callback_data="home"),
                InlineKeyboardButton("❌ CLOSE", callback_data="close"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        try:
            await query.message.edit(HELP_TEXT, reply_markup=reply_markup)
        except MessageNotModified:
            pass
    await query.answer()
