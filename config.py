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

BOT_TOKEN:       str = _require("8998263670:AAFvRY4TBGj9SAX9CKu0Y9MKOO_rMCs43Po")
API_ID:          int = int(_require("30422005"))
API_HASH:        str = _require("5170ded206641d73215baf40175a6924")
OWNER_ID:        int = int(os.environ.get("5940554521", "0").strip())
PORT:            int = int(os.environ.get("PORT", "8080").strip())
USERBOT_SESSION: str = os.environ.get("BQHQM_UAjaUb14WrFgoqKUEcVmaBaQr3MxwCW8vzzXV4bXL-lxKAYOIDdBzVcbmg9R1Ay2sIor9QY4-xyzfssyzpTq4N6tcJqm0g_48w4mSJqudT54keIONOnUi-swWXeMoSwm_UiTs1fGolHX2tzIqoYyeQvR7MX1YCPORPz4zqhTU787VskCcDKb-vKwAbHN2cq21IVy5rVRDWQO2zHnbOuQDagDf_JWkdWQovNP80iprDbeJO8zSNQ-g26Yb_r92RO7OozRB2vlIgSXMVMlHWEoZS0nOcDV4iQj-B4bTl6PXMbzrf6bNdxa6eN2aJZcHvyTx6oSrK9mFyybumAJnvulNe1gAAAAIGL8ckAA", "").strip()  # optional, for /names
