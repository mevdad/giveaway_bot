from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bt_admin_not_add_give_photo = InlineKeyboardButton('Ні', callback_data='admin_not_add_give_photo')
bt_admin_add_give_photo = InlineKeyboardButton('Так', callback_data='admin_add_give_photo')

kb_admin_add_give_photo = InlineKeyboardMarkup().add(bt_admin_not_add_give_photo, bt_admin_add_give_photo)