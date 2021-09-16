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
from logger import LOGGER
from pyrogram import Client as ufs, filters
from pyrogram.errors import BotInlineDisabled

ADMINS = Config.ADMINS
USERNAME = Config.BOT_USERNAME
REPLY_MESSAGE = Config.REPLY_MESSAGE


async def is_reply(_, client, message):
    if Config.REPLY_MESSAGE:
        return True
    else:
        return False


reply_filter = filters.create(is_reply)


@ufs.on_message(filters.private & filters.incoming & ~filters.bot & ~filters.service & ~filters.me & ~filters.edited)
async def nopm(client, message):
    if REPLY_MESSAGE is not None:
        try:
            inline = await client.get_inline_bot_results(USERNAME, "UFSBotz")
            m = await client.send_inline_bot_result(
                message.chat.id,
                query_id=inline.query_id,
                result_id=inline.results[0].id,
                hide_via=True
            )
            old = Config.msg.get(message.chat.id)
            if old:
                await client.delete_messages(message.chat.id, [old["msg"], old["s"]])
            Config.msg[message.chat.id] = {"msg": m.updates[1].message.id, "s": message.message_id}
        except BotInlineDisabled:
            LOGGER.error(
                f"Error: Inline Mode For @{USERNAME} Is Not Enabled. Enable From @Botfather To Enable PM Permit.")
            for admin in ADMINS:
                try:
                    await client.send_message(chat_id=admin,
                                              text=f"Hey 🙋‍♂️,\nInline Mode Isn't Enabled For @{USERNAME} Yet. "
                                                   f"A Nibba Is Spamming Me In PM, Enable Inline Mode For @{USERNAME} "
                                                   f"From @Botfather To Reply Him 😉!")
                except Exception as e:
                    print(e)
                    pass
        except Exception as e:
            print(e)
            pass
