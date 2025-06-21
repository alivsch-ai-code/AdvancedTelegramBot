Markdown

# AdvancedChannelBot

AdvancedChannelBot is a versatile Telegram bot designed to interact with users through text and image messages, leveraging the power of Google's Generative AI.

## About The Project

This bot is built to be easily extensible, providing a solid foundation for more advanced features. It's structured to handle different types of content and can be customized to fit various needs. The core of the bot uses the `pyTelegramBotAPI` library for interacting with the Telegram API and `google-generativeai` for intelligent responses.

### Features

* **Command Handling**: Responds to predefined commands (e.g., `/example`).
* **Text Message Processing**: Handles plain text messages for interactive chat.
* **Image Processing**: Can receive and process photo messages.
* **AI Integration**: Utilizes Google Gemini for advanced AI capabilities.
* **Asynchronous**: Built with `asyncio` for efficient, non-blocking operation.

Customization:

You have full control over how your bot behaves and responds!

Edit Bot's Role & Personality: In the config folder, open bot_role_settings.json. Here, you can easily define the bot's name, its core role, and even adjust its "kindness" (which can influence its tone, e.g., "criminal" for a more mischievous or bold persona).

JSON

{
  "name": "AZAMAT",
  "role": "Generiere die Antwort wie folgt: Du bist ein Bot, der drauf programmiert worden ist.",
  "kindness": "criminal"
}
Adjust AI Generation Settings: Also in the config folder, you'll find generation_config.json. This file lets you fine-tune the Gemini AI's output. For example, temperature controls randomness (lower for more focused, higher for more creative), top_p and top_k influence the diversity of generated tokens, and max_output_tokens limits the response length.

JSON

{
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 50
}

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

You need to have Python installed on your system. This project relies on several Python libraries. You can install them using pip:

```sh
pip install pyTelegramBotAPI google-generativeai
Installation
Clone the repo

Bash

git clone [https://github.com/your_username/AdvancedChannelBot.git](https://github.com/your_username/AdvancedChannelBot.git)
Navigate to the project directory

Bash

cd AdvancedChannelBot
Set up your API Keys
The bot requires API keys for both Telegram and Google Gemini. These are managed in a secrets_user.py file. Create this file in the root directory and add your keys as follows:

Python

# secrets_user.py
access_secrets = {
    "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "GOOGLE_GEMINI_KEY": "YOUR_GOOGLE_GEMINI_API_KEY"
}
You can get a Telegram Bot Token by talking to the BotFather.
You can obtain a Google Gemini API Key from the Google AI Studio.
Usage
Once the bot is configured, you can start it by running the main.py script:

Bash

python main.py
The bot will start polling for new messages. You can interact with it on Telegram:

Send /example: The bot will reply with a simple help message.
Send any text: The bot will process the text using the text_handler.
Send a photo: The bot will process the image using the image_handler.
Project Structure
AdvancedChannelBot/
│
├── core/
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── text_handler.py
│   │   └── image_handler.py
│   └── bot.py
│
├── main.py
└── secrets_user.py
main.py: The entry point for starting the bot.
core/: Contains the core logic of the bot.
handlers/: Modules for handling different message types.
text_handler.py: Logic for handling text messages.
image_handler.py: Logic for handling image messages.
secrets_user.py: (You must create this) Stores your secret API keys.
Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
Distributed under the MIT License. See LICENSE for more information.

Acknowledgments
pyTelegramBotAPI
google-generativeai-python