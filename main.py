import os
import random

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import BOT_NAME
from personalities import get_reply
from mandatory_join import check_membership, check_join_button
from keyboards import main_menu, personality_menu
from owner import owner_panel, owner_buttons


TOKEN = os.getenv("BOT_TOKEN")


# ذخیره شخصیت کاربران
user_personality = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_membership(update, context):
        return

    await update.message.reply_text(
        f"سلاممم 🥺🌸\n"
        f"من {BOT_NAME} هستم 🧸💗\n"
        f"خیلی خوشحالم که اومدی پیشم ✨\n\n"
        f"هرچی دوست داری بگو، من گوش میدم 🌸",
        reply_markup=main_menu()
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_membership(update, context):
        return

    user_id = update.effective_user.id

    personality = user_personality.get(
        user_id,
        "cute"
    )

    text = update.message.text.lower()


    # جواب‌های مخصوص
    if "سلام" in text:
        replies = [
            "سلاممممم 🥺🌸 خوش اومدی",
            "وااای سلام 💗 ملورینا اینجاست",
            "سلام کوچولو 🌸 امروز حالت چطوره؟"
        ]

    elif "خوبی" in text:
        replies = [
            "آرههه خوبم 🧸💗 تو خوبی؟",
            "وقتی باهام حرف می‌زنی خوبم 🌸",
            "خوبم خوبم 😸✨"
        ]

    elif "چرا" in text:
        replies = [
            "چراااا؟ 🥺 بیا تعریف کن",
            "اوه اوه چرا؟ کنجکاوم بدونم 🌸"
        ]

    else:
        replies = [
            get_reply(personality),
            "وااای جالب بود 🥺 بیشتر بگو",
            "ملورینا داره گوش میده 🧸💗",
            "ههه چه بامزه گفتی 🌸",
            "من اینجام، ادامه بده ✨"
        ]


    await update.message.reply_text(
        random.choice(replies)
    )



async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "personalities":

        await query.edit_message_text(
            "شخصیت ملورینا رو انتخاب کن 🌸",
            reply_markup=personality_menu()
        )


    elif query.data in [
        "cute",
        "kind",
        "naughty",
        "tsundere",
        "sleepy",
        "crybaby",
        "princess"
    ]:

        user_personality[
            query.from_user.id
        ] = query.data


        await query.edit_message_text(
            "انتخاب شددد 🥺🌸\n"
            "ملورینا از این به بعد اینطوری حرف میزنه 💗"
        )


    elif query.data == "check_join":

        await check_join_button(
            update,
            context
        )


    elif query.data == "chat":

        await query.edit_message_text(
            "بگووو 🥺🌸 ملورینا گوش میده"
        )



def main():

    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "owner",
            owner_panel
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            buttons
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            owner_buttons
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )


    app.run_polling()



if __name__ == "__main__":
    main()
