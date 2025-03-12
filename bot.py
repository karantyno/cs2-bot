import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7250987821:AAH6K0nJr5IT0aRNUMdwvvPjqTcDn5vrhk4"  # Вставь свой токен
ADMIN_ID = 326929052  # Твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список игроков
players = []

# Клавиатура с кнопками
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Вступить и не ссать", callback_data="join")],
        [InlineKeyboardButton(text="🎮 Записаться на игру", callback_data="register")],
        [InlineKeyboardButton(text="📋 Список участников", callback_data="players")],
        [InlineKeyboardButton(text="⚔ Разделение команд", callback_data="teams")],
        [InlineKeyboardButton(text="🚪 Выйти из списка", callback_data="leave")]
    ]
)
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
@dp.message(lambda message: message.text == "🎮 Записаться на игру" or message.text == "/join")
async def join_tournament(message: types.Message):
    if len(players) < 12:
        if message.from_user.full_name not in players:
            players.append(message.from_user.full_name)
            await message.answer(f"✅ {message.from_user.full_name} записан! ({len(players)}/12)")
            
            # Автоуведомление, если лобби заполнено
            if len(players) == 12:
                await message.answer("🔥 Лобби заполнено! Запись закрыта!")
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

# Таймер обратного отсчета
async def countdown_timer():
    while True:
        now = datetime.now()
        game_time = datetime(now.year, now.month, now.day, 21, 0)  # 21:00 МСК

        # Если текущее время больше 21:00, значит, следующее уведомление завтра
        if now > game_time:
            game_time += timedelta(days=1)

        time_left = (game_time - now).total_seconds()

        # Отправлять уведомления за 30, 20 и 10 минут до игры
        if time_left > 0:
            await asyncio.sleep(time_left - 1800)  # Ждать до 30 минут до начала
            await notify_players("⏳ Осталось 30 минут до начала игры!")
            await asyncio.sleep(600)  # Ждать до 20 минут до начала
            await notify_players("⏳ Осталось 20 минут до начала игры!")
            await asyncio.sleep(600)  # Ждать до 10 минут до начала
            await notify_players("⏳ Осталось 10 минут до начала игры!")

# Рассылка уведомлений игрокам
async def notify_players(message: str):
    for player in players:
        try:
            await bot.send_message(player, message)
        except Exception as e:
            print(f"Ошибка отправки {player}: {e}")

async def main():
    asyncio.create_task(countdown_timer())  # Запуск таймера
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
