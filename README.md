# Raspberry Pi Locator Telegram Notifier

This script checks the [rpilocator.com](rpilocator.com) RSS feed for stock alerts for a specified country and model, and sends a notification via Telegram when a new stock alert is found.

## Prerequisites

- Docker
- A Telegram account

## Required:

1. Create a new Telegram bot using [BotFather](https://t.me/BotFather):
   - Open a chat with BotFather and send the command `/newbot`.
   - Follow the prompts to choose a name and username for your bot.
   - BotFather will provide you with a token for your bot - make a note of this as you will need it later.
2. Create a new chat with your bot and send it a message to start the conversation.
3. Copy the `.env.example` file to a new file named `.env`.
4. Set the values for the environment variables in the `.env` file:
   - `COUNTRY_CODE`: The country code to search for in the stock alerts.
   - `MODEL_NAME`: The name of the model to search for in the stock alerts.
   - `TELEGRAM_BOT_TOKEN`: The Telegram bot token for your bot (obtained in step 1).

## Build and Run:

1. Clone the repository with `git clone https://github.com/coltondick/rpilocator-telegram-notify.git`.
2. Navigate to the repository with `cd rpilocator-telegram-notify`.
3. Copy the `.env.example` file to a new file named `.env`.
4. Set the values for the environment variables in the `.env` file:
   - `COUNTRY_CODE`: The country code to search for in the stock alerts.
   - `MODEL_NAME`: The name of the model to search for in the stock alerts.
   - `TELEGRAM_BOT_TOKEN`: The Telegram bot token to use for sending notifications.
5. Build the Docker image with `docker build -t rpilocator-telegram-notify .`.
6. Run the Docker container with `docker run -d --name rpilocator-telegram-notify --env-file .env rpilocator-telegram-notify`.

## Manual Instructions:

1. Install the required packages by running `pip install -r requirements.txt`.
2. Run the script with `python __main__.py`.

## Usage

The script will check the Raspberry Pi Locator RSS feed every 5 minutes for new stock alerts for the specified country and model. If a new stock alert is found, the script will send a notification via Telegram to the specified chat ID. If the same stock alert has already been sent in a previous notification, the script will not send another notification.

The script also stores the notifications in a SQLite database. If the feed has been modified since the last time the script ran, the script will update the database with the latest notifications and remove any notifications that are no longer in the feed.

## Contributing

If you find any bugs or have suggestions for improvements, please open an issue or pull request on the GitHub repository.

## License

This script is licensed under the [MIT License](LICENSE).
