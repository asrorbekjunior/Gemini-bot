from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def mainInline():
    keyboard = [
        [
            InlineKeyboardButton(text="Mening malumotlarim", callback_data='my_info'),
            InlineKeyboardButton(text="Hisobot yuborish", callback_data='send_report')
        ],
        [
            InlineKeyboardButton(text="O'qigan kitoblarim", callback_data='my_read_books'),
            InlineKeyboardButton(text="vizual ko'rinish", callback_data='vizual_view'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_menu():
    keyboard = [
        [
            InlineKeyboardButton(text="📊 Bot statistikasi", callback_data="BotStats"),
            InlineKeyboardButton(text="⚙️ Botni sozlash", callback_data="set_bot")
        ],
        [
            InlineKeyboardButton(text="Kanal sozlamalari", callback_data='set_channel'),
            InlineKeyboardButton(text="Admin sozlamalari", callback_data='set_admins')
        ],
        [
            InlineKeyboardButton(text="Xabar yuborish", callback_data='send_message')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def channelskeyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="📢 Kanal qo'shish", callback_data="add_channel"),
            InlineKeyboardButton(text="🔴 Kanal o'chirish", callback_data="delete_channel")
        ],
        [
            InlineKeyboardButton(text="Kanllar ro'yxati", callback_data='channels_list')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def adminskeyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="👮‍♂️ Admin qo'shish", callback_data='add_admin'),
            InlineKeyboardButton(text="🙅‍♂️ Admin o'chirish", callback_data='delete_channel')
        ],
        [
            InlineKeyboardButton(text="Adminlar ro'yxati", callback_data="admins_list")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)