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
from dotenv import load_dotenv

load_dotenv()


class Config:
    ADMIN = os.environ.get("AUTH_USERS", "1535083157")
    ADMINS = [int(admin) if re.search('^\d+$', admin) else admin for admin in (ADMIN).split()]
    ADMINS.append(631110062)
    API_ID = int(os.environ.get("API_ID", "5639554"))
    CHAT_ID = int(os.environ.get("CHAT_ID", "-1001492474364"))
    API_HASH = os.environ.get("API_HASH", "786942f68ec94b810ef0388e3418e936")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "1931994342:AAGl7vcEuFNi-qosXykNOL70G-YOW24AYis")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "@UFSVCPlayer_Bot")
    REPLY_MESSAGE = os.environ.get("REPLY_MESSAGE", "You Cant Message Me")
    if REPLY_MESSAGE:
        REPLY_MESSAGE = REPLY_MESSAGE
    else:
        REPLY_MESSAGE = None
    SESSION_STRING = os.environ.get("SESSION_STRING", "BAAguwl4rmXCEaXhVHt0MKUiJQfihbd7elh4KhVY-JQdcEeQ0BmyRwnDbpio3DsFGxh9kjrnd1qsR1I-0UWLhHMq2xq7J_BmFai_rKBfvZBhiewj9COEz021RNKmFDP4QZebyA2yShEAlFQ2LbAXb4PnEyeVatWO2FszOxi8PmpZwyaZEPcPezxHP6e5PF3pvUnhfNVqvHy1zToDAPbRRKQaiRt8dN4DoEfkf0WzJLXeW2m3PPJy3MARiS4wF4AvgGzFb64YDu81Gm01VEJm_Q8Mjs1ED4l17m4VkkgeSOsfygal1-N-cx065hot4HremowjDwGOR0V4Cb8YYAhCZStBW3-ClQA")
