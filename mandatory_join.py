from telegram import Update
from telegram.ext import ContextTypes
from config import CHANNELS

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    not_joined = []

    for num, username, link in CHANNELS:
        try:
            chat_member = await context.bot.get_chat_member(username, user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                not_joined.append((num, username, link))
        except:
            not_joined.append((num, username, link))

    if not_joined:
        text = "وایی 😢🌸 هنوز همه‌ی کانال‌های یوری رو عضو نشدی\n\n"
        text += "برای استفاده از ملورینا اول این کانال‌ها رو دنبال کن 💗\n"
        text += "بعد برگرد و روی «عضو شدم» بزن ✨\n\n"

        for num, username, link in not_joined:
            text += f"{num} کانال: {link}\n"

        await update.message.reply_text(text)
        return False

    return True


async def check_join_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    not_joined = []

    for num, username, link in CHANNELS:
        try:
            chat_member = await context.bot.get_chat_member(username, user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                not_joined.append((num, username, link))
        except:
            not_joined.append((num, username, link))

    if not_joined:
        text = "وایی 😢🌸 هنوز عضو همه کانال‌ها نشدی\n"
        text += "لطفاً همه رو دنبال کن و دوباره امتحان کن 💗\n\n"

        for num, username, link in not_joined:
            text += f"{num} کانال: {link}\n"

        await query.edit_message_text(text)
        return

    # اگر همه کانال‌ها عضو بود → منو باز کن
    from keyboards import main_menu
    await query.edit_message_text(
        "عالیه 😍✨\nهمه کانال‌ها رو عضو شدی!\n\n"
        "بزن بریم داخل منو 💗",
        reply_markup=main_menu()
    )
