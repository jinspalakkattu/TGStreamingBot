# Telegram Video Player Bot (Beta)
![GitHub Repo stars](https://img.shields.io/github/stars/jinspalakkattu/TGStreamingBot?color=blue&style=flat)
![GitHub forks](https://img.shields.io/github/forks/jinspalakkattu/TGStreamingBot?color=green&style=flat)
![GitHub issues](https://img.shields.io/github/issues/jinspalakkattu/TGStreamingBot)
![GitHub closed issues](https://img.shields.io/github/issues-closed/jinspalakkattu/TGStreamingBot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jinspalakkattu/TGStreamingBot)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/jinspalakkattu/TGStreamingBot)
![GitHub contributors](https://img.shields.io/github/contributors/jinspalakkattu/TGStreamingBot?style=flat)
![GitHub repo size](https://img.shields.io/github/repo-size/jinspalakkattu/TGStreamingBot?color=red)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jinspalakkattu/TGStreamingBot)
![GitHub](https://img.shields.io/github/license/jinspalakkattu/TGStreamingBot)
[![Bot Updates](https://img.shields.io/badge/TGStreamingBot-Updates%20Channel-green)](https://t.me/joinchat/7qlEga5lO0o2MTg0)
[![Bot Support](https://img.shields.io/badge/TGStreamingBot-Support%20Group-blue)](https://t.me/joinchat/6YRhp5LyjXNkNGY0)

An Telegram Bot By [ᏞuᏟᎥfᎬᏒ](https://t.me/lnc3f3r) To Stream Videos in Telegram Voice Chat.

## Main Features

- Supports Live Streaming
- Supports YouTube Streaming
- Supports Live Radio Streaming
- Supports Video Files Streaming
- Supports YouTube Live Streaming
- Customizable Userbot Protection (PM Guard)

## Deploy Own Bot

### Railway (Reommanded)
<p><a href="https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fjinspalakkattu%2FTGStreamingBot&envs=API_ID%2CAPI_HASH%2CBOT_TOKEN%2CSESSION_STRING%2CCHAT_ID%2CAUTH_USERS%2CBOT_USERNAME%2CREPLY_MESSAGE&optionalEnvs=REPLY_MESSAGE&API_IDDesc=User+Account+Telegram+API_ID+get+it+from+my.telegram.org%2Fapps&API_HASHDesc=User+Account+Telegram+API_HASH+get+it+from+my.telegram.org%2Fapps&BOT_TOKENDesc=Your+Telegram+Bot+Token%2C+get+it+from+%40Botfather+XD&SESSION_STRINGDesc=Pyrogram+Session+String+of+User+Account%2C+get+it+from+%40genStr_robot&CHAT_IDDesc=ID+of+your+Channel+or+Group+where+the+bot+will+works+or+stream+videos&AUTH_USERSDesc=ID+of+Auth+Users+who+can+use+Admin+commands+%28for+multiple+users+seperated+by+space%29&BOT_USERNAMEDesc=Your+Telegram+Bot+Username+without+%40%2C+get+it+from+%40Botfather+XD&REPLY_MESSAGEDesc=A+reply+message+to+those+who+message+the+USER+account+in+PM.+Make+it+blank+if+you+do+not+need+this+feature.&REPLY_MESSAGEDefault=Hello+Sir%2C+I%27m+a+bot+to+stream+videos+on+telegram+voice+chat%2C+not+having+time+to+chat+with+you+%F0%9F%98%82%21&referralCode=SAFONE"><img src="https://img.shields.io/badge/Deploy%20To%20Railway-blueviolet?style=for-the-badge&logo=railway" width="200"/></a></p>

### Heroku (Don't Complain)
<p><a href="https://heroku.com/deploy?template=https://github.com/jinspalakkattu/TGStreamingBot"><img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200"/></a></p>

## Commands (Botfather)
```sh
start - Start The Bot
help - Show Help Message
radio - Start Radio Streaming
stream - Start Video Streaming
endstream - Stop Streaming & Left VC
```

## Config Vars
1. `API_ID` : User Account Telegram API_ID, get it from my.telegram.org
2. `API_HASH` : User Account Telegram API_HASH, get it from my.telegram.org
3. `BOT_TOKEN` : Your Telegram Bot Token, get it from @Botfather XD
4. `BOT_USERNAME` : Your Telegram Bot Username, get it from @Botfather XD
4. `SESSION_STRING` : Pyrogram Session String of User Account, get it from [TG String Session](https://replit.com/@ErichDaniken/Generate-Telegram-String-Session/)
5. `CHAT_ID` : ID of Channel/Group where the bot will works or stream videos.
6. `AUTH_USERS` : ID of Users who can use Admins commands (for multiple users seperated by space).
7. `REPLY_MESSAGE` : A reply to those who message the USER account in PM. Leave it blank if you do not need this feature.

## Requirements
- Python 3.6 or Higher.
- [Telegram API key](https://docs.pyrogram.org/intro/quickstart#enjoy-the-api).
- Latest [FFmpeg Python](https://www.ffmpeg.org/).
- Pyrogram [String Session](https://replit.com/@ErichDaniken/Generate-Telegram-String-Session/) of the account.
- The User Account Needs To Be An Admin In The Group / Channel. 

## Self Host
```sh
$ git clone https://github.com/jinspalakkattu/TGStreamingBot.git
$ cd VideoPlayerBot
$ sudo apt-get install python3-pip ffmpeg
$ pip3 install -U pip
$ pip3 install -U -r requirements.txt
# <create .env variables appropriately>
$ python3 -m bot.py
```


## License
```sh
TGStreamingBot, Telegram Video Chat Bot
Copyright (c) 2021  [Jins Mathew](https://github.com/jinspalakkattu)

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
```

## Credits

- [Me](https://github.com/jinspalakkattu) for [Noting](https://github.com/jinspalakkattu/TGStreamingBot) 😬
- [Dan](https://github.com/delivrance) for [Pyrogram](https://github.com/pyrogram/pyrogram) ❤️
- [MarshalX](https://github.com/MarshalX) for [pytgcalls](https://github.com/MarshalX/tgcalls) ❤️
- And Thanks To All [Contributors](https://github.com/AsmSafone/VideoPlayerBot/graphs/contributors)! ❤️