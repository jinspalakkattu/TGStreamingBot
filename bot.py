from config import Config
from pyrogram import Client


bot = Client(
    "ufsbotz",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="tgbot/ufsbotz")
)