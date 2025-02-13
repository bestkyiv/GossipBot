# GossipBot
> Created by [@eltagun]

GossipBot is a Telegram bot designed to forward messages to a specified chat.

## Features

- Forward messages to a specified chat.
- Enable or disable message forwarding.
- Access control to restrict bot usage to specific users.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/GossipBot.git
    cd GossipBot
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your environment variables:
    ```env
    TELEGRAM_BOT_TOKEN=your_bot_token
    ACCESS_CHECK=true
    DEBUG=false
    LOCAL_CHAT_ID=-111111111
    STAGE_CHAT_ID=-111111111
    CORETEAM_PEOPLE=tag1,tag_2,tagThree
    ```

## Usage

1. Run the bot:
    ```sh
    python src/gossip_bot.py
    ```

2. Use the following commands in your Telegram chat:
    - `/start` - Start the bot.
    - `/help` - Get help information.
    - `/enable` - Enable message forwarding.
    - `/disable` - Disable message forwarding.

## Configuration

The bot can be configured using environment variables or the `.env` file.

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: The token for your Telegram bot.
- `ACCESS_CHECK`: Enable or disable access control.
- `DEBUG`: Enable or disable debug mode.
- `LOCAL_CHAT_ID`: The chat ID for the local testing.
- `STAGE_CHAT_ID`: The chat ID for the staging environment.
- `CORETEAM_PEOPLE`: Comma-separated list of usernames with access.

## Testing

Run the tests using `unittest`:
```sh
python -m unittest discover -s src
```
