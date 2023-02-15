import requests
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()


def get_chat_id():
    """
    It gets the chat ID of the Telegram chat.
    :return: The chat ID of the Telegram user who sent the message.
    """

    # Get the Telegram bot token and URL
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    # Send a GET request to the Telegram API to retrieve the chat ID
    response = requests.get(telegram_url)
    data = response.json()

    # Extract the chat ID from the response
    chat_id = data["result"][0]["message"]["chat"]["id"]

    return str(chat_id)
