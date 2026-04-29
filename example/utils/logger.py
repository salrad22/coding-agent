import datetime
import json


LOG_FILE = "app.log"


def log(message, level="INFO"):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "level": level,
        "message": message,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def info(message):
    log(message, "INFO")


def error(message):
    log(message, "ERROR")


def warning(message):
    log(message, "WARNING")


