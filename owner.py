from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

OWNER_ID = 8255361263


def is_owner(user_id):
    return user_id == OWNER_ID



async def owner_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not is_owner(user_id):
        await update.message.reply_text(
            "این بخش فقط برای سازنده ملورینا هست 🌸"
        )
        return


    buttons = [

        [
            InlineKeyboardButton(
                "🛡 اضافه کردن فیلترشکن",
                callback_data="add_vpn"
            )
        ],

        [
            InlineKeyboardButton(
                "🎀 اضافه کردن استیکر به ملورینا",
                callback_data="add_sticker"
            )
        ],

        [
            InlineKeyboardButton(
                "🤖 ساخت ربات با کد اجرا",
                callback_data="create_bot"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 معرفی فیلترشکن رایگان",
                callback_data="free_vpn"
            )
        ]

    ]


    await update.message.reply_text(
        "👑 پنل سازنده ملورینا\n\n"
        "سلام سازنده‌ی من 🌸\n"
        "اینجا فقط خودت به تنظیمات ویژه دسترسی داری 💗",

        reply_markup=InlineKeyboardMarkup(buttons)
    )



async def owner_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "add_vpn":

        await query.edit_message_text(
            "🛡 بخش اضافه کردن فیلترشکن\n\n"
            "اینجا بعداً سرور یا لینک فیلترشکن اضافه می‌کنیم."
        )


    elif query.data == "add_sticker":

        await query.edit_message_text(
            "🎀 استیکر جدید را بفرست تا برای شخصیت ملورینا ذخیره شود."
        )


    elif query.data == "create_bot":

        await query.edit_message_text(
            "🤖 ساخت ربات با کد\n\n"
            "این بخش بعداً برای ساخت ربات‌های جدید اضافه می‌شود."
        )


    elif query.data == "free_vpn":

        await query.edit_message_text(
            "🌸 معرفی فیلترشکن رایگان\n\n"
            "این بخش برای همه کاربران نمایش داده می‌شود."
      )
