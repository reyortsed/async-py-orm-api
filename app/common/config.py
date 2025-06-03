import os
from dotenv import load_dotenv

load_dotenv()

def get_env_or_secret(key: str) -> str:
    return os.getenv(f"DEVOPS_{key}") or os.getenv(key, "")

