from aiogram import types
from aiogram.dispatcher import FSMContext

from app import bot, dp
from database import TelegramChannel
from keyboards import *
from states import CreatedGivesStates


@dp.callback_query_handler(
    text=bt_admin_add_group_for_channel.callback_data,
    state=CreatedGivesStates.show_connected_channel
)
async def add_new_group_for_channel(
        jam: types.CallbackQuery,
        state: FSMContext
):
    state_data = await state.get_data()

    bot_data = await bot.get_me()
    await jam.message.edit_text(
        f'1) Додайте бота @{bot_data.username} у групу каналу з правами: \n<code>- публікація повідомлень\n- редагування чужих повідомлень</code>\n\n2) Переслати репостом будь-яке повідомлення з групи: ',
        reply_markup=kb_admin_cancel_action
    )
    await CreatedGivesStates.add_group.set()


@dp.message_handler(
    state=CreatedGivesStates.add_group,
)
async def get_group_data(
    jam: types.Message,
    state: FSMContext
):
    try:

        group_data = jam.forward_from_chat

        if group_data.type == 'supergroup':

            member_info = await bot.get_chat_member(
                chat_id=group_data.id,
                user_id=bot.id
            )

            if member_info.status == 'administrator':
                state_data = await state.get_data()
                channel_callback_value = state_data['channel_callback_value']

                await TelegramChannel().filter(channel_callback_value=channel_callback_value).update(
                    group_id=group_data.id
                )

                await jam.answer(
                    '✅  <b>Група успішно додана</b>',
                    reply_markup=kb_admin_manage_channels
                )
                await CreatedGivesStates.manage_channels.set()


        else:
            await jam.answer(
                '🚫  <b>Це не група, спробуйте ще раз:</b> ',
                reply_markup=kb_admin_cancel_action
            )


    except Exception as error:
        await jam.answer(
            '🚫  <b>Помилка! Перевірте права бота і переслати репостом повідомлення з групи ще раз:</b> ',
            reply_markup=kb_admin_cancel_action
        )
