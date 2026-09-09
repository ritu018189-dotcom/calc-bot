# Environment variables

| Variable    | Required | Description                                                        |
|-------------|----------|----------------------------------------------------------------------|
| `BOT_TOKEN` | Yes      | Telegram bot token from [@BotFather](https://t.me/BotFather).       |

`main.py` calls `load_dotenv()` on startup, so a local `.env` file (copy it
from `.env.example`) is picked up automatically in development. In
production, set the variable through your host's environment/secrets
mechanism instead of shipping a `.env` file.
