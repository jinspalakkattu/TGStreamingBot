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
from pyrogram import Client as ufs, idle
from bot.config import Config
from bot.ufsbotz.nopm import User

Bot = ufs(
    "ufsbotz",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins={"root": "bot/ufsbotz"},
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")

Bot.start()
User.start()
print("\n[INFO] - STARTED VIDEO PLAYER BOT, JOIN !")

idle()
Bot.stop()
User.stop()
print("\n[INFO] - STOPPED VIDEO PLAYER BOT, JOIN !")
