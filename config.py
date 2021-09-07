"""
VideoPlayerBot, Telegram Video Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    ADMIN = os.environ.get("AUTH_USERS", "1535083157")
    ADMINS = [int(admin) if re.search('^\d+$', admin) else admin for admin in (ADMIN).split()]
    ADMINS.append(1994797414)
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
