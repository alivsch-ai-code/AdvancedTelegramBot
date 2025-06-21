# AdvancedChannelBot/main.py
# Hier wird der Bot gestartet (Inhalt identisch mit core/bot.py)
import argparse
import traceback
import asyncio
import google.generativeai as genai
import telebot
from telebot.async_telebot import AsyncTeleBot
from secrets_user import access_secrets  
from core.handlers import text_handler, image_handler

async def main():
    parser = argparse.ArgumentParser(description="Advanced Telegram Bot")
    args = parser.parse_args()

# Please configure your access tokens in the config/access_token.json file 
    api_key = access_secrets["GOOGLE_GEMINI_KEY"] # Changed from dot notation to square bracket notation
    tg_token = access_secrets["telegram_bot_token"]


    genai.configure(api_key=api_key)
    bot = AsyncTeleBot(tg_token)

    # Here you can define your bot commands and handlers
    await bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("example", "Example command)")
        ],
    )

    # Registering the command handlers for your setted commands
    bot.register_message_handler(
        lambda message, bot: bot.reply_to(message, "Huy, i am here to help you!"),
        commands=['example'],
        pass_bot=True
    )

    # Registering the query handler for a text query
    bot.register_message_handler(
        text_handler.handle_text_messages,
        content_types=['text'],
        pass_bot=True,
        func=lambda msg: not telebot.util.is_command(msg.text)
    )

    # Registering the query handler for a photo query
    bot.register_message_handler(
        image_handler.handle_image_messages,
        content_types=['photo'],
        pass_bot=True
    )
    # Setting up bot.polling for handling incoming messages
    await bot.polling(none_stop=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Beende Bot...")
    except Exception as e:
        traceback.print_exc()