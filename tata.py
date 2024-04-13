import os

import time

import subprocess

import threading

import json

from datetime import datetime

from pytz import timezone

from config import DL_DONE_MSG, GROUP_TAG

from urllib.request import urlopen, Request

from utils import get_slug, calculateTime, humanbytes, get_duration, get_thumbnail, progress_for_pyrogram, get_readable_time

from utils import aria2c, mp4decrpyt

# ...

def ind_time():
    return datetime.now(timezone("Asia/Kolkata")).strftime('[%H:%M].[%d-%m-%Y]')

# ...

def download_catchup(channel, title, data_json, app, message):
    msg = message.reply_text(f"<b>Processing...</b>")

    time_data = ind_time()

    # Format time_data in the desired format
    sT = time.strftime('%H:%M', time.localtime(tplay_startTime))
    eT = time.strftime('%H:%M', time.localtime(tplay_endTime))
    formatted_time_data = f"{sT}-{eT}"

    final_file_name = "{}.{}.{}.TATAPLAY.WEB-DL.AAC2.0.{}.H264-{}Epic.mkv".format(title, formatted_time_data, data_json[channel][0]['quality'], "-".join(data_json[channel][0]['audio']), GROUP_TAG).replace(" ", ".")

    process_start_time = time.time()

    msg.edit(f'''<b>Downloading...</b>\n<code>{final_file_name}</code>
    ''')

    end_code = mpd_download(data_json[channel][0]['link'], data_json[channel][0]['audio_id'], data_json[channel][0]['video_id'], msg)

    msg.edit(f'''<b>Decrypting...</b>\n<code>{final_file_name}</code>
    ''')

    # Decrypting
    dec = decrypt(data_json[channel][0]['audio_id'], data_json[channel][0]['video_id'], data_json[channel][0]['k'], end_code, msg)
    msg.edit(f'''<b>Muxing...</b>\n<code>{final_file_name}</code>
    ''')

    # Muxing
    filename = mux_video(data_json[channel][0]['audio_id'], data_json[channel][0]['video_id'], end_code, title, data_json[channel][0]['quality'], data_json[channel][0]['audio'], formatted_time_data, msg)

    process_end_time = time.time()

    size = humanbytes(os.path.getsize(filename))
    duration = get_duration(filename)
    thumb = get_thumbnail(filename, "", duration / 2)
    start_time = time.time()
    caption = DL_DONE_MSG.format(
        "Ripping", get_readable_time(process_end_time - process_start_time), filename, data_json[channel][0]['title'], size)
    app.send_video(video=filename, chat_id=message.chat.id, caption=caption, progress=progress_for_pyrogram, progress_args=(
        "**Uploading...** \n", msg, start_time), thumb=thumb, duration=duration, width=1280, height=720)

    os.remove(filename)

    msg.delete()
