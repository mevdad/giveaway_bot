from aiogram import types
from aiogram.dispatcher import FSMContext

from app import dp
from keyboards import *
from database import GiveAway
from states import CreatedGivesStates


@dp.callback_query_handler(
    text=bt_admin_created_gives.callback_data,
    state='*'
)
async def show_created_gives(jam: types.CallbackQuery):
    markup = await GiveAway().get_keyboard_of_created_gives(
        user_id=jam.from_user.id
    )

    if markup:
        markup.add(bt_admin_cancel_action)

        await jam.message.edit_text(
            '💎  <b>Виберіть розіграш для перегляду:</b> ',
            reply_markup=markup
        )
        await CreatedGivesStates.select_give.set()

    else:
        await jam.answer('У вас немає створених розіграшів')


@dp.callback_query_handler(
    lambda c: c.data != bt_admin_cancel_action.callback_data,
    state=CreatedGivesStates.select_give,
)
async def show_selected_give(
    jam: types.CallbackQuery,
    state: FSMContext,
    give_callback_value: str = False
):
    await CreatedGivesStates.manage_selected_give.set()


    if not give_callback_value:
        give_callback_value = jam.data
    await state.update_data(give_callback_value=give_callback_value)


    give_data = await GiveAway().get_give_data(
        user_id=jam.from_user.id,
        callback_value=give_callback_value
    )

    message_text = ''
    for give in give_data:
        await state.update_data(type_of_give=give['type'])
        message_text = f'<b>Тип розіграшу:</b> <code>{"За коментарями" if give["type"] == "comments" else "За кнопкою"}</code>\n<b>Назва розіграшу:</b> <code>{give["name"]}</code>\n\n<b>Текст:</b>\n{give["text"]}\n\n<b>Фото:</b> <code>{"Ні" if give["photo_id"] is None else "Так"}</code>\n<b>Відео:</b> <code>{"Ні" if give["video_id"] is None else "Так"}</code>\n<b>Капча:</b> <code' \
                       f'>{"Так" if give["captcha"] else "Ні"}</code>\n<b>Кількість ' \
                       f'переможців:</b> <code' \
                       f'>{give["winners_count"]}</code>\n<b>Дата завершення:</b> <code>{give["over_date"]}</code>'


    await jam.message.edit_text(
        message_text,
        reply_markup=kb_admin_manage_created_gives
    )
