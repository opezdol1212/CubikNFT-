import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Кнопка
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("🎲 Бросить кубик"))

# Храним состояния (временно)
user_states = {}

@dp.message_handler(CommandStart())
async def start(msg: types.Message):
    await msg.answer("Привет! Нажми кнопку, чтобы сыграть в кубики 🎲", reply_markup=keyboard)

@dp.message_handler(lambda m: m.text == "🎲 Бросить кубик")
async def play_dice(msg: types.Message):
    user_id = msg.from_user.id
    await msg.answer("Мой ход... 🎲")

    # Бот кидает кубик
    bot_dice = await bot.send_dice(msg.chat.id, emoji="🎲")
    bot_value = bot_dice.dice.value

    user_states[user_id] = {
        "bot": bot_value,
        "waiting_user": True
    }

    await msg.answer("Теперь твой ход! Просто отправь 🎲 (встроенный кубик в Telegram)")

@dp.message_handler(content_types=types.ContentType.DICE)
async def user_dice(msg: types.Message):
    user_id = msg.from_user.id
    state = user_states.get(user_id)

    if not state or not state.get("waiting_user"):
        await msg.reply("Сначала нажми кнопку 🎲, чтобы начать игру.")
        return

    user_value = msg.dice.value
    bot_value = state["bot"]

    # Определим победителя
    if user_value > bot_value:
        result = "🎉 Ты победил!"
    elif user_value < bot_value:
        result = "😈 Я победил!"
    else:
        result = "🤝 Ничья!"

    await msg.answer(f"Результат:\nТы: {user_value} | Я: {bot_value}\n{result}")
    user_states[user_id]["waiting_user"] = False
