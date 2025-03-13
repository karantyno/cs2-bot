import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7250987821:AAH6K0nJr5IT0aRNUMdwvvPjqTcDn5vrhk4"  # Вставь свой токен
ADMIN_ID = 326929052  # Твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

players = []

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 Вступить и не ссать")],
        [KeyboardButton(text="🎮 Записаться на игру")],
        [KeyboardButton(text="📋 Список участников")],
        [KeyboardButton(text="🚪 Выйти из списка")],
        [KeyboardButton(text="⚔ Разделение команд")],
        [KeyboardButton(text="🗑 Очистить список (только для админа)")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать! Выбери действие:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "🔥 Вступить и не ссать")
async def join_ready(message: types.Message):
    await message.answer("Красавчик! Теперь нажми - 'Записаться на игру'")

@dp.message(lambda message: message.text == "🎮 Записаться на игру")
async def join_tournament(message: types.Message):
    if len(players) < 12:
        if message.from_user.full_name not in players:
            players.append(message.from_user.full_name)
            await message.answer(f"✅ {message.from_user.full_name} записан! ({len(players)}/12)")
            if len(players) == 12:
                await message.answer("🔥 Лобби заполнено! Запись закрыта!")
        else:
            await message.answer("⚠️ Вы уже записаны!")
    else:
        await message.answer("❌ Лобби заполнено!")

@dp.message(lambda message: message.text == "📋 Список участников")
async def list_players(message: types.Message):
    if players:
        await message.answer("📜 Список игроков:\n" + "\n".join(players))
    else:
        await message.answer("❌ Пока никто не записался.")

@dp.message(lambda message: message.text == "🚪 Выйти из списка")
async def leave_tournament(message: types.Message):
    if message.from_user.full_name in players:
        players.remove(message.from_user.full_name)
        await message.answer("Зассал? 😏 Ждем тебя в другой раз!")
    else:
        await message.answer("❌ Вас нет в списке.")

@dp.message(lambda message: message.text == "⚔ Разделение команд")
async def teams_division(message: types.Message):
    await message.answer("⚔ Функция разделения команд в разработке!")

@dp.message(lambda message: message.text == "🗑 Очистить список (только для админа)")
async def reset_players(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        global players
        players = []
        await message.answer("🔄 Список участников очищен!")
    else:
        await message.answer("⛔ У вас нет прав использовать эту команду.")

async def countdown_timer():
    while True:
        now = datetime.now()
        game_time = datetime(now.year, now.month, now.day, 21, 0)
        if now > game_time:
            game_time += timedelta(days=1)
        time_left = (game_time - now).total_seconds()
        if time_left > 0:
            await asyncio.sleep(time_left - 1800)
            await notify_players("⏳ Осталось 30 минут до начала игры!")
            await asyncio.sleep(600)
            await notify_players("⏳ Осталось 20 минут до начала игры!")
            await asyncio.sleep(600)
            await notify_players("⏳ Осталось 10 минут до начала игры!")

async def notify_players(message: str):
    for player in players:
        try:
            await bot.send_message(player, message)
        except Exception as e:
            print(f"Ошибка отправки {player}: {e}")

async def main():
    asyncio.create_task(countdown_timer())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
