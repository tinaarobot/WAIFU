import os
import telegram.ext as tg
from pyrogram import Client
import logging  
from telegram.ext import Application

from motor.motor_asyncio import AsyncIOMotorClient
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

### ❖ ➥
OWNER_ID = os.getenv("OWNER_ID", None)

### ❖ ➥
SUDO_USERS = os.getenv("SUDO_USERS", None).split()

### ❖ ➥
LOGGER_ID = os.getenv("LOGGER_ID", None)

### ❖ ➥
BOT_USERNAME = os.getenv("BOT_USERNAME", None)

### ❖ ➥
BOT_TOKEN = os.getenv("BOT_TOKEN", None)

### ❖ ➥
MONGO_URL = os.getenv("MONGO_URL", None)

### ❖ ➥
IMG_URL = os.getenv("IMG_URL", None).split()

### ❖ ➥
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", None)

### ❖ ➥
CHANNEL_ID = os.getenv("CHANNEL_ID", None)

### ❖ ➥
API_HASH = os.getenv("API_HASH", None)

### ❖ ➥
API_ID = os.getenv("API_ID", None)

### ❖ ➥
UPDATE_CHAT = os.getenv("UPDATE_CHAT", None)

application = Application.builder().token(BOT_TOKEN).build()
ROY = Client(
    "lmao",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    
    
)
client = AsyncIOMotorClient(MONGO_URL)
db = client['Character_catcher']
collection = db['anime_characters_lol']
user_totals_collection = db['user_totals_lmaoooo']
user_collection = db["user_collection_lmaoooo"]
group_user_totals_collection = db['group_user_totalsssssss']
top_global_groups_collection = db['top_global_groups']



