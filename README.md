Markdown

# AdvancedChannelBot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Intelligent Telegram Bot powered by Google Gemini AI 🌟

AdvancedChannelBot is a versatile and intelligent Telegram bot designed to interact with users through a rich set of features, leveraging the cutting-edge capabilities of **Google's Gemini AI**. This bot brings multimodal communication (text, voice, images) and real-time information directly into your Telegram chats, all while being easily customizable and deployable.

## ✨ About The Project

This project provides a robust and extensible foundation for building a highly interactive Telegram bot. It's structured for clear separation of concerns, making it easy to understand, maintain, and expand with new functionalities. The core communication is handled by `pyTelegramBotAPI`, while `google-generativeai` powers the advanced AI features.

### Key Features

* **Intelligent Conversations**: Engage in natural, context-aware dialogues thanks to the powerful **Google Gemini AI**.
* **Multimodal Interaction**: Processes and responds to both **text messages** and **voice messages**. It can also **analyze and describe uploaded images**.
* **Image Generation**: Request the bot to **generate creative images** based on your text prompts (functionality depends on the specific Gemini model's capabilities and API access).
* **Real-time Market Data**: Get instant updates on **stock prices** and **cryptocurrency values**.
* **Hourly News Briefs**: Stay informed with periodic news summaries delivered directly to your chat.
* **Customizable Persona & Responses**: Tailor the bot's personality, tone, and specific response styles.
* **Dynamic Model Switching**: Flexibly switch between different Gemini models (e.g., `gemini-2.0-flash-exp` and `gemini-1.5-pro`) for varied performance.
* **User-Specific Logging & Summaries**: All user interactions are logged individually, summarized daily, and retained for a configurable period, providing insights into bot usage.
* **Asynchronous Operations**: Built with `asyncio` for efficient, non-blocking performance, ensuring a smooth user experience.

### 🛠️ Customization

You have full control over how your bot behaves, its personality, and how it fine-tunes AI responses!

* **Bot's Role & Personality:**
    In the `config` folder, open `bot_role_settings.json`. Here, you can define the bot's name, its core role, and even adjust its "kindness" to influence its tone (e.g., "criminal" for a more mischievous or bold persona).

    ```json
    {
      "name": "AZAMAT",
      "role": "Generiere die Antwort wie folgt: Du bist ein Bot, der drauf programmiert worden ist.",
      "kindness": "criminal"
    }
    ```

* **AI Generation Settings:**
    Also in the `config` folder, you'll find `generation_config.json`. This file lets you fine-tune the Gemini AI's output. Parameters like `temperature` control randomness (lower for more focused, higher for more creative), `top_p` and `top_k` influence the diversity of generated tokens, and `max_output_tokens` limits the response length.

    ```json
    {
      "temperature": 0,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 50
    }
    ```

## 🚀 Getting Started

Follow these simple steps to get a local copy of the bot up and running.

### Prerequisites

Ensure you have the following installed on your system:

* **Python 3.9+**: The project is developed with recent Python versions.
* **pip**: Python's package installer.
* **ffmpeg**: Required for processing voice messages.
    * **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.
    * **Linux (Debian/Ubuntu):** `sudo apt-get install ffmpeg`
    * **macOS (Homebrew):** `brew install ffmpeg`
* **Docker Desktop (recommended for Windows/macOS)**: For easy containerized deployment.

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/your_username/AdvancedChannelBot.git](https://github.com/your_username/AdvancedChannelBot.git)
    ```

2.  **Navigate to the Project Directory:**

    ```bash
    cd AdvancedChannelBot
    ```

3.  **Set up Python Virtual Environment (Recommended):**

    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On Linux/macOS:
    source ./.venv/bin/activate
    ```

4.  **Install Python Libraries:**

    ```bash
    pip install -r requirements.txt
    ```
    *A `requirements.txt` file (to be created by you based on your `pyproject.toml` dependencies, or using `pip freeze > requirements.txt` after installing) should include:*
    `pyTelegramBotAPI`
    `google-generativeai`
    `yfinance`
    `requests`
    `beautifulsoup4`
    `md2tgmd`
    `vosk`
    `Pillow`

5.  **Configure Vosk Speech Recognition Model (within Dockerfile or manually if not using Docker):**
    The bot uses the Vosk German model for voice message processing. This is typically handled during the Docker build process if using the provided Docker setup. If running locally without Docker, ensure this model is downloaded and correctly placed:

    ```bash
    # (Inside your project root, e.g., in a 'data' directory)
    mkdir -p data/vosk-model-de-0.21
    # Download the model (e.g., using wget or curl)
    wget [https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) -P data/
    # Unzip the model
    unzip data/vosk-model-de-0.21.zip -d data/
    # Remove the zip file
    rm data/vosk-model-de-0.21.zip
    ```

6.  **Set up your API Keys:**
    The bot requires API keys for both Telegram and Google Gemini. These are managed in a `secrets_user.py` file. Create this file in the **root directory** of your project and add your keys as follows:

    ```python
    # secrets_user.py
    access_secrets = {
        "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
        "GOOGLE_GEMINI_KEY": "YOUR_GOOGLE_GEMINI_API_KEY"
    }
    ```
    * You can get a **Telegram Bot Token** by talking to the official `@BotFather` on Telegram.
    * You can obtain a **Google Gemini API Key** from the [Google AI Studio](https://aistudio.google.com/app/apikey).

### ▶️ Usage

Once the bot is configured, you can start it by running the `main.py` script:

```bash
python main.py
The bot will start polling for new messages. You can interact with it on Telegram using the following types of messages and commands:

/start: Initiates a conversation and gets a welcome message from Azamat.
/switch: Toggles between the primary and alternative Gemini models.
Text Messages: Send any text for intelligent replies.
Voice Messages: Send a voice note, and the bot will transcribe and respond.
Photos: Send a photo for the bot to analyze and describe.
Stock/Crypto Queries: Type a stock ticker (e.g., AAPL) or cryptocurrency keyword (e.g., Bitcoin price) to get current market data.
Image Generation Requests: Use prompts like "Gen Pic [your description]" (e.g., Gen Pic a cute cat playing with yarn) to generate images.
📁 Project Structure
AdvancedChannelBot/
├── core/
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── command_handler.py   # Handles specific bot commands like /start, /switch
│   │   ├── image_handler.py     # Logic for processing image messages
│   │   ├── query_handler.py     # Logic for handling stock/crypto and general queries
│   │   ├── text_handler.py      # Logic for handling general text messages
│   │   └── voice_handler.py     # Logic for handling voice messages
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py    # Interfaces with Google Gemini API for text, multimodal, and image generation
│   │   ├── news_service.py      # Fetches and sends hourly news updates
│   │   ├── openai_service.py    # (Optional) Placeholder for OpenAI integration
│   │   ├── deepseek_service.py  # (Optional) Placeholder for DeepSeek integration
│   │   ├── qwen_service.py      # (Optional) Placeholder for QWen integration
│   │   └── vosk_service.py      # Handles Vosk speech-to-text processing (if separated)
│   └── bot.py                   # Main bot initialization and handler registration (might be merged into main.py)
│
├── config/
│   ├── __init__.py              # Package initializer, can hold global config
│   ├── bot_role_settings.json   # JSON file for bot's persona customization
│   ├── config.py                # Main configuration dictionary (e.g., `conf`)
│   └── generation_config.py     # AI generation parameters (e.g., temperature, top_k)
│
├── data/                        # Directory for storing data (e.g., Vosk models)
│   └── vosk-model-de-0.21/      # Vosk German speech recognition model files
│
├── logs/                        # Directory for user-specific interaction logs
├── summaries/                   # Directory for daily log summaries
├── .dockerignore                # Specifies files/folders to ignore when building Docker images
├── Dockerfile                   # Dockerfile for building the bot's Docker image
├── docker-compose.yml           # Docker Compose file for easy multi-service deployment
├── main.py                      # The primary entry point for starting the bot
├── requirements.txt             # Python dependencies
├── secrets_user.py              # (You must create this) Stores your sensitive API keys
└── README.md                    # This README file
🙏 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. Don't forget to give the project a star! Thanks again!

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
📄 License
Distributed under the MIT License. See LICENSE for more information.

💖 Acknowledgments
pyTelegramBotAPI
google-generativeai-python
yfinance
requests
BeautifulSoup4
md2tgmd
Vosk
Pillow