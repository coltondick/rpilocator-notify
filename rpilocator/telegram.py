"""
This module provides functions to send notifications to a Telegram chat using the Telegram Bot API.

Functions:
    get_chat_id(telegram_bot_token: str) -> str:
        Gets the chat ID of the Telegram chat.
    send_notification(telegram_bot_token: str, telegram_chat_id: str, message: str) -> None:
        Sends a notification message to a Telegram chat using the given bot token and chat ID.

To use this module, you need to have a Telegram bot and its token. You can create a bot and obtain its token by
talking to the BotFather on Telegram.

Example usage:

    from telegram_notifier import get_chat_id, send_notification

    # Obtain the chat ID of the user who sent the last message to the bot
    chat_id = get_chat_id('my_bot_token')

    # Send a notification message to the user
    send_notification('my_bot_token', chat_id, 'Hello from my bot!')

"""


import logging
import requests


def get_chat_id(telegram_bot_token):
    """
    It gets the chat ID of the Telegram chat.
    :return: The chat ID of the Telegram user who sent the message.
    """

    # Get the Telegram URL
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/getUpdates"

    # Send a GET request to the Telegram API to retrieve the chat ID
    response = requests.get(telegram_url, timeout=30)
    data = response.json()

    # Extract the chat ID from the response
    telegram_chat_id = data["result"][0]["message"]["chat"]["id"]

    return str(telegram_chat_id)


def send_notification(telegram_bot_token, telegram_chat_id, message):
    """Sends a notification message to a Telegram chat using the given bot token and chat ID."""
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    telegram_params = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(telegram_url, json=telegram_params, timeout=30)
    if response.ok:
        logging.info("Notification sent successfully!")
    else:
        logging.warning(
            "Notification failed with status code %s: %s - %s", response.status_code, response.reason, response.text
        )
