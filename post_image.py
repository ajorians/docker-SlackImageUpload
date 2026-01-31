import os
import sys
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")
IMAGE_PATH = os.environ.get("IMAGE_PATH", "/data/example.png")

START_FILE = os.environ.get("START_FILE", "/data/last_run.txt")

def log(msg):
    timestamp = datetime.utcnow().isoformat()
    print(f"[{timestamp}] {msg}", flush=True)

def main():
    log("Script started")

    try:
        with open(START_FILE, "a") as f:
            f.write(f"Started at {datetime.utcnow().isoformat()} UTC\n")
        log(f"Wrote start file: {START_FILE}")
    except Exception as e:
        log(f"Failed to write start file: {e}")

    if not SLACK_BOT_TOKEN:
        log("Missing SLACK_BOT_TOKEN")
        sys.exit(1)

    if not SLACK_CHANNEL:
        log("Missing SLACK_CHANNEL")
        sys.exit(1)

    client = WebClient(token=SLACK_BOT_TOKEN)

    try:
        log(f"Uploading image: {IMAGE_PATH}")
        response = client.files_upload_v2(
            channel=SLACK_CHANNEL,
            file=IMAGE_PATH,
            title="Testing Image",
            initial_comment="Testing something"
        )
        log("Upload successful:", response["file"]["id"])

    except SlackApiError as e:
        log("Error posting image:", e.response["error"])
    except Exception as e:
        log("Unexpected error:", str(e))

    log("Script finished successfully")

if __name__ == "__main__":
    main()

