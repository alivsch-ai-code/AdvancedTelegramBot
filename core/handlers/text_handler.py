# core/handlers/text_handler.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.services import gemini_service
from telebot import types, TeleBot  # Ensure you import TeleBot if needed




async def handle_text_messages(message: types.Message, bot: TeleBot):
    """Handles text messages."""
    try:
        # Access user information from message
        user_id = message.from_user.id
        user_full_name = message.from_user.full_name
        text = message
    except Exception as e:
        print(f"Error handling text message: {e}")


    # # Beispiel: Auswahl des Modells basierend auf Benutzerbefehl oder Konfiguration
    # user_choice = conf.get("default_model", "gemini")  # Standardmäßig Gemini

    # if message.text == "/openai":
    #     user_choice = "openai"
    #     await context.send_message(chat_id=user_id, text="Wechsle zu OpenAI")
    # elif message.text == "/deepseek":
    #     user_choice = "deepseek"
    #     await context.send_message(chat_id=user_id, text="Wechsle zu DeepSeek")
    # elif message.text == "/qwen":
    #     user_choice = "qwen"
    #     await context.send_message(chat_id=user_id, text="Wechsle zu QWEN")
    # elif message.text == "/gemini":
    #     user_choice = "gemini"
    #     await context.send_message(chat_id=user_id, text="Wechsle zu Gemini")

    # # Generiere die Antwort basierend auf der Auswahl
    # if user_choice == "openai":
    #     response = await openai_service.generate_openai_response(message.text)
    # elif user_choice == "deepseek":
    #     response = await deepseek_service.generate_deepseek_response(message.text)
    # elif user_choice == "qwen":
    #     response = await qwen_service.generate_qwen_response(message.text)
    # else:  # Standardmäßig Gemini
    #     response = await gemini_service.send_text_message(user_id, message.text, str(message.from_user.full_name))
    
    
    
    response = await gemini_service.send_text_message(str(user_id), str(message.text), str(message.from_user.full_name))

        # Your message processing logic here
    await bot.reply_to(message, response)#f"Received: {text} from {user_full_name}")