# Discord Moondream Bot

A Discord bot that creates threaded conversations for users to interact with Moondream's AI image analysis API. This bot allows users to analyze images with various Moondream
capabilities (caption, query, detect, point) directly within Discord threads.

## Features

- Thread-based conversations for clean user interaction
- Direct integration with Moondream API via CURL-like requests
- Support for all Moondream endpoints (caption, query, detect, point)
- Raw API response display for transparency and debugging
- Simple command structure with or without prefixes (context-aware)
- Minimal dependencies for easier deployment

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token (from Discord Developer Portal)
- Moondream API Key (from console.moondream.ai)
- Administrator permissions on a Discord server

## Setup Guide

### 1. Create a Discord Application and Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name like "Moondream Bot"
3. Navigate to the "Bot" tab in the left sidebar and click "Add Bot"
4. Under the bot settings, enable the following Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent
5. Click "Reset Token" and copy your new bot token (save it securely for later)

### 2. Set Bot Permissions and Generate Invite URL

1. Still in the Discord Developer Portal, go to OAuth2 > URL Generator
2. Under "Scopes", select "bot"
3. Under "Bot Permissions", select the following permissions:
   - Read Messages/View Channels
   - Send Messages
   - Create Public Threads
   - Send Messages in Threads
   - Manage Threads
   - Attach Files
   - Read Message History
4. Copy the generated URL at the bottom of the page
5. Open the URL in your browser and select your server to invite the bot

### 3. Get a Moondream API Key

1. Go to [console.moondream.ai](https://console.moondream.ai)
2. Create an account or log in
3. Navigate to the API section and generate a new API key
4. Copy and save this API key securely

### 4. Set Up Your Development Environment

```bash
# Create a project directory
mkdir discord-moondream-bot
cd discord-moondream-bot

# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install required dependencies
pip install discord.py requests python-dotenv pillow
```

### 5. Create Project Files

Create a `.env` file in your project directory:

```
DISCORD_TOKEN=your_discord_bot_token_here
MOONDREAM_API_KEY=your_moondream_api_key_here
```

Create the `bot.py` file with the code provided in this repository.

### 6. Run the Bot

```bash
python bot.py
```

If everything is set up correctly, you should see:

```
Logged in as YourBotName (bot_id)
------
```

## Usage Guide

### Starting a Moondream Session

**Method 1: Interactive Mode**

```
!moondream
```

This will create a new thread where the bot will provide instructions on how to use it.

**Method 2: Direct Command**

```
!moondream caption
```

(with an attached image) This will create a thread and immediately process the image with the specified command.

### Commands Within Threads

Once inside a thread, you can use these commands without the `!moondream` prefix:

- `caption` - Generate a description of the attached image
- `query [question]` - Ask a question about the attached image
  - Example: `query What objects are in this image?`
- `detect [object]` - Detect specified objects in the attached image
  - Example: `detect person`
- `point [object]` - Point at specified objects in the attached image
  - Example: `point dog`

Always attach an image when using these commands.

## API Response Format

For each command, the bot will return:

1. A formatted response with the main information
2. The raw JSON response from Moondream API for transparency

Example:

```
Caption: A person sitting at a desk working on a computer.

Raw API Response:
{
  "caption": "A person sitting at a desk working on a computer.",
  "time_taken": 0.523
}
```

## Troubleshooting

### Bot Doesn't Respond

- Verify that all required intents are enabled in the Discord Developer Portal
- Check that your bot has proper permissions in your server
- Ensure the bot is online and check your console for error messages

### API Errors

- Verify your Moondream API key is correct
- Check that you're within your API usage limits
- Ensure the image format is supported (JPEG, PNG)

### Thread Creation Issues

- Ensure your bot has the "Create Public Threads" and "Manage Threads" permissions
- Some older Discord servers may have thread features limited

## Notes on Rate Limits

- Discord has rate limits on thread creation
- Moondream API may have rate limits based on your plan
- Consider adding retry logic for production use

## Additional Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Moondream API Documentation](https://docs.moondream.ai/)
- [Python Requests Library Documentation](https://docs.python-requests.org/)

## License

This project is provided as open source. Feel free to modify and use as needed.
