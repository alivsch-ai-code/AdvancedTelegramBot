# core/handlers/image_handler.py
import os
import tempfile
from telebot.async_telebot import types
from md2tgmd import escape
from core.services import gemini_service

async def handle_image_messages(message: types.Message, bot):
    try:
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
            temp_image.write(downloaded_file)
            image_path = temp_image.name

        sent_msg = await bot.reply_to(message, "Bild empfangen! Warte auf Analyse...")

        user_id = str(message.from_user.id)
        gemini_response = await gemini_service.process_image_with_gemini(image_path, user_id)
        if gemini_response:
            await bot.edit_message_text(
                escape(gemini_response),
                chat_id=sent_msg.chat.id,
                message_id=sent_msg.message_id,
                parse_mode="MarkdownV2"
            )
        else:
            await bot.edit_message_text(
                "Fehler bei der Bildanalyse.",
                chat_id=sent_msg.chat.id,
                message_id=sent_msg.message_id
            )

        os.remove(image_path)
    except Exception as e:
        await bot.edit_message_text(
            f"Fehler: {str(e)}",
            chat_id=sent_msg.chat.id,
            message_id=sent_msg.message_id
        )