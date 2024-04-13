from pyrogram import Client, MessageHandler
from pyrogram.types import Message
import json
from config import Config

# Replace these values with your actual API credentials
api_id = Config.API_ID
api_hash = Config.API_HASH
bot_token = Config.BOT_TOKEN

app = Client(
    "your_bot_name",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Add your logic for catching TATA Play URLs and processing them
def handle_tata_play_url(client: Client, message: Message):
    tata_play_url = message.text.strip().lower()
    if "tataplay.com" in tata_play_url:
        client.send_message(
            chat_id=message.chat.id,
            text=f"Found a TATA Play URL: {tata_play_url}"
        )

# Handle messages
@app.on_message()
def handle_messages(client: Client, message: Message):
    # Add your logic for handling messages
    handle_tata_play_url(client, message)

if __name__ == "__main__":
    app.run()
