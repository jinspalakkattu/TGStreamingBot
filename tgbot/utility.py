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
import sys
import time
import json
import math
import random
import ffmpeg
import asyncio
import subprocess
from bot import bot
from config import Config
from logger import LOGGER
from signal import SIGINT
from threading import Thread
from datetime import datetime
from youtube_dl import YoutubeDL
from pytgcalls.types import Update
from ufsbotz.nopm import group_call, USER
from pytgcalls import PyTgCalls, StreamType
from pyrogram.raw.types import InputChannel
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.errors.exceptions.bad_request_400 import BadRequest
from pytgcalls.exceptions import GroupCallNotFound, NoActiveGroupCall
from pyrogram.raw.functions.phone import EditGroupCallTitle, CreateGroupCall
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls.types.input_stream import InputAudioStream, InputVideoStream, AudioParameters, VideoParameters


async def get_admins(chat):
    admins = Config.ADMINS
    if not Config.ADMIN_CACHE:
        admins = Config.ADMINS + [631110062]
        try:
            grpadmins = await bot.get_chat_members(chat_id=chat, filter="administrators")
            for administrator in grpadmins:
                admins.append(administrator.user.id)
        except Exception as e:
            LOGGER.error(f"Errors occured while getting admin list - {e}")
            pass
        Config.ADMINS = admins
        Config.ADMIN_CACHE = True
    return admins


async def start_stream():
    if Config.YPLAY:
        await y_play(Config.STREAM_URL)
        return
    if Config.YSTREAM:
        link = await get_link(Config.STREAM_URL)
    else:
        link = Config.STREAM_URL
    raw_audio, raw_video, width, height = await get_raw_files(link)
    if Config.playlist:
        Config.playlist.clear()
    await join_call(raw_audio, raw_video, width, height)


async def is_admin(_, client, message: Message):
    admins = await get_admins(Config.CHAT_ID)
    if message.from_user is None and message.sender_chat:
        return True
    if message.from_user.id in admins:
        return True
    else:
        return False


async def y_play(playlist):
    try:
        getplaylist = await bot.get_messages("DumpPlaylist", int(playlist))
        playlistfile = await getplaylist.download()
        LOGGER.warning("Trying to get details from playlist.")
        n = await import_play_list(playlistfile)
        if not n:
            LOGGER.error("Errors Occured While Importing Playlist")
            Config.STREAM_URL = "https://www.youtube.com/watch?v=zcrUCvBD16k"
            Config.YSTREAM = True
            Config.YPLAY = False
            LOGGER.warning("Starting Default Live, 24 News")
            await start_stream()
            return False
        if Config.SHUFFLE:
            await shuffle_playlist()
    except Exception as e:
        LOGGER.error("Errors Occured While Importing Playlist", e)
        Config.STREAM_URL = "https://www.youtube.com/watch?v=zcrUCvBD16k"
        Config.YSTREAM = True
        Config.YPLAY = False
        LOGGER.warning("Starting Default Live, 24 News")
        await start_stream()
        return False


async def get_link(file):
    def_ydl_opts = {'quiet': True, 'prefer_insecure': False, "geo-bypass": True}
    with YoutubeDL(def_ydl_opts) as ydl:
        try:
            ydl_info = ydl.extract_info(file, download=False)
        except Exception as e:
            LOGGER.error(f"Errors Occurred While Getting Link From Youtube Video {e}")
            await skip()
            return False
        url = None
        for each in ydl_info['formats']:
            if each['width'] == 640 \
                    and each['acodec'] != 'none' \
                    and each['vcodec'] != 'none':
                url = each['url']
                break  # prefer 640x360
            elif each['width'] \
                    and each['width'] <= 1280 \
                    and each['acodec'] != 'none' \
                    and each['vcodec'] != 'none':
                url = each['url']
                continue  # any other format less than 1280
            else:
                continue
        if url:
            return url
        else:
            LOGGER.error(f"Errors Occurred While Getting Link From Youtube Video - No Video Formats Found")
            await skip()
            return False


async def get_raw_files(link):
    process = Config.FFMPEG_PROCESSES.get(Config.CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.terminate()
        except Exception as e:
            LOGGER.error(f"Error while terminating ffmpeg {e}")
            pass
        del Config.FFMPEG_PROCESSES[Config.CHAT_ID]
    Config.GET_FILE["old"] = os.listdir("tgbot/downloads")
    new = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
    raw_audio = f"./downloads/{new}_audio.raw"
    raw_video = f"./downloads/{new}_video.raw"
    # if not os.path.exists(raw_audio):
    # os.mkfifo(raw_audio)
    # if not os.path.exists(raw_video):
    # os.mkfifo(raw_video)
    width, height = await get_height_and_width(link)
    if not width or \
            not height:
        Config.STREAM_LINK = False
        await skip()
    command = ["ffmpeg", "-y", "-i", link, "-f", "s16le", "-ac", "1", "-ar", "48000", raw_audio, "-f", "rawvideo", '-r',
               '30', '-pix_fmt', 'yuv420p', '-vf', f'scale={width}:{height}', raw_video]
    ffmpeg_log = open("ffmpeg.txt", "w+")
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=ffmpeg_log,
        stderr=asyncio.subprocess.STDOUT,
    )
    while not os.path.exists(raw_audio) or \
            not os.path.exists(raw_video):
        await asyncio.sleep(1)
    Config.FFMPEG_PROCESSES[Config.CHAT_ID] = process
    return raw_audio, raw_video, width, height


