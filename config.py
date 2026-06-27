import os
import sys
from dotenv import load_dotenv

load_dotenv()

def _require(key: str) -> str:
    """Get required env var — exits with clear message if missing."""
    val = os.environ.get(key, "").strip()
    if not val:
        print(f"\n[FATAL] Required env var '{key}' is not set in Railway Variables!", file=sys.stderr)
        print(f"[FATAL] In Railway → Variables → add:  {key}  =  <your value>", file=sys.stderr)
        sys.exit(1)
    return val

BOT_TOKEN:       str = _require("BOT_TOKEN")
API_ID:          int = int(_require("API_ID"))
API_HASH:        str = _require("API_HASH")
OWNER_ID:        int = int(os.environ.get("OWNER_ID", "0").strip())
PORT:            int = int(os.environ.get("PORT", "8080").strip())
USERBOT_SESSION: str = os.environ.get("USERBOT_SESSION", "").strip()  # optional, for /names
