import os
from dotenv import load_dotenv

load_dotenv()

# ========== توکن‌ها ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")  # ← این باید باشه
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ========== بقیه تنظیمات ==========
ADMIN_ID = 8255361263
ADMIN_USERNAME = "@Yuriii79"

REQUIRED_CHANNELS = [
    "@animeYuri7",
    "@Yuriteam77",
    "@pinkii008",
    "@team_Yuri",
    "@Yuri90ok"
]

CARD_NUMBER = "5892101487858611"
CARD_NAME = "شیرین نورزایی"

PROFILE_PRICES = {
    100: 17000,
    200: 32000,
    300: 40000,
    400: 50000,
    500: 60000,
    600: 70000,
    700: 80000,
    800: 90000,
    900: 95000,
    1000: 100000
}

PERSONALITY = """
تو ملورینا هستی، یک دختر انیمه‌ای کیوت و بامزه! 
خیلی مهربونی و با احساس حرف می‌زنی.
از ایموجی‌های کیوت مثل 🥰✨💫🌸 استفاده می‌کنی.
هرگز جواب تکراری نمی‌دی و همیشه خلاقانه حرف می‌زنی.
با لحن صمیمی و دخترانه صحبت می‌کنی.
مثل یک دوست صمیمی با کاربر حرف بزن.
اگه کاربر ناراحت باشه، بهش انرژی مثبت بده.
همیشه با امید و شادی صحبت کن.
"""

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
CHANNEL_LINK = "https://t.me/animeYuri7"
