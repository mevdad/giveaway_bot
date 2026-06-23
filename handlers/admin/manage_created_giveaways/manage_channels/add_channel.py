from aiogram import types
from aiogram.dispatcher import FSMContext

from app import bot, dp
from database import TelegramChannel
from states import CreatedGivesStates
from keyboards import *


@dp.message_handler(
    state=CreatedGivesStates.add_channel,
)
async def get_channel_data(
    jam: types.Message,
    state: FSMContext
):
    try:

        channel_data = jam.forward_from_chat

        if channel_data.type == 'channel':

            try:
                member_info = await bot.get_chat_member(
                    chat_id=channel_data.id,
                    user_id=bot.id
                )

                if member_info.status == 'administrator':
                    model = TelegramChannel()

                    if not await model.exists_channel(
                            channel_id=channel_data.id
                    ):

                        state_data = await state.get_data()

                        await model.add_channel(
                            owner_id=jam.from_user.id,
                            channel_id=channel_data.id,
                            give_callback_value=state_data['give_callback_value'],
                            name=channel_data.title
                        )

                        await jam.answer(
                            '✅  <b>Канал успішно доданий</b>',
                            reply_markup=kb_admin_manage_channels
                        )
                        await CreatedGivesStates.manage_channels.set()

                    else:
                        await jam.answer(
                            '🚫  <b>Даний канал вже доданий, спробуйте інший:</b> ',
                            reply_markup=kb_admin_cancel_action
                        )


                else:
                    await jam.answer(
                        '🚫  Помилка! </b>Перевірте права бота та переслати повідомлення з каналу знову:</b> ',
                        reply_markup=kb_admin_cancel_action
                    )


            except Exception as error:
                print(error)
                await jam.answer(
                    '🚫  <b>Помилка! Перевірте права бота та переслати повідомлення з каналу знову:</b> ',
                    reply_markup=kb_admin_cancel_action
                )


        else:
            await jam.answer(
                '🚫  <b>Це не канал, спробуйте ще раз:</b>',
                reply_markup=kb_admin_cancel_action
            )

    except AttributeError:
        await jam.answer(
            '🚫  <b>Це не канал, спробуйте ще раз:</b>',
            reply_markup=kb_admin_cancel_action
        )
