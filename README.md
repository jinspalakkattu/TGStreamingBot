# Telegram Video Player Bot

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

Telegram bot to stream videos in telegram voicechat for both groups and channels. Supports live strams, YouTube videos
and telegram media.

## Config Vars:

### Mandatory Vars

1. `API_ID` : Get From [my.telegram.org](https://my.telegram.org/)
2. `API_HASH` : Get from [my.telegram.org](https://my.telegram.org)
3. `BOT_TOKEN` : [@Botfather](https://telegram.dog/BotFather)
4. `SESSION_STRING` : Generate From
   here [![GenerateStringName](https://img.shields.io/badge/repl.it-generateStringName-yellowgreen)](https://replit.com/@jinspalakkattu/TG-Session-String)
5. `CHAT` : ID of Channel/Group where the bot plays Music.

### Optional Vars

1. `LOG_GROUP` : Group to send Playlist, if CHAT is a Group()
2. `ADMINS` : ID of users who can use admin commands.
3. `STARTUP_STREAM` : This will be streamed on startups and restarts of bot. You can use either any STREAM_URL or a
   direct link of any video or a Youtube Live link. You can also use YouTube Playlist.Find a Telegram Link for your
   playlist from [PlayList Dumb](https://telegram.dog/DumpPlaylist) or get a PlayList
   from [PlayList Extract](https://telegram.dog/GetAPlaylistbot). The PlayList link should in
   form `https://t.me/DumpPlaylist/xxx`.
4. `REPLY_MESSAGE` : A reply to those who message the USER account in PM. Leave it blank if you do not need this
   feature.
5. `ADMIN_ONLY` : Pass `Y` If you want to make /play command only for admins of `CHAT`. By default /play is available
   for all.

## Requirements

- Python 3.8 or Higher.
- [FFMpeg](https://www.ffmpeg.org/).

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jinspalakkattu/TGStreamingBot/tree/py-tgcalls)

## Deploy to Railway

<p>
    <a href="https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fjinspalakkattu%2FTGStreamingBot%2Ftree%2Fpy-tgcalls&envs=API_ID%2CAPI_HASH%2CBOT_TOKEN%2CSESSION_STRING%2CCHAT_ID%2CAUTH_USERS%2CREPLY_MESSAGE&optionalEnvs=REPLY_MESSAGE&API_IDDesc=User+Account+Telegram+API_ID+get+it+from+my.telegram.org%2Fapps&API_HASHDesc=User+Account+Telegram+API_HASH+get+it+from+my.telegram.org%2Fapps&BOT_TOKENDesc=Your+Telegram+Bot+Token%2C+get+it+from+%40Botfather+XD&SESSION_STRINGDesc=Pyrogram+Session+String+of+User+Account%2C+get+it+from+%40genStr_robot&CHAT_IDDesc=ID+of+your+Channel+or+Group+where+the+bot+will+works+or+stream+videos&AUTH_USERSDesc=ID+of+Auth+Users+who+can+use+Admin+commands+%28for+multiple+users+seperated+by+space%29&REPLY_MESSAGEDesc=A+reply+message+to+those+who+message+the+USER+account+in+PM.+Make+it+blank+if+you+do+not+need+this+feature.&REPLY_MESSAGEDefault=Hello+Dear%2C+I%27m+a+bot+to+stream+videos+on+telegram+voice+chat%2C+not+having+time+to+chat+with+you+%F0%9F%98%82%21&referralCode=UFSBotz">
        <img src="https://img.shields.io/badge/Deploy%20To%20Railway-blueviolet?style=for-the-badge&logo=railway" width="200"/>
    </a>
</p>

⚠️ Warning:

Railway.app may ban your railway account if you tried to play DMCA contents. Its is hereby forewarned that we wont be
responsible for any loss caused to you. Proceed at your own risk.

## Deploy to VPS

```sh
git clone https://github.com/jinspalakkattu/TGStreamingBot
cd VCPlayerBot
pip3 install -r requirements.txt
# <Create Variables appropriately>
python3 main.py
```

## Features

- Playlist, queue.
- Supports Play from Youtube Playlist.
- Change VoiceChat title to current playing song name.
- Supports Live streaming from youtube
- Play from telegram file supported.
- Starts Radio after if no songs in playlist.
- Automatically downloads audio for the first two tracks in the playlist to ensure smooth playing
- Automatic restart even if heroku restarts.
- Support exporting and importing playlist.

### Note

[Note To A So Called Dev](https://telegram.dog/GetTGLink/802):

Kanging this codes and and editing a few lines and releasing a V.x of your repo wont make you a Developer. Fork the repo
and edit as per your needs.

## LICENSE

- [GNU General Public License](./LICENSE)

## CREDITS

- [py-tgcalls](https://github.com/pytgcalls/pytgcalls)
- [Dan](https://github.com/delivrance) for [Pyrogram](https://github.com/pyrogram/pyrogram)


