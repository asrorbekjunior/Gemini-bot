from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters, CommandHandler
from ..models import TelegramUser
from ..inline_keyboards import admin_menu
from asgiref.sync import sync_to_async

async def start_add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("<b>Ho'sh kimni <u>admin</u> qilamiz uning telegram ID raqamini kiriting...</b>", parse_mode="HTML")
    return "Start_Add_admin"

async def end_add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.text
    try:
        int_id = int(user_id)
    except ValueError:
        await update.message.reply_text("<b>ID raqam bo'lishi kerak. Qaytadan urinib ko'ring.</b>", parse_mode="HTML")
        return "Start_Add_admin"

    # Django ORM so'rovini asinxron holga o'tkazamiz
    user = await sync_to_async(TelegramUser.objects.filter(user_id=int_id).first)()
    if user:
        await sync_to_async(TelegramUser.make_admin)(int_id)
        await update.message.reply_text(
            f"<b><a href='tg://user?id={int_id}'>{user.first_name}</a> botga administrator bo'ldi👌</b>\n\n<blockquote>Admin menu</blockquote>",
            parse_mode="HTML",
            reply_markup=admin_menu()
        )
        await context.bot.send_message(chat_id=int_id, text="<b>🥳Tabariklayman siz Admin maqomiga ega bo'ldingiz</b>", parse_mode="HTML")
    else:
        await update.message.reply_text(
            f"<b><u>{int_id}</u> raqamli foydalanuvchi topilmadi.\nIDni tekshirib qaytadan kiritng.</b>",
            parse_mode="HTML"
        )
        return "Start_Add_admin"

    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user
    context.bot.send_message(chat_id=user_id, text="Jarayon bekor qilindi.")
    return ConversationHandler.END

def add_admin_handlers():
    handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_add_admin, pattern="add_admin")],
        states={
            "Start_Add_admin": [MessageHandler(filters.TEXT & ~filters.COMMAND, end_add_admin)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return handler