from dependencies import *


def get_chat_id(telegram_bot_token):
    """
    It gets the chat ID of the Telegram chat.
    :return: The chat ID of the Telegram user who sent the message.
    """

    # Get the Telegram URL
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/getUpdates"

    # Send a GET request to the Telegram API to retrieve the chat ID
    response = requests.get(telegram_url)
    data = response.json()

    # Extract the chat ID from the response
    telegram_chat_id = data["result"][0]["message"]["chat"]["id"]

    return str(telegram_chat_id)


def send_notification(telegram_bot_token, telegram_chat_id, message):
    """Sends a notification message to a Telegram chat using the given bot token and chat ID."""
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    telegram_params = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(telegram_url, json=telegram_params)
    if response.ok:
        logging.info("Notification sent successfully!")
    else:
        logging.warning(
            f"Notification failed with status code {response.status_code}: {response.reason} - {response.text}"
        )
