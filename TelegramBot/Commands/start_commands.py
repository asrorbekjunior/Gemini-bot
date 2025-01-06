from telegram.ext import ContextTypes
from telegram import Update
from ..inline_keyboards import mainInline



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum Gemini botga xush kelibsiz!\nSavollaringizni menga yuboring")