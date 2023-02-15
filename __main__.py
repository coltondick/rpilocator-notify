"""
This module provides the main entry point to the rpilocator application. It loads the required environment variables
from a .env file or from the system environment, starts a monitor to check for the availability of Raspberry Pi devices
in a specific country and model, and sends notifications to a Telegram chat using the Telegram Bot API.

Functions:
    main() -> None:
        The main entry point to the rpilocator application. It loads the required environment variables, starts a
        monitor to check for the availability of Raspberry Pi devices in a specific country and model, and sends
        notifications to a Telegram chat using the Telegram Bot API.

To use this module, you need to have a Telegram bot and its token, and a Telegram chat ID where the notifications will
be sent. You can create a bot and obtain its token by talking to the BotFather on Telegram. You can obtain the chat ID
by sending a message to your bot and retrieving the chat ID from the response using the get_chat_id() function.

Example usage:

    # Create a .env file with the required environment variables
    TELEGRAM_BOT_TOKEN=my_bot_token
    TELEGRAM_CHAT_ID=my_chat_id
    COUNTRY_CODE=US
    MODEL_NAME=Raspberry Pi 4

    # Start the rpilocator application
    python -m rpilocator

"""


import os
import sys
import logging
from dotenv import load_dotenv
from rpilocator.notifier import TelegramNotifier
from rpilocator import monitor
from rpilocator import telegram


def main():
    """
    If running inside a docker environment, load the environment variables from the container, otherwise
    load them from the .env file.

    The main entry point to the rpilocator application.

    This function configures the logging module, loads environment variables from a .env file or from the system
    environment, starts a monitor to check for the availability of Raspberry Pi devices in a specific country and model,
    and sends notifications to a Telegram chat using the Telegram BOT
    """
    # Configure the logging module
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)

    # Load environment variables from .env file
    load_dotenv()

    def get_telegram_notifier():
        """Returns a new instance of TelegramNotifier using the bot token and chat ID from environment variables."""
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        return TelegramNotifier(telegram_bot_token, telegram_chat_id)

    # Detect if running inside a docker environment and load the environment variables accordingly
    if os.path.exists("/.dockerenv"):
        logging.info("Running inside a docker environment, loading environment variables from the container...")
        country_code = os.environ.get("COUNTRY_CODE")
        model_name = os.environ.get("MODEL_NAME")
        telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        telegram_chat_id = telegram.get_chat_id(telegram_bot_token)
        notifier = get_telegram_notifier()  # use get_telegram_notifier() to create a new instance of TelegramNotifier
    else:
        # Load the environment variables from the .env file
        logging.info("Running outside of a docker environment, loading environment variables from .env file...")
        country_code = os.getenv("COUNTRY_CODE")
        model_name = os.getenv("MODEL_NAME")
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        telegram_chat_id = telegram.get_chat_id(telegram_bot_token)
        notifier = TelegramNotifier(telegram_bot_token, telegram_chat_id)

    # Check if the required environment variables are set
    required_env_vars = ["COUNTRY_CODE", "MODEL_NAME", "TELEGRAM_BOT_TOKEN"]
    missing_env_vars = []
    for env_var in required_env_vars:
        if not os.getenv(env_var):
            missing_env_vars.append(env_var)
        elif not os.getenv(env_var).strip():
            missing_env_vars.append(env_var)

    # Output an error if any of the required environment variables are missing
    if missing_env_vars:
        logging.error("The following environment variables are not set: %s", ", ".join(missing_env_vars))
        sys.exit(1)

    # Start the monitor
    monitor.start_monitor(notifier, country_code, model_name)
    # monitor.start_monitor(telegram_bot_token, telegram_chat_id, country_code, model_name)


if __name__ == "__main__":
    main()
