from app import dp, bot
from config import OWNERS

@dp.errors_handler(
    exception=Exception
)
async def handle_bot_exceptions(
        update,
        error
):
    user_id = update['message']['from']['id']
    username = update['message']['from']['username']
    message_text = update['message']['text']

    for owner_id in OWNERS:
        await bot.send_message(
            chat_id=owner_id,
            text=f'<b>🚫  Виникла непередбачувана помилка</b>\n\nID користувача: {user_id}\nUsername користувача: {username}\n\nТекст повідомлення:\n<code>{message_text}</code>\n\nТекст помилки:\n<code>{error}</code>'
        )

    return True
