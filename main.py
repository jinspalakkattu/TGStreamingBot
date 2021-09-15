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
from bot import bot
from config import Config
from logger import LOGGER
from pyrogram import idle
from tgbot.utility import start_stream
from tgbot.ufsbotz.nopm import USER, group_call

if not os.path.isdir("tgbot/downloads"):
    os.makedirs("tgbot/downloads")
else:
    for f in os.listdir("tgbot/downloads"):
        os.remove(f"tgbot/downloads/{f}")


async def main():
    await bot.start()
    Config.BOT_USERNAME = (await bot.get_me()).username
    await group_call.start()
    await start_stream()
    LOGGER.warning(f"{Config.BOT_USERNAME} Started.")
    print("\n[INFO] - STARTED VIDEO PLAYER BOT !")
    await idle()
    LOGGER.warning("Stopping")
    print("\n[INFO] - STOPPED VIDEO PLAYER BOT !")
    await group_call.start()
    await bot.stop()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
