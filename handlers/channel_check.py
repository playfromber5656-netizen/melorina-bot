from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def check_all_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    required_channels = context.bot_data.get("required_channels", [])
    not_member = []
    
    for channel in required_channels:
        try:
            chat_member = await context.bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )
            if chat_member.status in ["left", "kicked"]:
                not_member.append(channel)
        except Exception:
            not_member.append(channel)
    
    return not_member

async def check_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    not_member = await check_all_channels(update, context)
    
    if not_member:
        keyboard = []
        for ch in not_member:
            keyboard.append([InlineKeyboardButton(
                f"📢 عضویت در {ch}",
                url=f"https://t.me/{ch.replace('@', '')}"
            )])
        keyboard.append([InlineKeyboardButton("✅ بررسی مجدد", callback_data="check_again")])
        
        await query.edit_message_text(
            f"🌸 عزیزم! هنوز تو این کانال‌ها عضو نشدی:\n\n"
            f"{chr(10).join([f'{i+1}️⃣ {ch}' for i, ch in enumerate(not_member)])}\n\n"
            f"برو عضو شو، بعد بیا پیش من! 🥰",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        from handlers.start import show_main_menu
        await query.edit_message_text("🌸 تبریک! همه کانال‌ها رو عضو شدی! 🥰")
        await show_main_menu(query.message, context)
