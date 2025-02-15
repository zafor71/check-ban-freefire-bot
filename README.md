# Discord Bot Free Fire Info

## Description
This Discord bot provides detailed information about Free Fire players, checks their ban status, and retrieves data on guilds and guild leaders. It uses the RapidAPI API to fetch information and the official Free Fire API to verify bans.

## Features
- 🔍 **Get player information** via the `/get_info` command
- 🚨 **Check if a player is banned** via the `/check_ban` command
- 📜 **Display guild and leader details**
- 🌍 **Multi-region support**

## Installation
### Prerequisites
- Python 3.8+
- A registered Discord bot ([Create a bot here](https://discord.com/developers/applications))
- A RapidAPI account with a valid API key ([link](https://rapidapi.com/nazi436123/api/id-game-checker/))

### Installation Steps
1. **Clone the project**
   ```bash
   git clone https://github.com/paulafredo/check-ban-and-info-ff
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   Create a `.env` file and add:
   ```env
   APPLICATION_ID=your_application_id
   TOKEN=your_discord_token
   RAPIDAPI_KEY=your_rapidapi_key
   RAPIDAPI_HOST=your_rapidapi_host
   ```
4. **Run the bot**
   ```bash
   python bot.py
   ```

## Available Commands
| Command       | Description |
|--------------|-------------|
| `/get_info` `<UID>` | Get information about a Free Fire player |
| `/check_ban` `<UID>` | Check if a player is banned |

## Ban Check API Response Details
- **If the account is NOT banned:**
  ```json
  {
      "status": "success",
      "msg": "",
      "data": {
          "is_banned": 0,
          "period": 0
      }
  }
  ```
- **If the account is banned:**
  ```json
  {
      "status": "success",
      "msg": "",
      "data": {
          "is_banned": 1,
          "period": 1
      }
  }
  ```


## License
This project is licensed under the MIT License.

