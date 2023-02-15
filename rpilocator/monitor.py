"""
This module monitors an RSS feed for a specific product and sends notifications through a notifier when a new entry is added.

The RSS feed URL, the product title to search for, and the notifier object are provided as arguments to the start_monitor function. The notifier object must have a send_notification method that accepts a message string.

When a new entry is found in the RSS feed, the function checks if it is different from the previous one stored in a SQLite database. If it is different, the message is sent via the notifier object and the entry is stored in the database.

The function runs in an infinite loop, checking the feed every 5 minutes.

Note: The feedparser and requests modules must be installed to run this module.
"""

import sqlite3
import time
from datetime import datetime
import logging
import feedparser
import requests


def start_monitor(notifier, country_code, model_name):
    """Starts monitoring an RSS feed and sends notifications to a notifier when a new entry is added."""
    # URL of the RSS feed
    url = "https://rpilocator.com/feed/"

    # Construct the product title to search for
    product_title = f"Stock Alert ({country_code}): {model_name}"

    # Connect to the database and create the notifications table if it doesn't exist
    conn = sqlite3.connect("notifications.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY, message TEXT, timestamp INTEGER)")
    conn.commit()

    # Get the last modified time from the database
    cur.execute("SELECT timestamp FROM notifications ORDER BY timestamp DESC LIMIT 1")
    last_modified = cur.fetchone()
    if last_modified is not None:
        last_modified = datetime.fromtimestamp(last_modified[0])
    else:
        last_modified = datetime(1970, 1, 1)

    while True:
        # Parse the RSS feed and check if it has been modified since the last time the script ran
        headers = {"If-Modified-Since": last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")}
        response = requests.get(url, headers=headers, timeout=30)
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
                cur.execute("SELECT message FROM notifications ORDER BY timestamp DESC LIMIT 1")
                last_message = cur.fetchone()
                if last_message is not None and message == last_message[0]:
                    logging.info("Duplicate notification, skipping...")
                else:
                    # Send the message via the notifier
                    notifier.send_notification(message)

                    # Insert the message and timestamp into the database
                    timestamp = int(datetime.timestamp(datetime.now()))
                    cur.execute("INSERT INTO notifications (message, timestamp) VALUES (?, ?)", (message, timestamp))
                    conn.commit()
            else:
                logging.info("No matching entries found.")

            # Update the last modified time in the database
            if "Last-Modified" in response.headers:
                last_modified = datetime.strptime(response.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S GMT")
                cur.execute("DELETE FROM notifications WHERE timestamp < ?", (int(datetime.timestamp(last_modified)),))
                conn.commit()
            else:
                last_modified = datetime.now()

        else:
            logging.warning(
                "Feed request failed with status code %s: %s - %s", response.status_code, response.reason, response.text
            )

        # Wait for 5 minutes before checking the feed again
        time.sleep(300)
