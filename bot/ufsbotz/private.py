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
import asyncio
from config import Config
from bot.ufsbotz.misc import USERNAME
from pyrogram import Client as ufs, filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

CHAT_ID = Config.CHAT_ID

HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**, \n\nI'm **TG Streaming Bot**. \nI Can Stream Lives, Radios, " \
            "YouTube Videos & Telegram Video Files On Voice Chat Of Telegram Channels & Groups 😉! \n\n**Made With ❤️ " \
            "By @lnc3f3r!** 👑 "
HELP_TEXT = """
🏷️ --**Setting Up**-- :

\u2022 Start a voice chat in your channel or group.
\u2022 Add bot and user account in chat with admin rights.
\u2022 Use /stream [youtube link] or /stream [live stream link] or /stream as a reply to an video file.

🏷️ --**Common Commands**-- :

\u2022 `/start` - Start the bot
\u2022 `/help` - Show help message

🏷️ --**Admin Only Commands**-- :

\u2022 `/stream` - Start streaming the video
\u2022 `/radio` - Start streaming the radio
\u2022 `/endstream` - Stop streaming the video
\u2022 `/restart` - Restart the bot (Owner only)

© **Powered By** : 
**@lnc3f3r | 𝙐𝙁𝙎 𝘽𝙤𝙩𝙯** 👑
"""


@ufs.on_callback_query()
async def cb_handler(client: ufs, query: CallbackQuery):
    if query.data == "help":
        buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/jinspalakkattu/TGStreamingBot"),
            ],
            [
                InlineKeyboardButton("BACK HOME", callback_data="home"),
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data == "home":
        buttons = [
            [
                InlineKeyboardButton("SEARCH INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/jinspalakkattu/TGStreamingBot"),
            ],
            [
                InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass


@ufs.on_message(filters.command(["start", f"start@{USERNAME}"]) & (filters.chat(CHAT_ID) | filters.private))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("SEARCH INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/jinspalakkattu/TGStreamingBot"),
            ],
            [
                InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(text=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)


@ufs.on_message(filters.command(["help", f"help@{USERNAME}"]) & (filters.chat(CHAT_ID) | filters.private))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/jinspalakkattu/TGStreamingBot"),
            ],
            [
                InlineKeyboardButton("BACK HOME", callback_data="home"),
                InlineKeyboardButton("CLOSE MENU", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(text=HELP_TEXT, reply_markup=reply_markup)
