import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7250987821:AAH6K0nJr5IT0aRNUMdwvvPjqTcDn5vrhk4"  # Замени на свой токен
ADMIN_ID = 326929052  # Твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список игроков
players = []

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 Вступить и не ссать")],
        [KeyboardButton(text="🎮 Записаться на игру")],
        [KeyboardButton(text="📋 Список участников")],
        [KeyboardButton(text="⚔ Разделение команд")],
        [KeyboardButton(text="🚪 Выйти из списка")]
    ],
    resize_keyboard=True  # Компактные кнопки
)

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать! Выбери действие:", reply_markup=keyboard)

# Кнопка "Вступить и не ссать"
@dp.message(lambda message: message.text == "🔥 Вступить и не ссать")
async def join_ready(message: types.Message):
    await message.answer("Красавчик! Теперь нажми - 'Записаться на игру'")

# Кнопка "Записаться на игру" и команда /join
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

# Кнопка "Список участников"
@dp.message(lambda message: message.text == "📋 Список участников")
async def list_players(message: types.Message):
    if players:
        await message.answer("📜 Список игроков:\n" + "\n".join(players))
    else:
        await message.answer("❌ Пока никто не записался.")

# Кнопка "🚪 Выйти из списка"
@dp.message(lambda message: message.text == "🚪 Выйти из списка")
async def leave_tournament(message: types.Message):
    if message.from_user.full_name in players:
        players.remove(message.from_user.full_name)
        await message.answer("Зассал? 😏 Ждем тебя в другой раз!")
    else:
        await message.answer("❌ Вас нет в списке.")

# Кнопка "Разделение команд" (заглушка, пока без логики)
@dp.message(lambda message: message.text == "⚔ Разделение команд")
async def teams_division(message: types.Message):
    await message.answer("⚔ Функция разделения команд в разработке!")

# Админ-команда /reset (сброс списка игроков)
@dp.message(Command("reset"))
async def reset_players(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        global players
        players = []
        await message.answer("🔄 Список участников очищен!")
    else:
        await message.answer("⛔ У вас нет прав использовать эту команду.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
