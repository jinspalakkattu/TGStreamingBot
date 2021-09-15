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
from config import Config
from script import HOME_TEXT, HELP_TEXT
from tgbot.utility import is_admin, update
from pyrogram import Client as ufs, filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaDocument

CHAT_ID = Config.CHAT_ID
USERNAME = Config.BOT_USERNAME
admin_filter = filters.create(is_admin)


@ufs.on_callback_query()
async def cb_handler(client: ufs, query: CallbackQuery):
    if query.data == "help":
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
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data == "home":
        buttons = [
            [
                InlineKeyboardButton("🔍 SEARCH INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("📣 CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
                InlineKeyboardButton("👥 SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
            ],
            [
                InlineKeyboardButton("🤖 MORE BOTS", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
                InlineKeyboardButton("🧩 SOURCE CODE", url="https://github.com/jinspalakkattu/TGStreamingBot"),
            ],
            [
                InlineKeyboardButton("🆘 HOW TO USE", callback_data="help"),
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
                InlineKeyboardButton("🔍 SEARCH INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("📣 CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
                InlineKeyboardButton("👥 SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
            ],
            [
                InlineKeyboardButton("🤖 MORE BOTS", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
                InlineKeyboardButton("🧩 SOURCE CODE", url="https://github.com/jinspalakkattu/TGStreamingBot"),
            ],
            [
                InlineKeyboardButton("🆘 HOW TO USE", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(text=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)


@ufs.on_message(filters.command(["help", f"help@{USERNAME}"]) & (filters.chat(CHAT_ID) | filters.private))
async def help(client, message):
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
    await message.reply_text(text=HELP_TEXT, reply_markup=reply_markup)


@ufs.on_message(filters.command(['repo', f"repo@{Config.BOT_USERNAME}"]))
async def repo_(client, message):
    buttons = [
        [
            InlineKeyboardButton("📣 CHANNEL", url="https://t.me/joinchat/7qlEga5lO0o2MTg0"),
            InlineKeyboardButton("👥 SUPPORT", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
        ],
        [
            InlineKeyboardButton("🤖 MORE BOTS", url="https://t.me/joinchat/6YRhp5LyjXNkNGY0"),
            InlineKeyboardButton("🧩 SOURCE CODE", url="https://github.com/jinspalakkattu/TGStreamingBot"),
        ]
    ]
    await message.reply(
        "**The Source Code Of This Bot Is Public And Can Be Found At <a "
        "href=https://github.com/jinspalakkattu/TGStreamingBot>TGStreamingBot.</a>"
        "\nYou Can Deploy Your Own Bot And Use In Your "
        "Group.\n\nFeel Free To Star☀️The Repo If You Liked It 🙃.**",
        reply_markup=InlineKeyboardMarkup(buttons))


@ufs.on_message(filters.command(
    ['restart', 'update', f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter)
async def update_handler(client, message):
    await message.reply("Updating 🔄 & Restarting The Bot 🤖.")
    await update()


@ufs.on_message(filters.command(['logs', f"logs@{Config.BOT_USERNAME}"]) & admin_filter)
async def get_logs(client, message):
    logs = []
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("ffmpeg.txt",
                                       caption="FFMPEG Logs \n\n© **Powered By** : **@lnc3f3r | 𝙐𝙁𝙎 𝘽𝙤𝙩𝙯** 👑"))
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("botlog.txt",
                                       caption="Bot Logs \n\n© **Powered By** : **@lnc3f3r | 𝙐𝙁𝙎 𝘽𝙤𝙩𝙯** 👑"))
    if logs:
        await message.reply_media_group(logs)
        logs.clear()
    else:
        await message.reply("No Log Files Found.")
