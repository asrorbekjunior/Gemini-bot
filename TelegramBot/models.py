from django.utils.timezone import now, timedelta
from django.db import models, transaction
from django.db.models import Count, Sum
from time import sleep
from telegram import Bot
from telegram.error import TelegramError


class TelegramUser(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ]

    user_id = models.BigIntegerField(unique=True, verbose_name="Telegram User ID")
    first_name = models.CharField(max_length=256, blank=True, null=True, verbose_name="First Name")
    username = models.CharField(max_length=256, blank=True, null=True, verbose_name="Username")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date Joined")
    last_active = models.DateTimeField(auto_now=True, verbose_name="Last Active")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="User Status"
    )
    is_admin = models.BooleanField(default=False, verbose_name="Is Admin")
    is_active = models.BooleanField(default=False, verbose_name="Is Active")

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
        ordering = ['-last_active']

    def __str__(self):
        return f"{self.first_name} (@{self.username})" if self.username else f"{self.user_id}"

    @classmethod
    def get_admin_ids(cls):
        """
        Admin bo'lgan userlarning IDlarini qaytaradi.
        """
        return list(cls.objects.filter(is_admin=True).values_list('user_id', flat=True))

    @classmethod
    def get_active_user_ids(cls):
        """
        Statusi "active" bo'lgan userlarning IDlarini qaytaradi.
        """
        return list(cls.objects.filter(status='active').values_list('user_id', flat=True))

    @classmethod
    def get_today_new_users(cls):
        """
        Bugungi yangi foydalanuvchilarni qaytaradi.
        """
        today = now().date()
        return cls.objects.filter(date_joined__date=today)

    @classmethod
    def get_daily_new_users(cls):
        """
        Har bir kun uchun yangi foydalanuvchilar sonini qaytaradi.
        """
        return cls.objects.values('date_joined__date').annotate(count=Count('id')).order_by('-date_joined__date')

    @classmethod
    def get_total_users(cls):
        """
        Umumiy foydalanuvchilar sonini qaytaradi.
        """
        return cls.objects.count()

    @classmethod
    def count_active_users(cls):
        """
        Statusi 'active' bo'lgan foydalanuvchilar sonini qaytaradi.
        """
        return cls.objects.filter(is_active=True).count()

    @classmethod
    def count_admin_users(cls):
        """
        Admin bo'lgan foydalanuvchilar sonini qaytaradi.
        """
        return cls.objects.filter(is_admin=True).count()

    @classmethod
    @transaction.atomic
    def find_and_inactive_users(cls, bot_token):
        """
        Nofaol foydalanuvchilarni aniqlab, ularning statusini 'blocked' ga o'zgartiradi.
        :param bot_token: Telegram bot tokeni
        :return: Noafaol foydalanuvchilar soni
        """
        bot = Bot(token=bot_token)
        blocked_users_count = 0

        for user in cls.objects.all():
            try:
                # Foydalanuvchiga chat action yuborish
                bot.send_chat_action(chat_id=user.user_id, action="typing")
                sleep(0.1)  # Telegram API cheklovlarini e'tiborga olish
            except TelegramError as e:
                # Faqat botni bloklaganlar uchun statusni yangilash
                if "bot was blocked by the user" in str(e) or "user is deactivated" in str(e):
                    user.is_active = False
                    user.save(update_fields=['is_active'])
                    inactive_users_count += 1
                else:
                    # Boshqa xatoliklar uchun log yaratish
                    print(f"Error for user {user.user_id}: {e}")

        return inactive_users_count
    @classmethod
    @transaction.atomic
    def make_admin(cls, user_id):
        """
        Userni admin qiladi.
        :param user_id: Admin qilinadigan foydalanuvchining Telegram user_id-si
        :return: Yangilangan user obyekti yoki None (user topilmasa)
        """
        try:
            user = cls.objects.get(user_id=user_id)
            user.is_admin = True
            user.save(update_fields=['is_admin'])
            return user
        except cls.DoesNotExist:
            print(f"User with ID {user_id} does not exist.")
            return None

    @classmethod
    @transaction.atomic
    def remove_admin(cls, user_id):
        """
        Userni adminlikdan chiqaradi.
        :param user_id: Adminlikdan chiqariladigan foydalanuvchining Telegram user_id-si
        :return: Yangilangan user obyekti yoki None (user topilmasa)
        """
        try:
            user = cls.objects.get(user_id=user_id)
            user.is_admin = False
            user.save(update_fields=['is_admin'])
            return user
        except cls.DoesNotExist:
            print(f"User with ID {user_id} does not exist.")
            return None

