import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('TOKEN')
API_KEY = getenv('API_KEY')

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    headers = {'Authorization': f"Bearer {API_KEY}"}
    user_id = message.from_user.id
    student_payload = {"student_id": str(user_id), "notify": True}
    async with ClientSession() as session:
        async with session.post('https://api.bf60e757.nip.io/api/v1/student/', json=student_payload,
                                headers=headers) as response:
            if response.status == 200:
                reply = await response.json()
                await message.answer(f"Добро пожаловать!")
            elif response.status == 409:
                await message.answer(f"Добро пожаловать снова!")
            else:
                print(response)
                await message.answer("Ошибка: не удалось зарегистрироваться в очереди. Попробуйте позже.")


@dp.message(Command("queue"))
async def queue_command_handler(message: Message) -> None:
    headers = {'Authorization': f"Bearer {API_KEY}"}
    user_id = message.from_user.id
    queue_payload = {"student_id": str(user_id)}
    async with ClientSession() as session:
        async with session.post('https://api.bf60e757.nip.io/api/v1/queue/', json=queue_payload,
                                headers=headers) as queue_response:
            reply = await queue_response.json()
            async with session.get(f'https://api.bf60e757.nip.io/api/v1/queue/{reply}',
                                   headers=headers) as status_response:
                if queue_response.status == 200 and status_response.status == 200:
                    rep = await status_response.json()
                    await message.answer(f"Вы успешно добавлены в очередь. Ваша позиция: {rep.get('position')}")
                else:
                    await message.answer("Ошибка: не удалось добавить в очередь. Попробуйте позже.")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    asyncio.run(main())
