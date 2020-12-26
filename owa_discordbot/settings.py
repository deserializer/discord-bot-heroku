import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
env_path = Path(".", ".env")
load_dotenv(env_path)

OWA_CONFIG = {
    "prefix": os.getenv("OWA_PREFIX"),
    "discord_token": os.getenv("OWA_DISCORD_TOKEN"),
    "csv_dir": os.getenv("OWA_QUESTIONS_CSV"),
}
