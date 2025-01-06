from telegram import Update
from telegram.ext import ContextTypes
from ..inline_keyboards import admin_menu


async def Admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Admin menu",
        reply_markup=admin_menu()
    )