class PagesRead(models.Model):
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="daily_pages",
        verbose_name="User"
    )
    date = models.DateField(verbose_name="Date", default=now)
    pages_read = models.IntegerField(verbose_name="Pages Read", default=0)

    class Meta:
        verbose_name = "Daily Pages Read"
        verbose_name_plural = "Daily Pages Read"
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.first_name} - {self.date}: {self.pages_read} pages"

    @classmethod
    def add_pages(cls, user, pages):
        """
        Foydalanuvchining bugungi o'qigan sahifalari sonini qo'shadi.
        :param user: TelegramUser modeli obyekti
        :param pages: O'qilgan sahifalar soni
        """
        entry, created = cls.objects.get_or_create(user=user, date=now().date())
        entry.pages_read += pages
        entry.save(update_fields=['pages_read'])

    @classmethod
    def get_user_daily_pages(cls, user_id):
        """
        Foydalanuvchining har kuni o'qigan sahifalarini qaytaradi.
        :param user_id: TelegramUser user_id
        :return: Sahifalar ro'yxati
        """
        return cls.objects.filter(user__user_id=user_id).order_by('-date')

    @classmethod
    def get_total_pages(cls, user_id):
        """
        Foydalanuvchining jami o'qigan sahifalarini qaytaradi.
        :param user_id: TelegramUser user_id
        :return: Jami sahifalar soni
        """
        return cls.objects.filter(user__user_id=user_id).aggregate(total=models.Sum('pages_read'))['total'] or 0

    @classmethod
    def get_top_readers_daily(cls, limit=10):
        """
        Bir kunda eng ko'p sahifa o'qigan foydalanuvchilarni qaytaradi.
        :param limit: Foydalanuvchilar soni
        :return: Foydalanuvchilar va o'qigan sahifalari ro'yxati
        """
        return cls.objects.filter(date=now().date()).order_by('-pages_read')[:limit]

    @classmethod
    def get_top_readers_weekly(cls, limit=10):
        """
        Bir haftada eng ko'p sahifa o'qigan foydalanuvchilarni qaytaradi.
        :param limit: Foydalanuvchilar soni
        :return: Foydalanuvchilar va jami o'qigan sahifalari
        """
        week_ago = now().date() - timedelta(days=7)
        return cls.objects.filter(date__gte=week_ago).values('user__first_name').annotate(total_pages=models.Sum('pages_read')).order_by('-total_pages')[:limit]

    @classmethod
    def get_user_stats(cls, user_id, period="daily"):
        """
        Foydalanuvchining bir kunda, bir haftada yoki bir oyda o'qigan sahifalarini hisoblaydi.
        :param user_id: TelegramUser user_id
        :param period: Period turi (daily, weekly, monthly)
        :return: O'qigan sahifalar soni
        """
        if period == "daily":
            return cls.objects.filter(user__user_id=user_id, date=now().date()).aggregate(total=models.Sum('pages_read'))['total'] or 0
        elif period == "weekly":
            week_ago = now().date() - timedelta(days=7)
            return cls.objects.filter(user__user_id=user_id, date__gte=week_ago).aggregate(total=models.Sum('pages_read'))['total'] or 0
        elif period == "monthly":
            month_ago = now().date() - timedelta(days=30)
            return cls.objects.filter(user__user_id=user_id, date__gte=month_ago).aggregate(total=models.Sum('pages_read'))['total'] or 0
        else:
            raise ValueError("Invalid period. Use 'daily', 'weekly', or 'monthly'.")

    @classmethod
    def get_top_users(cls, period="weekly", limit=10):
        """
        Eng ko'p o'qigan foydalanuvchilarni qaytaradi.
        :param period: Period turi (daily, weekly, monthly)
        :param limit: Foydalanuvchilar soni
        :return: Foydalanuvchilar va jami o'qigan sahifalari
        """
        if period == "daily":
            return cls.get_top_readers_daily(limit)
        elif period == "weekly":
            return cls.get_top_readers_weekly(limit)
        elif period == "monthly":
            month_ago = now().date() - timedelta(days=30)
            return cls.objects.filter(date__gte=month_ago).values('user__first_name').annotate(total_pages=models.Sum('pages_read')).order_by('-total_pages')[:limit]
        else:
            raise ValueError("Invalid period. Use 'daily', 'weekly', or 'monthly'.")




class BooksRead(models.Model):
    user = models.ForeignKey('TelegramUser', on_delete=models.CASCADE, verbose_name="User")
    book_title = models.CharField(max_length=256, verbose_name="Book Title")
    date_read = models.DateField(verbose_name="Date Read")
    pages_read = models.IntegerField(default=0, verbose_name="Pages Read")

    @classmethod
    def add_book(cls, user, book_title, pages_read):
        today = now().date()
        cls.objects.create(user=user, book_title=book_title, pages_read=pages_read, date_read=today)

    @classmethod
    def get_total_books(cls):
        return cls.objects.count()

    @classmethod
    def get_user_books(cls, user):
        return cls.objects.filter(user=user).values('book_title', 'date_read', 'pages_read')

    @classmethod
    def get_user_books_in_period(cls, user, period='daily'):
        today = now().date()
        if period == 'daily':
            filter_date = today
        elif period == 'weekly':
            filter_date = today - timedelta(days=7)
        elif period == 'monthly':
            filter_date = today - timedelta(days=30)
        elif period == 'yearly':
            filter_date = today - timedelta(days=365)
        else:
            raise ValueError("Invalid period specified")

        return cls.objects.filter(user=user, date_read__gte=filter_date).aggregate(
            total_books=Count('id'), total_pages=Sum('pages_read')
        )

    @classmethod
    def get_books_in_period(cls, period='daily'):
        today = now().date()
        if period == 'daily':
            filter_date = today
        elif period == 'weekly':
            filter_date = today - timedelta(days=7)
        elif period == 'monthly':
            filter_date = today - timedelta(days=30)
        elif period == 'yearly':
            filter_date = today - timedelta(days=365)
        else:
            raise ValueError("Invalid period specified")

        return cls.objects.filter(date_read__gte=filter_date).values('user__id', 'user__username').annotate(
            total_books=Count('id'), total_pages=Sum('pages_read')
        ).order_by('-total_books')

    @classmethod
    def get_top_book_readers(cls, limit=10):
        return cls.objects.values('user__id', 'user__username').annotate(
            total_books=Count('id'), total_pages=Sum('pages_read')
        ).order_by('-total_books')[:limit]
