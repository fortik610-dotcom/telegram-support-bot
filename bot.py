import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

@dp.message(F.chat.type == "private")
async def forward_to_admin(message: Message):
    user = message.from_user

    text = (
        f"<b>Новое сообщение</b>\n\n"
        f"👤 Имя: {user.full_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"{message.text}"
    )

    sent = await bot.send_message(ADMIN_CHAT_ID, text)
    await sent.reply(f"<code>{user.id}</code>")

@dp.message(F.reply_to_message)
async def reply_to_user(message: Message):
    if message.chat.id != ADMIN_CHAT_ID:
        return

    replied_text = message.reply_to_message.text

    if replied_text and "<code>" in replied_text:
        user_id = int(replied_text.replace("<code>", "").replace("</code>", ""))

        await bot.send_message(
            user_id,
            f"📩 Ответ поддержки:\n\n{message.text}"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
