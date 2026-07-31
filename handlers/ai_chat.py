from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import openai
import json
import os
import random
from datetime import datetime, timedelta
from config import OPENAI_API_KEY, PERSONALITY

openai.api_key = OPENAI_API_KEY

# ========== فایل‌های دیتابیس ==========
HISTORY_FILE = "data/chat_history.json"
IDEAS_FILE = "data/chat_ideas.json"

# ========== دکمه‌های شیشه‌ای کیوت ==========
CHAT_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🌸 ایده جدید", callback_data="ai_idea"),
        InlineKeyboardButton("💡 پیشنهاد بده", callback_data="ai_suggest")
    ],
    [
        InlineKeyboardButton("🎨 تغییر شخصیت", callback_data="ai_personality"),
        InlineKeyboardButton("📝 خلاصه مکالمه", callback_data="ai_summary")
    ],
    [
        InlineKeyboardButton("🔄 شروع مجدد", callback_data="ai_reset"),
        InlineKeyboardButton("📊 آمار مکالمه", callback_data="ai_stats")
    ],
    [
        InlineKeyboardButton("🎭 حالت شوخ", callback_data="ai_funny"),
        InlineKeyboardButton("🌸 حالت عادی", callback_data="ai_normal")
    ],
    [
        InlineKeyboardButton("🔙 منوی اصلی", callback_data="main_menu")
    ]
])

# ========== ایده‌های جدید برای مکالمه ==========
CHAT_IDEAS = [
    "بیا یه داستان عاشقانه باهم بنویسیم! 📝",
    "اگه یه روز به دنیای انیمه بری، چه کار می‌کنی؟ 🌸",
    "بهترین خاطره‌ات با انیمه چیه؟ 🎬",
    "اگه می‌تونستی یه شخصیت انیمه بسازی، چی بود؟ ✨",
    "به نظرت عشق واقعی توی انیمه‌ها چطوریه؟ 💕",
    "اگه یه ابرقدرت می‌داشتی، چی انتخاب می‌کردی؟ ⚡",
    "بهترین انیمه‌ای که تا حالا دیدی چیه؟ 🎭",
    "اگه یه روز رو توی یه انیمه زندگی کنی، کدوم رو انتخاب می‌کنی؟ 🌟",
    "چه شخصیت انیمه‌ای بهت شبیه‌تره؟ 🎀",
    "بهترین موسیقی متن انیمه‌ای که شنیدی؟ 🎵"
]

# ========== توابع مدیریت تاریخچه ==========
def load_history(user_id):
    """لود کردن تاریخچه مکالمه"""
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump({}, f)
    
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    
    if str(user_id) not in data:
        data[str(user_id)] = {
            "history": [],
            "mood": "normal",
            "chat_count": 0,
            "last_reset": str(datetime.now())
        }
    
    return data[str(user_id)]

def save_history(user_id, data):
    """ذخیره تاریخچه"""
    with open(HISTORY_FILE, "r") as f:
        all_data = json.load(f)
    
    all_data[str(user_id)] = data
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

def dedup_history(history):
    """حذف جواب‌های تکراری - نسخه پیشرفته"""
    if len(history) < 4:
        return history
    
    # چک کردن ۴ جواب آخر
    last_4 = history[-4:]
    assistant_msgs = [msg["content"] for msg in last_4 if msg["role"] == "assistant"]
    
    # اگه ۳ جواب آخر شبیه هم بودن
    if len(set(assistant_msgs)) <= 2 and len(assistant_msgs) >= 3:
        # یه جواب جدید تولید کن
        return history[:-2]
    
    # چک کردن کلمات تکراری
    if len(assistant_msgs) >= 2:
        words1 = set(assistant_msgs[0].split())
        words2 = set(assistant_msgs[1].split())
        if len(words1.intersection(words2)) / len(words1) > 0.7:
            return history[:-1]
    
    return history

