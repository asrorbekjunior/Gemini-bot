from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from .Commands.start_commands import start
from .BotAdmin.add_admin import add_admin_handlers
from .BotAdmin.admin_menu import Admin_menu
from .handlers.Botstats import bot_stats
from .handlers.ask_gemini import ask
from DjangoBot.settings import BOT_TOKEN
import os
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAPI.settings')
django.setup()

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

def main():
    """Asosiy funksiyani yaratish"""
    # Tokenni o'z botingizdan oling
    app = Application.builder().token(BOT_TOKEN).build()

    # start komandasi uchun handler qo'shish
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(bot_stats, pattern="BotStats"))
    app.add_handler(add_admin_handlers())
    app.add_handler(CommandHandler('admin', Admin_menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))

    # Botni ishga tushurish
    app.run_polling()
    print("Bot is Stoppinng...")

if __name__=="__main__":
    main()