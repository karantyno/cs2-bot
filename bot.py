import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "ТВОЙ_ТОКЕН"  # Вставь свой токен

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список игроков
players = []

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 Вступить и не ссать"), KeyboardButton(text="🎮 Записаться на игру")],
        [KeyboardButton(text="📋 Список участников"), KeyboardButton(text="⚔ Разделение команд")]
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать! Выбери действие:", reply_markup=keyboard)

# Кнопка "Вступить и не ссать"
@dp.message(lambda message: message.text == "🔥 Вступить и не ссать")
async def join_game(message: types.Message):
    await message.answer("Красавчик! Теперь нажми - 'Записаться на игру'")

# Кнопка "Записаться на игру" и команда /join
@dp.message(lambda message: message.text == "🎮 Записаться на игру" or message.text == "/join")
async def join_tournament(message: types.Message):
    if len(players) < 12:
        if message.from_user.full_name not in players:
            players.append(message.from_user.full_name)
            await message.answer(f"✅ {message.from_user.full_name} записан! ({len(players)}/12)")
            
            # Автоуведомление, если лобби заполнено
            if len(players) == 12:
                for player in players:  # Отправляем сообщение каждому участнику
                    await bot.send_message(message.chat.id, "🔥 Лобби заполнено! Запись закрыта, готовьтесь к бою!")
        else:
            await message.answer("⚠️ Вы уже записаны!")
    else:
        await message.answer("❌ Лобби заполнено!")

# Кнопка "Список участников" и команда /players
@dp.message(lambda message: message.text == "📋 Список участников" or message.text == "/players")
async def list_players(message: types.Message):
    if players:
        await message.answer("📜 Список игроков:\n" + "\n".join(players))
    else:
        await message.answer("❌ Пока никто не записался.")

# Кнопка "Разделение команд" (заглушка, пока без логики)
@dp.message(lambda message: message.text == "⚔ Разделение команд")
async def teams_division(message: types.Message):
    await message.answer("⚔ Функция разделения команд в разработке!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
