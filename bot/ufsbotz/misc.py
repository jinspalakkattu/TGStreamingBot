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
import asyncio
from config import Config
from pyrogram import Client, filters
from pyrogram.raw import functions, types

bot = Client(
    "VideoPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
bot.start()
ok = bot.get_me()
USERNAME = ok.username

try:
    bot.send(
        functions.bots.SetBotCommands(
            commands=[
                types.BotCommand(
                    command="start",
                    description="Start The Bot"
                ),
                types.BotCommand(
                    command="help",
                    description="Show Help Message"
                ),
                types.BotCommand(
                    command="radio",
                    description="Start Radio Streaming"
                ),
                types.BotCommand(
                    command="stream",
                    description="Start Video Streaming"
                ),
                types.BotCommand(
                    command="endstream",
                    description="Stop Streaming & Left VC"
                ),
                types.BotCommand(
                    command="restart",
                    description="Restart The Bot (Owner Only)"
                )
            ]
        )
    )
except:
    pass
