import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7250987821:AAH6K0nJr5IT0aRNUMdwvvPjqTcDn5vrhk4"  # Вставь свой токен
ADMIN_ID = 326929052  # Твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список игроков (ID и имя)
players = {}

# Инлайн-клавиатура с кнопками
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Вступить и не ссать", callback_data="join")],
        [InlineKeyboardButton(text="🎮 Записаться на игру", callback_data="register")],
        [InlineKeyboardButton(text="📋 Список участников", callback_data="players")],
        [InlineKeyboardButton(text="⚔ Разделение команд", callback_data="teams")],
        [InlineKeyboardButton(text="🚪 Выйти из списка", callback_data="leave")]
    ]
)

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать! Выбери действие:", reply_markup=inline_keyboard)

# Нажатие на инлайн-кнопку "Записаться на игру"
@dp.callback_query(lambda c: c.data == "register")
async def register_player(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.full_name

    if len(players) < 12:
        if user_id not in players:
            players[user_id] = user_name
            await bot.send_message(callback_query.from_user.id, f"✅ Вы записаны ({len(players)}/12)")
            
            if len(players) == 12:
                await bot.send_message(callback_query.from_user.id, "🔥 Лобби заполнено! Запись закрыта!")
        else:
            await bot.send_message(callback_query.from_user.id, "⚠️ Вы уже записаны!")
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Лобби заполнено!")

# Выход из списка
@dp.callback_query(lambda c: c.data == "leave")
async def leave_tournament(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id in players:
        del players[user_id]
        await bot.send_message(callback_query.from_user.id, "Вы вышли из списка.")
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Вас нет в списке.")

# Вывести список игроков
@dp.callback_query(lambda c: c.data == "players")
async def show_players(callback_query: types.CallbackQuery):
    if players:
        players_list = "\n".join(players.values())
        await bot.send_message(callback_query.from_user.id, f"📜 Список игроков:\n{players_list}")
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Пока никто не записался.")

# Таймер обратного отсчета
async def countdown_timer():
    while True:
        now = datetime.now()
        game_time = datetime(now.year, now.month, now.day, 21, 0)  # 21:00 МСК
        if now > game_time:
            game_time += timedelta(days=1)

        time_left = (game_time - now).total_seconds()

        if time_left > 0:
            await asyncio.sleep(time_left - 1800)  # 30 минут
            await notify_players("⏳ Осталось 30 минут до начала игры!")
            await asyncio.sleep(600)  # 20 минут
            await notify_players("⏳ Осталось 20 минут до начала игры!")
            await asyncio.sleep(600)  # 10 минут
            await notify_players("⏳ Осталось 10 минут до начала игры!")

# Рассылка уведомлений игрокам
async def notify_players(message: str):
    for user_id in players.keys():
        try:
            await bot.send_message(user_id, message)
        except Exception as e:
            print(f"Ошибка отправки {user_id}: {e}")

async def main():
    asyncio.create_task(countdown_timer())  # Запуск таймера
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
