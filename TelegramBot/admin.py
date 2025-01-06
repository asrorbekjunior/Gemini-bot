from django.contrib import admin
from .models import TelegramUser, PagesRead, BooksRead

# TelegramUser modeli uchun admin paneli
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'username', 'is_admin', 'date_joined')
    search_fields = ('first_name', 'username')
    list_filter = ('is_admin', 'date_joined')
    ordering = ('-date_joined',)
    
admin.site.register(TelegramUser, TelegramUserAdmin)


# PagesRead modeli uchun admin paneli
class PagesReadAdmin(admin.ModelAdmin):
    list_display = ('user', 'pages_read')
    search_fields = ('user__first_name', 'user__username')

admin.site.register(PagesRead, PagesReadAdmin)


# BooksRead modeli uchun admin paneli
class BooksReadAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_title', 'pages_read', 'date_read')
    search_fields = ('user__first_name', 'user__username', 'book_title')
    list_filter = ('date_read',)
    ordering = ('-date_read',)

admin.site.register(BooksRead, BooksReadAdmin)
