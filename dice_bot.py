import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [['🎲 Бросить кубик']]
    await update.message.reply_text(
        "Привет! Давай сыграем в кубики. Нажми кнопку 👇",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)

    text = (
        f"Ты бросил: 🎲 {user_roll}\n"
        f"Я бросил: 🤖 {bot_roll}\n\n"
    )

    if user_roll > bot_roll:
        text += "🎉 Ты победил!"
    elif user_roll < bot_roll:
        text += "😈 Я победил!"
    else:
        text += "😐 Ничья!"

    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Text(["🎲 Бросить кубик"]), roll_dice))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
