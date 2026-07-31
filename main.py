import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ConversationHandler
)
from config import BOT_TOKEN, ADMIN_ID, REQUIRED_CHANNELS

# ========== تنظیم لاگ ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== ایمپورت هندلرها ==========
from handlers.start import start_command, main_menu
from handlers.channel_check import check_all_channels, check_again
from handlers.ai_chat import chat_with_ai, ai_buttons_handler
from handlers.games import game_menu, rock_paper_scissors, game_2p, game_4p, game_6p
from handlers.manga import manga_menu, search_manga
from handlers.english import english_menu
from handlers.bot_builder import bot_builder_menu, build_new_bot, cancel
from handlers.profile_pics import profile_pics_menu, buy_profile_pics, select_style, select_color
from handlers.payments import (
    payment_menu, pay_manual, manual_pay_amount, 
    handle_payment_receipt, send_receipt_instruction,
    payment_history, payment_guide
)
from handlers.ads import ads_menu, send_ad_to_admin, confirm_ad, reject_ad
from handlers.memories import show_memories, save_memory
from handlers.add_to_channel import add_channel_menu, add_channel_new, get_channel_link, delete_channel
from handlers.social_media import social_media_menu, download_instagram, download_youtube, search_google
from admin_panel import admin_panel, admin_menu_callback, admin_stats, admin_update_bot, admin_settings

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # ========== ذخیره داده‌ها ==========
    app.bot_data["required_channels"] = REQUIRED_CHANNELS
    
    # ========== هندلرهای عمومی ==========
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(main_menu, pattern="main_menu"))
    app.add_handler(CallbackQueryHandler(check_again, pattern="check_again"))
    
    # ========== چت با AI (با دکمه‌های شیشه‌ای) ==========
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))
    app.add_handler(CallbackQueryHandler(ai_buttons_handler, pattern="^ai_"))
    app.add_handler(CallbackQueryHandler(ai_buttons_handler, pattern="^personality_"))
    
    # ========== پنل ادمین ==========
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(admin_menu_callback, pattern="admin_"))
    app.add_handler(CallbackQueryHandler(admin_stats, pattern="admin_stats"))
    app.add_handler(CallbackQueryHandler(admin_update_bot, pattern="admin_update"))
    app.add_handler(CallbackQueryHandler(admin_settings, pattern="admin_settings"))
    
    # ========== بازی ==========
    app.add_handler(CallbackQueryHandler(game_menu, pattern="game_menu"))
    app.add_handler(CallbackQueryHandler(rock_paper_scissors, pattern="rps_"))
    app.add_handler(CallbackQueryHandler(game_2p, pattern="game_2p"))
    app.add_handler(CallbackQueryHandler(game_4p, pattern="game_4p"))
    app.add_handler(CallbackQueryHandler(game_6p, pattern="game_6p"))
    
    # ========== مانگا ==========
    app.add_handler(CallbackQueryHandler(manga_menu, pattern="manga"))
    app.add_handler(CallbackQueryHandler(search_manga, pattern="manga_search"))
    
    # ========== انگلیسی ==========
    app.add_handler(CallbackQueryHandler(english_menu, pattern="english"))
    
    # ========== ساخت ربات ==========
    app.add_handler(CallbackQueryHandler(bot_builder_menu, pattern="build_bot"))
    
    # ========== پروفایل انیمه ==========
    app.add_handler(CallbackQueryHandler(profile_pics_menu, pattern="profile"))
    app.add_handler(CallbackQueryHandler(select_style, pattern="profile_style"))
    app.add_handler(CallbackQueryHandler(select_color, pattern="profile_color"))
    app.add_handler(CallbackQueryHandler(buy_profile_pics, pattern="buy_profile"))
    
    # ========== پرداخت ==========
    app.add_handler(CallbackQueryHandler(payment_menu, pattern="payment"))
    app.add_handler(CallbackQueryHandler(pay_manual, pattern="pay_manual"))
    app.add_handler(CallbackQueryHandler(manual_pay_amount, pattern="manual_pay_"))
    app.add_handler(CallbackQueryHandler(payment_guide, pattern="pay_guide"))
    app.add_handler(CallbackQueryHandler(payment_history, pattern="pay_history"))
    app.add_handler(CallbackQueryHandler(send_receipt_instruction, pattern="send_receipt"))
    app.add_handler(MessageHandler(filters.PHOTO, handle_payment_receipt))
    
    # ========== تبلیغات ==========
    app.add_handler(CallbackQueryHandler(ads_menu, pattern="ads"))
    app.add_handler(CallbackQueryHandler(send_ad_to_admin, pattern="send_ad"))
    app.add_handler(CallbackQueryHandler(confirm_ad, pattern="confirm_ad"))
    app.add_handler(CallbackQueryHandler(reject_ad, pattern="reject_ad"))
    
    # ========== خاطرات ==========
    app.add_handler(CallbackQueryHandler(show_memories, pattern="memories"))
    
    # ========== اضافه کردن به کانال ==========
    app.add_handler(CallbackQueryHandler(add_channel_menu, pattern="add_channel"))
    app.add_handler(CallbackQueryHandler(add_channel_new, pattern="add_channel_new"))
    app.add_handler(CallbackQueryHandler(delete_channel, pattern="delete_channel"))
    
    # ========== شبکه‌های اجتماعی ==========
    app.add_handler(CallbackQueryHandler(social_media_menu, pattern="social"))
    app.add_handler(CallbackQueryHandler(download_instagram, pattern="instagram"))
    app.add_handler(CallbackQueryHandler(download_youtube, pattern="youtube"))
    app.add_handler(CallbackQueryHandler(search_google, pattern="google"))
    
    # ========== مکالمه ساخت ربات ==========
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(build_new_bot, pattern="build_bot_start")],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, build_new_bot)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, build_new_bot)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv_handler)
    
    # ========== شروع ربات ==========
    logger.info("🌸 ملورینا با موفقیت روشن شد! 🥰")
    print("🤖 ملورینا با موفقیت روشن شد! 🥰")
    print("=" * 50)
    print("✨ قابلیت‌های فعال:")
    print("   ✅ چت با هوش مصنوعی (بدون تکرار)")
    print("   ✅ دکمه‌های شیشه‌ای کیوت")
    print("   ✅ ۴ شخصیت مختلف (عادی، شوخ، عاشقانه، خلاق)")
    print("   ✅ عضویت در کانال‌ها")
    print("   ✅ بازی سنگ کاغذ قیچی")
    print("   ✅ پروفایل انیمه از پینترست")
    print("   ✅ پرداخت دستی با شماره کارت")
    print("   ✅ پنل مدیریت ادمین")
    print("   ✅ اتصال به شبکه‌های اجتماعی")
    print("   ✅ خاطرات ملورینا")
    print("   ✅ تبلیغات")
    print("   ✅ مانگا و انگلیسی")
    print("=" * 50)
    print("🌸 برای شروع، ربات رو استارت کن! 🥰")
    print("=" * 50)
    
    app.run_polling()

if __name__ == "__main__":
    main()
