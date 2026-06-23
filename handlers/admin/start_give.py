from aiogram import types
from aiogram.dispatcher import FSMContext
from app import dp, bot
from keyboards import *
from states import CreatedGivesStates
from database import GiveAway, TelegramChannel, GiveAwayStatistic


@dp.callback_query_handler(
    text=bt_admin_start_give.callback_data,
    state=CreatedGivesStates.manage_selected_give
)
async def start_give(jam: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    give_callback_value = state_data['give_callback_value']

    give_model = GiveAway()
    channel_model = TelegramChannel()

    give_data = await give_model.get_give_data(
        user_id=jam.from_user.id,
        callback_value=give_callback_value
    )

    channel_data = await channel_model.get_channel_data(
        owner_id=jam.from_user.id
    )

    post_link = ''
    message_id = 0

    for give in give_data:
        message_text = f'{give["name"]}\n\n{give["text"]}\n\nКількість переможців: {give["winners_count"]}\nДата завершення: {give["over_date"].strftime("%d.%m.%Y %H:%M")}'

        if channel_data:

            bot_data = await bot.get_me()
            markup = InlineKeyboardMarkup()

            markup.add(
                InlineKeyboardButton(
                    text='Підтверджую, що досяг 21 року',
                    url=f'https://t.me/{bot_data.username}?start={give_callback_value}'
                )
            )

            for channel in channel_data:

                if give["type"] == 'comments':
                    if not bool(channel['group_id']):
                        await jam.answer('У вас немає підключених груп до каналів')
                        return


                message = ''
                if give["photo_id"] is None and give["video_id"] is None:
                    message = await bot.send_message(
                        chat_id=channel['channel_id'],
                        text=message_text,
                        reply_markup=markup if give["type"] == 'button' else None
                    )

                elif give["photo_id"]:
                    message = await bot.send_photo(
                        chat_id=channel['channel_id'],
                        photo=give["photo_id"],
                        caption=message_text,
                        reply_markup=markup if give["type"] == 'button' else None
                    )

                elif give["video_id"]:
                    message = await bot.send_video(
                        chat_id=channel['channel_id'],
                        video=give["video_id"],
                        caption=message_text,
                        reply_markup=markup if give["type"] == 'button' else None
                    )


                post_link = await message.chat.get_url() + '/' + str(message.message_id)
                message_id = message.message_id





        else:
            await jam.answer('У вас немає підключених каналів')
            return


    await TelegramChannel().filter(give_callback_value=give_callback_value).update(post_id=message_id)

    await GiveAwayStatistic().add_statistic(
        giveaway_callback_value=give_callback_value,
        members=[],
        winners=[],
        post_link=post_link
    )

    await give_model.update_give_status(
        callback_value=give_callback_value,
        status=True
    )

    await jam.message.edit_text(
        '<b> Розіграш успішно запущено</b> ✅',
        reply_markup=kb_admin_menu
    )
    await state.finish()
