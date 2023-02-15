from abc import ABC, abstractmethod
import logging
import requests


class Notifier(ABC):
    @abstractmethod
    def send_notification(self, message: str):
        pass


class TelegramNotifier(Notifier):
    """Sends a notification message to a Telegram chat using the given bot token and chat ID.

    Args:
        bot_token (str): The token of the Telegram bot that will be used to send the notification.
        chat_id (str): The ID of the chat where the notification will be sent.

    Attributes:
        bot_token (str): The token of the Telegram bot that will be used to send the notification.
        chat_id (str): The ID of the chat where the notification will be sent.

    Methods:
        send_notification(message: str) -> None: Sends a notification message to a Telegram chat using the given bot
        token and chat ID. The message is sent as a text message to the chat using the Telegram Bot API. If the
        notification is sent successfully, a log message is generated with level INFO. Otherwise, a log message is
        generated with level WARNING and the status code, reason, and text of the failed response.

    Raises:
        This class does not raise any exceptions.

    Examples:
        To send a notification using a Telegram bot with token 'my_token' to a chat with ID '12345', create a
        `TelegramNotifier` object and call its `send_notification` method:

        >>> notifier = TelegramNotifier('my_token', '12345')
        >>> notifier.send_notification('Hello from my bot!')

    """

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_notification(self, message: str):
        """Sends a notification message to a Telegram chat using the given bot token and chat ID."""
        telegram_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        telegram_params = {"chat_id": self.chat_id, "text": message}
        response = requests.post(telegram_url, json=telegram_params, timeout=30)
        if response.ok:
            logging.info("Notification sent successfully!")
        else:
            logging.warning(
                "Notification failed with status code %s: %s - %s",
                response.status_code,
                response.reason,
                response.text,
            )


class SlackNotifier(Notifier):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_notification(self, message: str):
        # code to send notification via Slack
        pass


class EmailNotifier(Notifier):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def send_notification(self, message: str):
        # code to send notification via email
        pass
