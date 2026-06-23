from app import bot
from database import GiveAway, TelegramChannel, TemporaryUsers
import json

async def delete_and_inform_of_the_end_give(
    give_callback_value: str,
    winners: list,
    summary_count_users: int,
):
    give_data = await GiveAway().filter(callback_value=give_callback_value).all().values(
        'owner_id',
        'name'
    )

    for give in give_data:

        if summary_count_users >= len(winners):

            text = f'🎁  <b>Розіграш завершено</b>\n\n<b>Назва:</b> {give["name"]}\n<b>Загальна кількість учасників:</b> {summary_count_users}\n\n<b>Переможці:</b>\n\n'
            for i in range(len(winners)):
                user_info = winners[i]
                text += f"{user_info['place']} місце - @{user_info['username']}"
                await bot.send_message(
                    chat_id=user_info["user_id"],
                    text=f'Вітаємо Ви виграли {user_info["place"]} місце в розіграші {give["name"]}. Для отримання призу звертайтесь до адміністратора. Ваші дані: {json.dumps(user_info)}'
                )
                if i < len(winners) - 1:
                    text += "\n"

            await bot.send_message(
                chat_id=give['owner_id'],
                text=text
            )

        else:
            await bot.send_message(
                chat_id=give['owner_id'],
                text=f'🎁  <b>Розіграш завершено</b>\n\n<b>Назва:</b> {give["name"]}\n<b>Не вдалося обрати переможців, учасників замало</b>'
            )

    await GiveAway().delete_give(callback_value=give_callback_value)
    await TemporaryUsers().filter(giveaway_callback_value=give_callback_value).delete()
