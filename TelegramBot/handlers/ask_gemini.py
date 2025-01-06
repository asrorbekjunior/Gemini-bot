from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import ContextTypes
import google.generativeai as genai
from telegram.helpers import escape_markdown
from DjangoBot.settings import API_KEY


genai.configure(api_key=API_KEY)

#
def ask_ai(prompt: str):
    """
    Google Generative AI API'dan ma'lumot olish.
    Sinxron metod orqali natijani qaytaradi.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model.generate_content(prompt, stream=True)

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Foydalanuvchi so'rovini API ga yuborib, javobni qaytaradi.
    """
    prompt = " ".join(update.message.text)
    msg = await update.message.reply_text("Javob olinmoqda...")

    try:
        # API orqali javob olish
        response = ask_ai(prompt)

        # Jonli tarzda javoblarni yuborish
        full_response = ""
        for chunk in response:
            full_response += chunk.text

            # Markdown formatni qochirish
            safe_text = escape_markdown(full_response, version=2)

            # Xabarni yangilashdan oldin mazmunni solishtirish
            if msg.text != safe_text:
                await msg.edit_text(safe_text, parse_mode=ParseMode.MARKDOWN_V2)

    except Exception as e:


        await msg.edit_text("Xatolik ro'y berdi\nQaytadan urining yoki biroz kuting", parse_mode=ParseMode.MARKDOWN_V2)
        await context.bot.send_message(chat_id=6194484795, text=f"Xatolik yuz berdi: {e}")
