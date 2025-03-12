import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "ТВОЙ_ТОКЕН_БОТА"
ADMIN_ID = 326929052  # Твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список игроков
players = []

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔥 Вступить и не ссать"), KeyboardButton(text="🎮 Записаться на игру")],
        [KeyboardButton(text="📋 Список участников"), KeyboardButton(text="⚔ Разделение команд")],
        [KeyboardButton(text="🚪 Выйти из списка")]
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать! Выбери действие:", reply_markup=keyboard)

# Кнопка "Вступить и не ссать"
@dp.message(lambda message: message.text == "🔥 Вступить и не ссать")
async def join_welcome(message: types.Message):
    await message.answer("Красавчик! Теперь нажми - записаться на игру")

# Кнопка "Записаться на игру" и команда /join
@dp.message(lambda message: message.text == "🎮 Записаться на игру" or message.text == "/join")
async def join_tournament(message: types.Message):
    if len(players) < 12:
        if message.from_user.full_name not in players:
            players.append(message.from_user.full_name)
            await message.answer(f"✅ {message.from_user.full_name} записан! ({len(players)}/12)")
            
            if len(players) == 12:
                await bot.send_message(chat_id=message.chat.id, text="🔥 Лобби заполнено! Запись закрыта!")
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

# Кнопка "Выйти из списка"
@dp.message(lambda message: message.text == "🚪 Выйти из списка")
async def leave_tournament(message: types.Message):
    if message.from_user.full_name in players:
        players.remove(message.from_user.full_name)
        await message.answer("😢 Зассал? Ждем тебя в другой раз!")
    else:
        await message.answer("❌ Ты не был в списке!")

# Админ-команда /reset (сброс списка)
@dp.message(Command("reset"))
async def reset_players(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        global players
        players = []
        await message.answer("🔄 Список игроков сброшен!")
    else:
        await message.answer("🚫 У тебя нет прав на эту команду!")

# Таймер на напоминание о начале игры
async def countdown_timer():
    while True:
        now = datetime.datetime.now()
        game_time = datetime.datetime(now.year, now.month, now.day, 21, 0)  # 21:00 МСК
        time_left = (game_time - now).total_seconds()
        
        if 0 < time_left <= 1800:  # Если до игры меньше 30 минут
            for player in players:
                await bot.send_message(player, "⏳ До начала игры осталось 30 минут! Готовьтесь!")
                await asyncio.sleep(600)  # Повторять каждые 10 минут
        
        await asyncio.sleep(60)  # Проверять каждую минуту

async def main():
    asyncio.create_task(countdown_timer())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
