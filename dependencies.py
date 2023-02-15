# dependencies.py

# Import standard library modules
from datetime import datetime
import logging
import os
import sqlite3
import time

# Import third-party packages
import feedparser
from dotenv import load_dotenv
import requests

# Import project modules
from rpilocator import monitor
from rpilocator import telegram
from rpilocator.notifier import TelegramNotifier
from rpilocator import notifier
