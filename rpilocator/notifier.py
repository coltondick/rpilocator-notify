from abc import ABC, abstractmethod
from dependencies import *


class Notifier(ABC):
    @abstractmethod
    def send_notification(self, message: str):
        pass


class TelegramNotifier(Notifier):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_notification(self, message: str):
        """Sends a notification message to a Telegram chat using the given bot token and chat ID."""
        telegram_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        telegram_params = {"chat_id": self.chat_id, "text": message}
        response = requests.post(telegram_url, json=telegram_params)
        if response.ok:
            logging.info("Notification sent successfully!")
        else:
            logging.warning(
                f"Notification failed with status code {response.status_code}: {response.reason} - {response.text}"
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
