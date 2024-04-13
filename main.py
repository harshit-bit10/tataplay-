import json
import subprocess
from datetime import datetime, timedelta
from pyrogram import Client, filters
from tata import download_catchup
from utils import check_user, get_tplay_data
from config import api_id, api_hash, bot_token, script_developer

print("Installing YT-DLP")
subprocess.run("pip install yt-dlp".split())

data_json = get_tplay_data()

app = Client("RC_tplay_dl_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.incoming & filters.text)
def tplay_past_catchup_dl_cmd_handler(app, message):
    if "/start" in message.text:
        app.send_photo(chat_id=message.chat.id, photo="https://te.legra.ph/file/e56ebe4d3ebe4f1936ad2.png", caption="<b>TataPlay Catchup Bot</b>\n\n`> >`<b>Made By My Big Brain</b>")
    
    auth_user = check_user(message)
    if auth_user is None:
        return
    
    if "/drm" in message.text:
        cmd = message.text.split("|")
        z = cmd[0].replace("/drm", "").strip()

        parts = message.text.split(' ')
    if len(parts) < 3:
    await message.reply("Invalid command format. Expected at least 3 parts.")
    return
        
        channel, time_range, filename = map(str.strip, parts)

        if time_range:
            start_time, end_time = map(lambda x: datetime.strptime(x, "%d/%m/%Y+%H:%M:%S"), time_range.split('-'))

            if end_time <= start_time:
                message.reply_text("<b>Invalid time range. End time should be greater than start time.</b>")
                return

            try:
                download_playback_catchup(channel, filename, data_json, app, message, start_time=start_time, end_time=end_time)
            except Exception as e:
                app.send_message(chat_id=message.chat.id, text=f"<b>An error occurred:</b> {str(e)}")
        else:
            try:
                download_playback_catchup(channel, filename, data_json, app, message)
            except Exception as e:
                app.send_message(chat_id=message.chat.id, text=f"<b>An error occurred:</b> {str(e)}")

    elif "watch.tataplay.com" in message.text:
        if "coming-soon" in message.text:
            message.reply_text(f"<b>Can't DL something which has not aired yet\nCheck URL and try again...</b>")
            return
        try:
            download_catchup(message.text, data_json, app, message)
        except Exception as e:
            app.send_message(chat_id=message.chat.id, text=f"<b>An error occurred:</b> {str(e)}")

@app.on_message(filters.incoming & filters.command(['start']) & filters.text)
def start_cmd_handler(app, message):
    message.reply_text("<b>TataPlay Catchup Bot</b>\n\n`> >`<b> Made By My Big Brain</b>")

print(script_developer , "\n")

app.run()