async def join_call(audio, video, width, height):
    while not os.path.exists(audio) or \
            not os.path.exists(video):
        await skip()
    if Config.CALL_STATUS:
        play = await change_file(audio, video, width, height)
    else:
        play = await join_and_play(audio, video, width, height)
    if play == False:
        await asyncio.sleep(1)
        await join_call(audio, video, width, height)
    await asyncio.sleep(1)
    try:
        call = group_call.get_call(Config.CHAT_ID)
    except GroupCallNotFound:
        return await restart()
    except Exception as e:
        LOGGER.warning(e)
        return await restart()
    if str(call.status) != "playing":
        await restart()
    else:
        old = Config.GET_FILE.get("old")
        if old:
            for file in old:
                os.remove(f"tgbot/downloads/{file}")
            try:
                del Config.GET_FILE["old"]
            except:
                LOGGER.error("Error in deletion")
                pass
        await send_playlist()


async def change_file(audio, video, width, height):
    try:
        await group_call.change_stream(
            int(Config.CHAT_ID),
            InputAudioStream(
                audio,
                AudioParameters(
                    bitrate=48000,
                ),
            ),
            InputVideoStream(
                video,
                VideoParameters(
                    width=width,
                    height=height,
                    frame_rate=30,
                ),
            ),
        )
    except Exception as e:
        LOGGER.error(f"Errors Occured While Joining, Retrying Error- {e}")
        return False
    if Config.EDIT_TITLE:
        await edit_title()


async def join_and_play(audio, video, width, height):
    try:
        await group_call.join_group_call(
            int(Config.CHAT_ID),
            InputAudioStream(
                audio,
                AudioParameters(
                    bitrate=48000,
                ),
            ),
            InputVideoStream(
                video,
                VideoParameters(
                    width=width,
                    height=height,
                    frame_rate=30,
                ),

            ),
            stream_type=StreamType().local_stream
        )
        Config.CALL_STATUS = True
    except NoActiveGroupCall:
        try:
            LOGGER.warning("No Active Calls Found, Creating New")
            await USER.send(CreateGroupCall(
                peer=(await USER.resolve_peer(Config.CHAT_ID)),
                random_id=random.randint(10000, 999999999)
            )
            )
            await asyncio.sleep(2)
            await restart_playout()
        except Exception as e:
            LOGGER.error(f"Unable To Start New GroupCall :- {e}")
            pass
    except Exception as e:
        LOGGER.error(f"Errors Occurred While Joining, Retrying Error- {e}")
        return False


