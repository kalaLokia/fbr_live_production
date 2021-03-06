"""
Main configurations of the application, this file needed to be loaded initially.

"""

import configparser
import os

from . import ROOT, CONNECTION_STRING, LOG_SUNDAY, MIN_PRODUCTION, PRODUCTION_START_HOUR
from .log_me import logMessage

if not os.path.exists(ROOT):
    os.makedirs(ROOT)

SLACK_WH = None
DISCORD_WH = None
GOOGLE_WH = None
SLACK_APP_TOKEN = None
SLACK_CHANNEL_ID = None
DISPLAY_HOUR_COUNT = 0

DATABASE_NAME = "barcode"  # default

is_api_available = False

config = configparser.ConfigParser(interpolation=None)
exists = config.read(ROOT + "config.ini")


if exists:

    if config.has_section("SQL SERVER"):
        try:
            DATABASE_NAME = config["SQL SERVER"]["DATABASE"]
            CONNECTION_STRING = (
                r"Driver={ODBC Driver 17 for SQL Server};"
                rf'Server={config["SQL SERVER"]["SERVER"]};'
                rf"Database={DATABASE_NAME};"
                rf'uid={config["SQL SERVER"]["UID"]};'
                rf'pwd={config["SQL SERVER"]["PWD"]};'
                r"Integrated Security=false;"
            )
        except KeyError as e:
            CONNECTION_STRING = None
            logMessage(f'Required key "{e.args[0]}" not found in configurations.')

    if config.has_section("SLACK APP"):
        try:
            SLACK_APP_TOKEN = config["SLACK APP"]["BOT_TOKEN"]
            SLACK_CHANNEL_ID = config["SLACK APP"]["CHANNEL_ID"]
            if not SLACK_APP_TOKEN.startswith("xoxb"):
                SLACK_APP_TOKEN = None
            else:
                is_api_available = True
        except KeyError as e:
            SLACK_APP_TOKEN = None
            logMessage(f'Required key "{e.args[0]}" not found in configurations.')

    if config.has_option("WEBHOOK", "SLACK"):
        value = config.get("WEBHOOK", "SLACK")
        if value.startswith("https://hooks.slack.com/services/"):
            SLACK_WH = value
            is_api_available = True

    if config.has_option("WEBHOOK", "DISCORD"):
        value = config.get("WEBHOOK", "DISCORD")
        if value.startswith("https://discord"):
            DISCORD_WH = value
            is_api_available = True

    if config.has_option("WEBHOOK", "GOOGLE"):
        value = config.get("WEBHOOK", "GOOGLE")
        if value.startswith("https://chat.googleapis.com"):
            GOOGLE_WH = value
            is_api_available = True

    if config.has_option("GENERAL", "SUNDAY_ENABLE"):
        value = config.get("GENERAL", "SUNDAY_ENABLE")
        try:
            if int(value) != 0:
                LOG_SUNDAY = True
        except:
            pass  # Default value will consider

    if config.has_option("GENERAL", "MIN_PRODUCTION_LOGGING"):
        value = config.get("GENERAL", "MIN_PRODUCTION_LOGGING")
        try:
            if int(value) > 0:
                MIN_PRODUCTION = int(value)
        except:
            pass  # Default value will consider

    if config.has_option("GENERAL", "PRODUCTION_START_HOUR"):
        value = config.get("GENERAL", "PRODUCTION_START_HOUR")
        try:
            value = int(value)
            if value >= 0 and value < 24:
                PRODUCTION_START_HOUR = value
        except:
            pass  # Default value will consider
    if config.has_option("GENERAL", "DISPLAY_HOUR_COUNT"):
        value = config.get("GENERAL", "DISPLAY_HOUR_COUNT")
        try:
            value = int(value)
            if value == 1:
                DISPLAY_HOUR_COUNT = value
        except:
            pass  # Default value will consider

    if not is_api_available:
        logMessage("No valid webhook configurations found. Failed to sent report.")
else:
    CONNECTION_STRING = None
    logMessage("Configuration file missing, Exiting..!")  # Then do not run
