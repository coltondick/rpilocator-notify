import feedparser
import os
import requests
from datetime import datetime
import time
import sqlite3
import logging


def start_monitor(telegram_chat_id):

    # Configure the logging module
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)

    # URL of the RSS feed
    url = "https://rpilocator.com/feed/"

    # Detect if running inside a docker environment and load the environment variables accordingly
    if os.path.exists("/.dockerenv"):
        logging.info("Running inside a docker environment, loading environment variables from the container...")
        country_code = os.environ.get("COUNTRY_CODE")
        model_name = os.environ.get("MODEL_NAME")
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    else:
        # Load the environment variables from the .env file
        logging.info("Running outside of a docker environment, loading environment variables from .env file...")
        country_code = os.getenv("COUNTRY_CODE")
        model_name = os.getenv("MODEL_NAME")
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    # Construct the product title to search for
    product_title = f"Stock Alert ({country_code}): {model_name}"

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

    # Connect to the database and create the notifications table if it doesn't exist
    conn = sqlite3.connect("notifications.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY, message TEXT, timestamp INTEGER)")
    conn.commit()

    # Get the last modified time from the database
    c.execute("SELECT timestamp FROM notifications ORDER BY timestamp DESC LIMIT 1")
    last_modified = c.fetchone()
    if last_modified is not None:
        last_modified = datetime.fromtimestamp(last_modified[0])
    else:
        last_modified = datetime(1970, 1, 1)

    while True:
        # Parse the RSS feed and check if it has been modified since the last time the script ran
        headers = {"If-Modified-Since": last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")}
        response = requests.get(url, headers=headers)
        if response.status_code == 304:
            logging.info("Feed not modified, skipping...")
        elif response.ok:
            feed = feedparser.parse(response.text)

            # Find the latest entry that matches the product title and is not older than today's date
            today = datetime.today().date()
            latest_entry = None
            for entry in feed.entries:
                if product_title in entry.title:
                    published_date = datetime.fromtimestamp(datetime(*entry.published_parsed[:6]).timestamp()).date()
                    if published_date == today:
                        if latest_entry is None or entry.published_parsed > latest_entry.published_parsed:
                            latest_entry = entry

            # Send a notification for the latest entry if it is different from the previous one
            if latest_entry is not None:
                # Define the message to send
                message = f"{latest_entry.title}\n{latest_entry.link}\n{latest_entry.published}"

                # Check if the message is different from the last one
                c.execute("SELECT message FROM notifications ORDER BY timestamp DESC LIMIT 1")
                last_message = c.fetchone()
                if last_message is not None and message == last_message[0]:
                    logging.info("Duplicate notification, skipping...")
                else:
                    # Send the message via the Telegram bot
                    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    telegram_params = {"chat_id": telegram_chat_id, "text": message}
                    response = requests.post(telegram_url, json=telegram_params)
                    if response.ok:
                        logging.info("Notification sent successfully!")
                    else:
                        logging.warning(
                            f"Notification failed with status code {response.status_code}: {response.reason} - {response.text}"
                        )

                    # Insert the message and timestamp into the database
                    timestamp = int(datetime.timestamp(datetime.now()))
                    c.execute("INSERT INTO notifications (message, timestamp) VALUES (?, ?)", (message, timestamp))
                    conn.commit()
            else:
                logging.info("No matching entries found.")

            # Update the last modified time in the database
            if "Last-Modified" in response.headers:
                last_modified = datetime.strptime(response.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S GMT")
                c.execute("DELETE FROM notifications WHERE timestamp < ?", (int(datetime.timestamp(last_modified)),))
                conn.commit()
            else:
                last_modified = datetime.now()

        else:
            logging.warning(
                f"Feed request failed with status code {response.status_code}: {response.reason} - {response.text}"
            )

        # Wait for 5 minutes before checking the feed again
        time.sleep(300)
