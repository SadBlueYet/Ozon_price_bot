import asyncio
import logging
from parsing import check_choise
from aiogram import Bot, Dispatcher, types

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6411855014:Your token", parse_mode="HTML")
# Диспетчер
dp = Dispatcher(bot=bot)


# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user = message.from_user.first_name 
    await message.answer(f"Здравствуйте, {user}!\nЯ бот для отслеживания цен на маркетплейсе ozon!\n"
                         "Отправьте мне <u>ссылку</u> или <u>код</u> товара, и я начну следить за ценой и оповещу вас в случае ее изменения!")
    
    
@dp.message_handler()
async def echo(message: types.Message):
    user_message = message.text
    otv = await check_choise(user_message)
    await message.answer(otv)
    
# Запуск процесса поллинга новых апдейтов
async def main():
   
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())