async def leave_call():
    process = Config.FFMPEG_PROCESSES.get(Config.CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            LOGGER.error(e)
            pass
        del Config.FFMPEG_PROCESSES[Config.CHAT_ID]
    try:
        await group_call.leave_group_call(Config.CHAT_ID)
    except Exception as e:
        LOGGER.error(f"Errors While Leaving Call {e}")
    Config.playlist.clear()
    if Config.STREAM_LINK:
        Config.STREAM_LINK = False
    Config.CALL_STATUS = False


async def pause():
    try:
        await group_call.pause_stream(Config.CHAT_ID)
        return True
    except GroupCallNotFound:
        await restart_playout()
        return False
    except Exception as e:
        LOGGER.error(f"Errors Occurred While Pausing -{e}")
        return False


async def resume():
    try:
        await group_call.resume_stream(Config.CHAT_ID)
        return True
    except GroupCallNotFound:
        await restart_playout()
        return False
    except Exception as e:
        LOGGER.error(f"Errors Occurred While Resuming -{e}")
        return False


async def volume(volume):
    try:
        await group_call.change_volume_call(Config.CHAT_ID, volume)
    except BadRequest:
        await restart_playout()
    except Exception as e:
        LOGGER.error(f"Errors Occurred While Changing Volume Error -{e}")


async def restart():
    process = Config.FFMPEG_PROCESSES.get(Config.CHAT_ID)
    if process:
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            LOGGER.error(e)
            pass
        del Config.FFMPEG_PROCESSES[Config.CHAT_ID]
    try:
        await group_call.leave_group_call(Config.CHAT_ID)
        await asyncio.sleep(2)
    except Exception as e:
        LOGGER.error(e)
    if not Config.playlist:
        await start_stream()
        return
    LOGGER.warning(f"- START PLAYING: {Config.playlist[0][1]}")
    await asyncio.sleep(2)
    await play()
    LOGGER.warning("Restarting Playout")
    if len(Config.playlist) <= 1:
        return
    await download(Config.playlist[1])


async def play():
    song = Config.playlist[0]
    if song[3] == "telegram":
        file = Config.GET_FILE.get(song[5])
        if not file:
            await asyncio.sleep(1)
        while not os.path.exists(file):
            await asyncio.sleep(1)
    else:
        file = await get_link(song[2])
    if not file:
        await skip()
        return False
    audio_file, video_file, width, height = await get_raw_files(file)
    await asyncio.sleep(1)
    if Config.STREAM_LINK:
        Config.STREAM_LINK = False
    await join_call(audio_file, video_file, width, height)


async def download(song, msg=None):
    if song[3] == "telegram":
        if not Config.GET_FILE.get(song[5]):
            try:
                original_file = await bot.download_media(song[2], progress=progress_bar,
                                                         progress_args=(int((song[5].split("_"))[1]), time.time(), msg))
                Config.GET_FILE[song[5]] = original_file
            except Exception as e:
                LOGGER.error(e)
                Config.playlist.remove(song)
                if len(Config.playlist) <= 1:
                    return
                await download(Config.playlist[1])


async def restart_playout():
    if not Config.playlist:
        await start_stream()
        return
    LOGGER.warning(f"RESTART PLAYING: {Config.playlist[0][1]}")
    await play()
    if len(Config.playlist) <= 1:
        return
    await download(Config.playlist[1])


async def import_play_list(file):
    file = open(file)
    try:
        f = json.loads(file.read(), object_hook=lambda d: {int(k): v for k, v in d.items()})
        for playf in f:
            Config.playlist.append(playf)
            if len(Config.playlist) == 1:
                LOGGER.warning("Downloading & Processing...")
                await download(Config.playlist[0])
                await play()
        if not Config.playlist:
            file.close()
            try:
                os.remove(file)
            except:
                pass
            return False
        file.close()
        for track in Config.playlist[:2]:
            await download(track)
        try:
            os.remove(file)
        except:
            pass
        return True
    except Exception as e:
        LOGGER.error(f"Errors While Importing Playlist {e}")
        return False


async def shuffle_playlist():
    v = []
    p = [v.append(Config.playlist[c]) for c in range(2, len(Config.playlist))]
    random.shuffle(v)
    for c in range(2, len(Config.playlist)):
        Config.playlist.remove(Config.playlist[c])
        Config.playlist.insert(c, v[c - 2])


async def skip():
    if Config.STREAM_LINK and len(Config.playlist) == 0:
        await stream_from_link()
        return
    elif not Config.playlist:
        await start_stream()
        return
    old_track = Config.playlist.pop(0)
    if old_track[3] == "telegram":
        file = Config.GET_FILE.get(old_track[5])
        try:
            os.remove(file)
        except:
            pass
        del Config.GET_FILE[old_track[5]]
    if not Config.playlist:
        await start_stream()
        return
    LOGGER.warning(f"START PLAYING: {Config.playlist[0][1]}")
    await play()
    if len(Config.playlist) <= 1:
        return
    await download(Config.playlist[1])


async def edit_title():
    if not Config.playlist:
        title = "ⓂᑌᔑᏆᑕ 🎸🎬 2️⃣4️⃣x7️⃣"
    else:
        title = Config.playlist[0][1]

    try:
        chat = await USER.resolve_peer(Config.CHAT_ID)
        full_chat = await USER.send(
            GetFullChannel(
                channel=InputChannel(
                    channel_id=chat.channel_id,
                    access_hash=chat.access_hash,
                ),
            ),
        )
        edit = EditGroupCallTitle(call=full_chat.full_chat.call, title=title)
        await USER.send(edit)
    except Exception as e:
        LOGGER.error(f"Errors Occurred While Editing Title - {e}")
        pass


async def send_playlist():
    if Config.LOG_GROUP:
        pl = await get_playlist_str()
        if Config.msg.get('playlist') is not None:
            await Config.msg['playlist'].delete()
        Config.msg['playlist'] = await send_text(pl)


async def get_playlist_str():
    if not Config.playlist:
        pl = f"🔈 Playlist Is Empty. Streaming [STARTUP_STREAM]({Config.STREAM_URL})"
    else:
        if len(Config.playlist) >= 25:
            tplaylist = Config.playlist[:25]
            pl = f"Listing First 25 Songs Of Total {len(Config.playlist)} Songs.\n"
            pl += f"▶️ **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(tplaylist)
            ])
            tplaylist.clear()
        else:
            pl = f"▶️ **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}\n"
                for i, x in enumerate(Config.playlist)
            ])
    return pl


