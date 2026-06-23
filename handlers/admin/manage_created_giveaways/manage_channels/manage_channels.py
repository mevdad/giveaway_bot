from aiogram import types
from aiogram.dispatcher import FSMContext

from app import bot, dp
from database import TelegramChannel
from states import CreatedGivesStates
from keyboards import *




@dp.callback_query_handler(
    text=[
        bt_admin_active_channels.callback_data,
        bt_admin_add_channel.callback_data
    ],
    state=CreatedGivesStates.manage_channels
)
async def manage_channels(
    jam: types.CallbackQuery,
    state: FSMContext
):
    callback = jam.data

    if callback == bt_admin_active_channels.callback_data:

        markup = await TelegramChannel().get_keyboard(
            owner_id=jam.from_user.id,
        )

        if markup:
            markup.add(bt_admin_cancel_action)

            await jam.message.edit_text(
                '💎  <b>Виберіть канал для перегляду:</b> ',
                reply_markup=markup
            )
            await CreatedGivesStates.select_connected_channel.set()


        else:
            await jam.answer('У вас немає підключених каналів')


    else:
        bot_data = await bot.get_me()

        await jam.message.edit_text(
            f'1) Додайте бота @{bot_data.username} на канал з правами: \n<code>- публікація повідомлень\n- редагування чужих публікацій</code>\n\n2) Перешліть репостом будь-яке повідомлення з каналу: ',
            reply_markup=kb_admin_cancel_action
        )
        await CreatedGivesStates.add_channel.set()
