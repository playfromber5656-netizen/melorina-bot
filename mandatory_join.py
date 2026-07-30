from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import CHANNELS


async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    not_joined = []

    for number, channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )

            if member.status in ["left", "kicked"]:
                not_joined.append((number, channel))

        except Exception:
            not_joined.append((number, channel))


    if not_joined:

        buttons = []

        for number, channel in not_joined:
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{number} کانال 🌸",
                        url=channel
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


        await update.effective_message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        return False


    return True



async def check_join_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if await check_membership(update, context):

        await query.edit_message_text(
            "وااای خوش اومدییی 🥺🌸\n"
            "حالا می‌تونی با ملورینا حرف بزنی 💗"
        )

    else:

        await query.answer(
            "هنوز بعضی کانال‌ها مونده 🥺",
            show_alert=True
                          )
