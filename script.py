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

HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**, \n\nI'm **TG Streaming Bot**. \nI Can Stream Lives, Radios, " \
            "YouTube Videos & Telegram Video Files On Voice Chat Of Telegram Channels & Groups 😉! \n\n**Made With ❤️ " \
            "By @lnc3f3r!** 👑 "

HELP_TEXT = """
**How Can I Play Video?**

You have file options.
 1. Play a video from a YouTube link.
    Command: **/play**
    <i>You can use this as a reply to a youtube link or pass link along command.</i>
 2. Play from a telegram file.
    Command: **/play**
    <i>Reply to a supported media(video and documents).</i>
 3. Play from a YouTube playlist
    Command: **/yplay**
    <i>First get a playlist file from @GetPlaylistBot or @DumpPlaylist and reply to playlist file.</i>
 4. Live Stream
    Command: **/stream**
    <i>Pass a live stream url or any direct url to play it as stream.</i>
 5. Import an old playlist.
    Command: **/import**
    <i>Reply to a previously exported playlist file. </i>

**How Can I Control Player?**
These are commands to control player.
 1. Skip a song.
    Command: **/skip**
    <i>You can pass a number greater than 2 to skip the song in that position.</i>
 2. Pause the player.
    Command: **/pause**
 3. Resume the player.
    Command: **/resume**
 4. Change Volume.
    Command: **/volume**
    <i>Pass the volume in between 1-200.</i>
 5. Leave the VC.
    Command: **/leave**
 6. Shuffle the playlist.
    Command: **/shuffle**
 7. Clear the current playlist queue.
    Command: **/clearplaylist**

**How Can I Export My Current Playlist?**
 1. Command: **/export**
    <i>To export current playlist for future use.</i>

**Other Commands**
 1. Update and restart the bot.
    Command: **/update** or **/restart**
 2. Get Logs
    Command: **/logs**

**How Can I Stream In My Group**
  <i>The source code of this bot is public and can be found at 
  <a href=https://github.com/jinspalakkattu/VCPlayerBot>VCPlayerBot.</a>

  You can deploy your own bot and use in your group.</i>

© **Powered By** : 
**@lnc3f3r | 𝙐𝙁𝙎 𝘽𝙤𝙩𝙯** 👑
"""
