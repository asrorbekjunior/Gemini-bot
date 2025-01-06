from functools import wraps

from telegram import Update
from telegram.ext import CallbackContext

from .models import TelegramUser


def admin_required(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        # Admin check
        try:
            user = TelegramUser.objects.get(user_id=user_id)
            if not user.is_admin:
                context.bot.send_message(chat_ad=user_id, text="Siz admin emassiz!😠")
                return
        except TelegramUser.DoesNotExist:
            context.bot.send_message(chat_ad=user_id, text="Sizning ma'lumotlaringiz topilmadi.")
            return

        # if Admin, function call
        return func(update, context, *args, **kwargs)

    return wrapper
