from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .cancel_action import bt_admin_cancel_action


bt_admin_edit_give_date = InlineKeyboardButton('« Редагувати дату', callback_data='admin_edit_give_date')
bt_admin_continue_create_give = InlineKeyboardButton('Продовжити »', callback_data='admin_continue_create_give')

kb_admin_edit_give_date = InlineKeyboardMarkup().add(bt_admin_edit_give_date, bt_admin_continue_create_give).add(bt_admin_cancel_action)
