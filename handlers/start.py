from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.channel_check import check_all_channels

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    not_member = await check_all_channels(update, context)
    
    if not_member:
        channel_list = "\n".join([f"{i+1}️⃣ {ch}" for i, ch in enumerate(not_member)])
        
        keyboard = []
        for ch in not_member:
            keyboard.append([InlineKeyboardButton(
                f"📢 عضویت در {ch}",
                url=f"https://t.me/{ch.replace('@', '')}"
            )])
        keyboard.append([InlineKeyboardButton("✅ بررسی مجدد", callback_data="check_again")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🌸 سلام عزیزم {user.first_name}! 🥰\n\n"
            f"برای اینکه بتونی با من حرف بزنی، باید تو این کانال‌های قشنگ عضو بشی:\n\n"
            f"{channel_list}\n\n"
            f"✨ پس از عضویت، دکمه بررسی رو بزن تا با هم بازی کنیم! 💫",
            reply_markup=reply_markup
        )
        return
    
    await show_main_menu(update.message, context)

async def show_main_menu(message, context):
    keyboard = [
        [InlineKeyboardButton("🎮 منوی دوم", callback_data="menu2"),
         InlineKeyboardButton("🎯 منوی سوم", callback_data="menu3")],
        [InlineKeyboardButton("📚 انگلیسی", callback_data="english"),
         InlineKeyboardButton("💰 ساخت ربات (پولی)", callback_data="build_bot")],
        [InlineKeyboardButton("⭐ امتیاز به ربات", callback_data="rate_bot"),
         InlineKeyboardButton("📖 مانگا", callback_data="manga")],
        [InlineKeyboardButton("🔐 معرفی فیلترشکن", callback_data="vpn"),
         InlineKeyboardButton("🎮 بازی", callback_data="game_menu")],
        [InlineKeyboardButton("👥 شرکت در بازی", callback_data="join_game")],
        [InlineKeyboardButton("🌸 پروفایل انیمه", callback_data="profile")],
        [InlineKeyboardButton("💝 پول توجیبی به ملورینا", callback_data="payment")],
        [InlineKeyboardButton("📢 تبلیغات", callback_data="ads")],
        [InlineKeyboardButton("🌐 شبکه‌های اجتماعی", callback_data="social")],
        [InlineKeyboardButton("🌸 کانال انیمه", url="https://t.me/animeYuri7")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(
        "🌸 **سلام عزیزم! من ملورینا هستم** 🥰✨\n\n"
        "از بین گزینه‌ها انتخاب کن تا باهم خوش بگذرونیم! 💫\n"
        "هر سوالی داری، بپرس که جواب تکراری نمی‌دم! 😉\n\n"
        "🌸 به کانالمون هم سر بزن!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_main_menu(query.message, context)
