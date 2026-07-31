from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import CHANNELS


async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تشخیص درست کاربر چه از پیام مستقیم چه از دکمه شیشه‌ای
    user = update.effective_user
    if not user:
        return False
    user_id = user.id
    
    not_joined = []

    for number, channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )

            # بررسی وضعیت عضویت (اگر کاربر خارج شده یا اخراج شده باشد)
            if member.status in ["left", "kicked"]:
                not_joined.append((number, channel))

        except Exception as e:
            print(f"Error checking channel {channel}: {e}")
            not_joined.append((number, channel))

    if not_joined:
        buttons = []

        for number, channel in not_joined:
            # اگر کانال آیدی است، لینک آن را درست بسازید یا اگر خودش لینک است مستقیم استفاده کنید
            channel_url = channel if channel.startswith("https") else f"https://t.me/{channel.replace('@', '')}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{number} کانال 🌸",
                        url=channel_url
                    )
                ]
            )

        buttons.append(
            [
                InlineKeyboardButton(
                    "✅ عضو شدم",
                    callback_data="check_join"
                )
            ]
        )

        text = (
            "وااای 🥺🌸 هنوز همه‌ی کانال‌های یوری رو عضو نشدی\n\n"
            "برای استفاده از ملورینا اول این کانال‌ها رو دنبال کن 💗\n"
            "بعد برگرد و روی «عضو شدم» بزن ✨"
        )

        # ارسال پیام جدید یا ویرایش پیام قبلی
        message = update.effective_message
        if message:
            await message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        return False

    return True


async def check_join_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if await check_membership(update, context):
        await query.message.edit_text(
            "وااای خوش اومدییی 🥺🌸\n"
            "حالا می‌تونی با ملورینا حرف بزنی 💗"
        )
    else:
        await query.answer(
            "هنوز بعضی کانال‌ها مونده 🥺",
            show_alert=True
        )
