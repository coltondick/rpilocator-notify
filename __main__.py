import monitor
import telegram

# Importing the start_monitor function from the monitor.py file and then calling it with the chat_id
# returned by the get_chat_id function in the telegram.py file.
monitor.start_monitor(telegram.get_chat_id())
