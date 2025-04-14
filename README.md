# 🔍 CheckBan Free Fire Discord Bot

![Status](https://img.shields.io/badge/status-active-brightgreen)

A Discord bot to check if a Free Fire account is banned, using a user ID. Also includes a Flask-based status server.

## 📚 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [License](#license)
- [Author](#author)

## 🚀 Features

- Check if a Free Fire account is banned using the `!ID <user_id>` command.
- Returns ban status and ban duration (if available) in an embedded Discord message.
- Flask web server on `http://localhost:10000` to indicate bot status.
- Secure credentials using `.env`.

## Requirements

- Python 3.8+
- A Discord bot token
- A `.env` file containing:
  ```ini
  APPLICATION_ID=your_application_id
  TOKEN=your_bot_token
  ```

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/paulafredo/check-ban-and-info-discord
   cd your-repo
   ```
2. Create environements:
   ```sh
   python -m venv .venv
   ```
   
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```



4. Create a `.env` file in the root directory and add your credentials:
   ```ini
   APPLICATION_ID=your_application_id
   TOKEN=your_bot_token
   ```

5. Run the bot:
   ```sh
   python main.py
   ```

## Usage

- Use `!ID <user_id>` in a Discord server where the bot is present.
- The bot will fetch ban information from [api-check-ban-freefire](https://github.com/paulafredo/api-check-ban-freefire) and respond with an embedded message.
- The bot's status can be checked via the Flask server running at `http://localhost:10000`.

## Technologies Used

- Python
- Discord.py
- Flask
- dotenv

## License

This project is licensed under the MIT License. Feel free to use and modify it.

## Author

[Paul Alfredo](https://github.com/paulafredo)