# ========== تابع اصلی چت ==========
async def chat_with_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به پیام‌های کاربر با هوش مصنوعی و دکمه‌های شیشه‌ای"""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # اگه پیام دستور بود، نادیده بگیر
    if user_message.startswith('/'):
        return
    
    # لود کردن تاریخچه
    user_data = load_history(user_id)
    history = user_data.get("history", [])
    mood = user_data.get("mood", "normal")
    chat_count = user_data.get("chat_count", 0) + 1
    user_data["chat_count"] = chat_count
    
    # اضافه کردن پیام کاربر
    history.append({"role": "user", "content": user_message})
    
    # حذف جواب‌های تکراری
    history = dedup_history(history)
    
    # ساخت پیام برای GPT با شخصیت و حالت
    personality = PERSONALITY
    
    # اضافه کردن حالت‌های مختلف
    if mood == "funny":
        personality += "\nحالت شوخ داری و کلی joke می‌گی. خیلی بامزه و شاد هستی."
    elif mood == "romantic":
        personality += "\nحالت عاشقانه داری و با احساسات قشنگ حرف می‌زنی."
    elif mood == "creative":
        personality += "\nحالت خلاق داری و ایده‌های جدید و جذاب می‌دی."
    
    # اضافه کردن تعداد مکالمه برای تنوع
    personality += f"\nاین {chat_count}امین پیام کاربره. سعی کن هر بار یه چیز جدید بگی."
    
    messages = [
        {"role": "system", "content": f"تو ملورینا هستی. {personality}"}
    ]
    
    # اضافه کردن تاریخچه (آخرین ۱۵ پیام)
    for msg in history[-15:]:
        messages.append(msg)
    
    try:
        # ارتباط با GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=400,
            temperature=0.85,  # برای تنوع بیشتر
            top_p=0.9,
            presence_penalty=0.6,  # جلوگیری از تکرار
            frequency_penalty=0.5
        )
        
        bot_reply = response.choices[0].message.content
        
        # اضافه کردن جواب ربات به تاریخچه
        history.append({"role": "assistant", "content": bot_reply})
        user_data["history"] = history
        save_history(user_id, user_data)
        
        # ارسال جواب با دکمه‌های شیشه‌ای
        await update.message.reply_text(
            bot_reply,
            reply_markup=CHAT_BUTTONS,
            parse_mode="Markdown"
        )
        
        # اگه تعداد پیام‌ها زیاد شد، یه ایده جدید پیشنهاد بده
        if chat_count % 5 == 0 and chat_count > 0:
            idea = random.choice(CHAT_IDEAS)
            await update.message.reply_text(
                f"🌸 {idea}\n\n"
                f"چی می‌گی عزیزم؟ 🥰",
                reply_markup=CHAT_BUTTONS
            )
        
    except Exception as e:
        await update.message.reply_text(
            "🥺 اوه! یه مشکلی پیش اومده!\n"
            "یکم دیگه دوباره امتحان کن عزیزم... 💫\n\n"
            "اگه دوست داری، می‌تونی از دکمه‌های زیر استفاده کنی:",
            reply_markup=CHAT_BUTTONS
        )
        print(f"GPT Error: {e}")

# ========== دکمه‌های شیشه‌ای ==========
async def ai_buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت دکمه‌های چت"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = load_history(user_id)
    action = query.data
    
    if action == "ai_idea":
        # ارسال یک ایده جدید
        idea = random.choice(CHAT_IDEAS)
        await query.edit_message_text(
            f"💡 **ایده جدید برای مکالمه:**\n\n"
            f"{idea}\n\n"
            f"🌸 چطوره راجع به این حرف بزنیم؟ 🥰",
            reply_markup=CHAT_BUTTONS,
            parse_mode="Markdown"
        )
    
    elif action == "ai_suggest":
        # پیشنهاد موضوعات جدید
        suggestions = [
            "انیمه‌های جدید که باید ببینی 🎬",
            "بهترین شخصیت‌های انیمه‌ای 🎭",
            "داستان‌های عاشقانه انیمه‌ای 💕",
            "انیمه‌های کمدی بامزه 😄",
            "انیمه‌های فانتزی و جادویی ✨"
        ]
        suggest = random.choice(suggestions)
        await query.edit_message_text(
            f"💫 **پیشنهاد من:**\n\n"
            f"بیا راجع به «{suggest}» حرف بزنیم!\n\n"
            f"🌸 نظرت چیه؟ 🥰",
            reply_markup=CHAT_BUTTONS,
            parse_mode="Markdown"
        )
    
    elif action == "ai_personality":
        # تغییر شخصیت
        keyboard = [
            [
                InlineKeyboardButton("🌸 عادی", callback_data="personality_normal"),
                InlineKeyboardButton("😂 شوخ", callback_data="personality_funny")
            ],
            [
                InlineKeyboardButton("💕 عاشقانه", callback_data="personality_romantic"),
                InlineKeyboardButton("🎨 خلاق", callback_data="personality_creative")
            ],
            [InlineKeyboardButton("🔙 برگشت", callback_data="personality_back")]
        ]
        await query.edit_message_text(
            "🎭 **انتخاب شخصیت ملورینا:**\n\n"
            "یه حالت رو انتخاب کن تا با اون حالت باهات حرف بزنم! 🥰\n\n"
            "🌸 هر حالت یه جور خاص و قشنگه!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif action.startswith("personality_"):
        # تغییر شخصیت
        mood = action.replace("personality_", "")
        if mood in ["normal", "funny", "romantic", "creative"]:
            user_data["mood"] = mood
            save_history(user_id, user_data)
            
            moods = {
                "normal": "🌸 حالت عادی",
                "funny": "😂 حالت شوخ",
                "romantic": "💕 حالت عاشقانه",
                "creative": "🎨 حالت خلاق"
            }
            
            await query.edit_message_text(
                f"✅ {moods.get(mood, '')} فعال شد!\n\n"
                f"🥰 حالا با این حالت باهات حرف می‌زنم!\n"
                f"بیا ادامه بدیم... 💫",
                reply_markup=CHAT_BUTTONS
            )
    
    elif action == "ai_summary":
        # خلاصه مکالمه
        history = user_data.get("history", [])
        if len(history) < 2:
            await query.edit_message_text(
                "📝 هنوز مکالمه‌ای نداشتیم!\n"
                "بیا شروع کنیم تا خاطره‌های قشنگ بسازیم! 🥰",
                reply_markup=CHAT_BUTTONS
            )
            return
        
        # خلاصه‌سازی با GPT
        try:
            summary_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "خلاصه‌ای از مکالمه زیر بنویس (حداکثر ۵ خط)"},
                    {"role": "user", "content": str(history[-10:])}
                ],
                max_tokens=100
            )
            summary = summary_response.choices[0].message.content
            
            await query.edit_message_text(
                f"📝 **خلاصه مکالمه:**\n\n"
                f"{summary}\n\n"
                f"🌸 چیزای قشنگی گفتیم! 🥰",
                reply_markup=CHAT_BUTTONS,
                parse_mode="Markdown"
            )
        except:
            await query.edit_message_text(
                "📝 **خلاصه مکالمه:**\n\n"
                f"تعداد پیام‌ها: {len(history)}\n"
                f"🌸 خاطرات قشنگ زیادی داریم! 🥰",
                reply_markup=CHAT_BUTTONS
            )
    
    elif action == "ai_reset":
        # شروع مجدد
        user_data["history"] = []
        user_data["chat_count"] = 0
        save_history(user_id, user_data)
        
        await query.edit_message_text(
            "🔄 **مکالمه ریست شد!** 🔄\n\n"
            "🌸 مثل یه شروع تازه!\n"
            "خوشحالم که دوباره باهام حرف می‌زنی! 🥰\n\n"
            "بیا از اول شروع کنیم... 💫",
            reply_markup=CHAT_BUTTONS
        )
    
    elif action == "ai_stats":
        # آمار مکالمه
        history = user_data.get("history", [])
        chat_count = user_data.get("chat_count", 0)
        mood = user_data.get("mood", "normal")
        
        moods = {
            "normal": "🌸 عادی",
            "funny": "😂 شوخ",
            "romantic": "💕 عاشقانه",
            "creative": "🎨 خلاق"
        }
        
        await query.edit_message_text(
            f"📊 **آمار مکالمه با ملورینا:**\n\n"
            f"💬 تعداد پیام‌ها: {chat_count}\n"
            f"🎭 حالت فعلی: {moods.get(mood, '🌸 عادی')}\n"
            f"📝 طول تاریخچه: {len(history)} پیام\n"
            f"🌸 مدت زمان: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"🥰 خوشحالم که باهات حرف می‌زنم! 💫",
            reply_markup=CHAT_BUTTONS,
            parse_mode="Markdown"
        )
    
    elif action == "ai_funny":
        # حالت شوخ
        user_data["mood"] = "funny"
        save_history(user_id, user_data)
        
        await query.edit_message_text(
            "😂 **حالت شوخ فعال شد!**\n\n"
            "🌸 دیگه کلی می‌خندیم با هم!\n"
            "بیا یه کم بخندیم... 🥰",
            reply_markup=CHAT_BUTTONS
        )
    
    elif action == "ai_normal":
        # حالت عادی
        user_data["mood"] = "normal"
        save_history(user_id, user_data)
        
        await query.edit_message_text(
            "🌸 **حالت عادی فعال شد!**\n\n"
            "🥰 برگشتیم به حالت معمولی و قشنگ!\n"
            "بیا ادامه بدیم... 💫",
            reply_markup=CHAT_BUTTONS
        )
    
    elif action == "personality_back":
        # برگشت به چت
        await query.edit_message_text(
            "🌸 برگشتیم به مکالمه!\n"
            "🥰 چیز جدیدی بگو؟",
            reply_markup=CHAT_BUTTONS
        )
