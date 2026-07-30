from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():

    buttons = [

        [
            InlineKeyboardButton(
                "🌸 چت با ملورینا",
                callback_data="chat"
            )
        ],

        [
            InlineKeyboardButton(
                "🎭 تغییر شخصیت",
                callback_data="personalities"
            )
        ],

        [
            InlineKeyboardButton(
                "📖 بیوگرافی کیوت",
                callback_data="bio"
            )
        ],

        [
            InlineKeyboardButton(
                "🎮 بازی با ملورینا",
                callback_data="games"
            )
        ],

        [
            InlineKeyboardButton(
                "🌙 شب بخیر / ☀️ صبح بخیر",
                callback_data="good_morning_night"
            )
        ]

    ]


    return InlineKeyboardMarkup(buttons)



def personality_menu():

    buttons = [

        [
            InlineKeyboardButton(
                "🌸 کیوت",
                callback_data="cute"
            )
        ],

        [
            InlineKeyboardButton(
                "💗 مهربون",
                callback_data="kind"
            )
        ],

        [
            InlineKeyboardButton(
                "😈 شیطون",
                callback_data="naughty"
            )
        ],

        [
            InlineKeyboardButton(
                "🙄 لجباز",
                callback_data="tsundere"
            )
        ],

        [
            InlineKeyboardButton(
                "😴 خوابالو",
                callback_data="sleepy"
            )
        ],

        [
            InlineKeyboardButton(
                "🥺 بغلی",
                callback_data="crybaby"
            )
        ],

        [
            InlineKeyboardButton(
                "👑 پرنسس",
                callback_data="princess"
            )
        ]

    ]


    return InlineKeyboardMarkup(buttons)



def join_button():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🌸 عضو شدم",
                    callback_data="check_join"
                )
            ]
        ]
      )
