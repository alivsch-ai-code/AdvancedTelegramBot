import asyncio
import base64
import google.generativeai as genai
from config import generation_config, safety_settings, bot_role_settings
from config.conf_model.model import conf
import logging
import os
import datetime

# ... (rest of your gemini_service.py code) ...

LOG_DIR = "LOGS/logs"  # Directory to store log files
SUMMARY_DIR = "LOGS/summaries"  # Directory to store daily summaries
LOG_RETENTION_DAYS = 7  # Number of days to keep summary logs

gemini_player_dict = {}
gemini_pro_player_dict = {}
default_model_dict = {}
model_1 = conf["model_1"]
model_2 = conf["model_2"]
n = conf["n"]

# Configure base logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def make_new_convo(model_name):
    def create_convo():
        return genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        ).start_chat()
    return await asyncio.to_thread(create_convo)

async def generate_multimodal_response(user_id: str, prompt: dict):
    model_type = default_model_dict.get(user_id, model_1)
    player_dict = gemini_pro_player_dict if model_type == model_2 else gemini_player_dict

    if user_id not in player_dict:
        player = await make_new_convo(model_type)
        player_dict[user_id] = player
    else:
        player = player_dict[user_id]

    if len(player.history) > n:
        player.history = player.history[-n:]

    loop = asyncio.get_running_loop()

    def generate():
        try:
            return player.model.generate_content(contents=prompt)
        except Exception as e:
            logging.error(f"Error generating multimodal response for user {user_id}: {e}")
            return None

    return await loop.run_in_executor(None, generate)


def get_user_log_path(user_id: str) -> str:
    os.makedirs(LOG_DIR, exist_ok=True)  # Ensure log directory exists
    return os.path.join(LOG_DIR, f"user_{user_id}.log")

def get_summary_log_path() -> str:
    os.makedirs(SUMMARY_DIR, exist_ok=True)  # Ensure summary directory exists
    today = datetime.date.today().strftime("%Y-%m-%d")
    return os.path.join(SUMMARY_DIR, f"summary_{today}.log")

def cleanup_old_summary_logs():
    """Deletes summary logs older than LOG_RETENTION_DAYS."""
    cutoff_date = datetime.date.today() - datetime.timedelta(days=LOG_RETENTION_DAYS)
    for filename in os.listdir(SUMMARY_DIR):
        try:
            date_str = filename.split("_")[1].split(".")[0]  # Extract date from filename
            file_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            if file_date < cutoff_date:
                os.remove(os.path.join(SUMMARY_DIR, filename))
                logging.info(f"Deleted old summary log: {filename}")
        except (IndexError, ValueError) as e:
            logging.warning(f"Could not parse date from filename: {filename}. Skipping. Error: {e}")

async def send_text_message(user_id: str, message_text: str, user_full_name: str) -> str | None:
    model_type = default_model_dict.get(user_id, model_1)
    player_dict = gemini_pro_player_dict if model_type == model_2 else gemini_player_dict
    bot_name= bot_role_settings["name"]
    bot_kindness = bot_role_settings["kindness"]
    bot_role = bot_role_settings["role"]

    try:
        if user_id not in player_dict:
            player = await make_new_convo(model_type)
            if player:  # Check if player was created successfully
                player_dict[user_id] = player
            else:
                logging.error(f"Failed to create new conversation for user {user_id}")
                return None  # Or raise an exception if appropriate
        else:
            player = player_dict[user_id]

        if len(player.history) > n:
            player.history = player.history[-n:]

        response = await asyncio.to_thread(
            player.send_message,
            f"Your are {bot_name}. You has the following role {bot_role} and you have to respond as {bot_kindness}. The User {user_full_name} has written following {message_text}. Please generate a answer!"
        )

        if response and hasattr(response, 'text') and response.text:  # Check response and its text attribute
            log_message = f"Request: {message_text}\nResponse: {response.text}\n"
            log_to_user_file(user_id, log_message)
            log_to_summary(user_id, message_text, response.text)
            return str(response.text)
        else:
            logging.warning(f"No valid response received from Gemini for user {user_id}")
            return None

    except Exception as e:
        logging.error(f"Error sending text message to user {user_id}: {e}")
        return None

async def send_voice_message(user_id: str, recognized_text: str, user_full_name: str) -> str | None:
    # ... (rest of your send_voice_message function) ...
    bot_name= bot_role_settings["name"]
    bot_kindness = bot_role_settings["kindness"]
    bot_role = bot_role_settings["role"]
    try:
        response = await asyncio.to_thread(
            player.send_message,
            f"Your are {bot_name}. You has the following role {bot_role} and you have to respond as {bot_kindness}. The User {user_full_name} has written following {recognized_text}. Please generate a answer!"
        )
        log_message = f"Voice Request: {recognized_text}\nResponse: {response.text}\n"
        log_to_user_file(user_id, log_message)
        log_to_summary(user_id, recognized_text, response.text)
        return response.text
    except Exception as e:
        logging.error(f"Error sending voice message to user {user_id}: {e}")
        return None

def log_to_user_file(user_id: str, log_message: str):
    """Logs request and response to a user-specific file."""
    log_path = get_user_log_path(user_id)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

def log_to_summary(user_id: str, request: str, response: str):
    """Logs a summary entry to the daily summary log."""
    summary_path = get_summary_log_path()
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    summary_entry = f"[{timestamp}] User {user_id}:\n  Request: {request}\n  Response: {response}\n"
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(summary_entry + "\n")

async def daily_summary_task():
    """Task to perform daily summary and log cleanup."""
    while True:
        now = datetime.datetime.now()
        next_run = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        await asyncio.sleep((next_run - now).total_seconds())  # Sleep until midnight

        logging.info("Performing daily log summary and cleanup...")
        summarize_user_logs()
        cleanup_old_summary_logs()
        logging.info("Daily log summary and cleanup completed.")

def summarize_user_logs():
    """Summarizes user logs for the day and appends to the summary log."""
    for filename in os.listdir(LOG_DIR):
        if filename.startswith("user_") and filename.endswith(".log"):
            user_id = filename.split("_")[1].split(".")[0]
            log_path = os.path.join(LOG_DIR, filename)
            summary_path = get_summary_log_path()

            try:
                with open(log_path, "r", encoding="utf-8") as infile, \
                        open(summary_path, "a", encoding="utf-8") as outfile:
                    outfile.write(f"\n--- Summary for User {user_id} ---\n")
                    outfile.write(infile.read())
                os.remove(log_path)  # Delete the user log after summary
                logging.info(f"Summarized and deleted user log: {filename}")
            except Exception as e:
                logging.error(f"Error summarizing user log {filename}: {e}")

async def process_image_with_gemini(image_path: str, user_id: str) -> str | None:
    bot_name= bot_role_settings["name"]
    bot_kindness = bot_role_settings["kindness"]
    bot_role = bot_role_settings["role"]
    try:
        
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
        prompt = {
            "parts": [
                {"text": "You have received this image. Please analyze it and provide a detailed description. Please respond as {bot_name} with the following role {bot_role} and respond as {bot_kindness}."},
                {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}
            ]
        }
        response = await generate_multimodal_response(user_id, prompt)
        if response and response.text:
            return response.text
        else:
            logging.warning(f"No text in multimodal response for user {user_id}")
            return None
    except Exception as e:
        logging.error(f"Error processing image for user {user_id}: {e}")
        return None