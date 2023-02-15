from dependencies import *


def main():
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
        exit(1)

    # Start the monitor
    monitor.start_monitor(notifier, country_code, model_name)
    # monitor.start_monitor(telegram_bot_token, telegram_chat_id, country_code, model_name)


if __name__ == "__main__":
    main()