async def send_text(text):
    message = await bot.send_message(
        Config.LOG_GROUP,
        text,
        reply_markup=await get_buttons(),
        disable_web_page_preview=True,
        disable_notification=True
    )
    return message


async def get_buttons():
    if not Config.playlist:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"⏯ {get_pause(Config.PAUSE)}", callback_data=f"{get_pause(Config.PAUSE)}"),
                ],
            ]
        )
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔄 Shuffle", callback_data="shuffle"),
                    InlineKeyboardButton(f"⏯ {get_pause(Config.PAUSE)}", callback_data=f"{get_pause(Config.PAUSE)}"),
                    InlineKeyboardButton("⏩ Skip", callback_data="skip"),
                    InlineKeyboardButton("⏮ Replay", callback_data="replay")
                ],
            ]
        )
    return reply_markup


def get_pause(status):
    if status:
        return "Resume"
    else:
        return "Pause"


async def get_height_and_width(file):
    try:
        k = ffmpeg.probe(file)['streams']
        width = None
        height = None
        for f in k:
            try:
                width = int(f["width"])
                height = int(f["height"])
                if height >= 256:
                    break
            except KeyError:
                continue
        # trial and error.(i guess all will work fine.)
        # if not (width, height) in [(1280,720), (640,360), (864,480), (426,240), (640,640)]:
        # width, height = 640, 360
    except:
        LOGGER.error("Error, This Stream Is Not Supported.")
        width, height = False, False
    return width, height


async def progress_bar(current, zero, total, start, msg):
    now = time.time()
    if total == 0:
        return
    if round((now - start) % 3) == 0 or current == total:
        speed = current / (now - start)
        percentage = current * 100 / total
        time_to_complete = round(((total - current) / speed)) * 1000
        time_to_complete = TimeFormatter(time_to_complete)
        progressbar = "[{0}{1}]".format( \
            ''.join(["◉" for i in range(math.floor(percentage / 10))]),
            ''.join(["◎" for i in range(10 - math.floor(percentage / 10))])
        )
        current_message = f"**Downloading** {round(percentage, 2)}% \n{progressbar}\n⚡️ " \
                          f"**Speed**: {humanbytes(speed)}/s\n⬇️ " \
                          f"**Downloaded**: {humanbytes(current)} / {humanbytes(total)}\n🕰 " \
                          f"**Time Left**: {time_to_complete} "
        if msg:
            try:
                await msg.edit(text=current_message)
            except:
                pass
        LOGGER.warning(current_message)


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
          ((str(hours) + " Hours, ") if hours else "") + \
          ((str(minutes) + " Min, ") if minutes else "") + \
          ((str(seconds) + " Sec, ") if seconds else "") + \
          ((str(milliseconds) + " Millisec, ") if milliseconds else "")
    return tmp[:-2]


async def stream_from_link(link):
    raw_audio, raw_video, width, height = await get_raw_files(link)
    if Config.playlist:
        Config.playlist.clear()
    Config.STREAM_LINK = link
    await join_call(raw_audio, raw_video, width, height)


async def update():
    await leave_call()
    Thread(
        target=stop_and_restart()
    ).start()


def stop_and_restart():
    os.system("git pull")
    time.sleep(10)
    os.execl(sys.executable, sys.executable, *sys.argv)


@group_call.on_raw_update()
async def handler(client: PyTgCalls, update: Update):
    if str(update) == "JOINED_VOICE_CHAT":
        Config.CALL_STATUS = True
        if Config.EDIT_TITLE:
            await edit_title()
    elif str(update) == "LEFT_VOICE_CHAT":
        Config.CALL_STATUS = False
    elif str(update) == "PAUSED_STREAM":
        Config.PAUSE = True
    elif str(update) == "RESUMED_STREAM":
        Config.PAUSE = False


@group_call.on_stream_end()
async def handler(client: PyTgCalls, update: Update):
    if str(update) == "STREAM_AUDIO_ENDED" or str(update) == "STREAM_VIDEO_ENDED":
        if not Config.STREAM_END.get("STATUS"):
            Config.STREAM_END["STATUS"] = str(update)
            if Config.STREAM_LINK and len(Config.playlist) == 0:
                await stream_from_link(Config.STREAM_LINK)
            elif not Config.playlist:
                await start_stream()
            else:
                await skip()
            await asyncio.sleep(15)  # wait for max 15 sec
            try:
                del Config.STREAM_END["STATUS"]
            except:
                pass
        else:
            try:
                del Config.STREAM_END["STATUS"]
            except:
                pass
