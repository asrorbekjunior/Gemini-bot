from django.core.management.base import BaseCommand
from TelegramBot.main_handler import main  # Botni boshqaruvchi funksiyangiz

class Command(BaseCommand):
    help = 'Telegram botni ishga tushirish'

    def handle(self, *args, **kwargs):
        self.stdout.write('Telegram bot ishga tushirildi...')
        try:
            main()  # Bu yerdagi `main()` botni boshlash funksiyasi
        except KeyboardInterrupt:
            self.stdout.write('Bot to‘xtatildi.')
