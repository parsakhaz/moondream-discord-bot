# Moondream Discord Bot

A Discord bot that integrates with Moondream's Vision AI API to analyze images directly within Discord. Create dedicated image analysis threads, ask questions about images, get captions, detect objects, and more.

![Moondream Bot Demo](https://i.imgur.com/placeholder.png)

## Features

- **Multi-modal Image Analysis**: Analyze images using Moondream's powerful AI vision API
- **Thread-Based Conversations**: Each image analysis gets its own dedicated thread for a clean conversation flow
- **AI-Generated Thread Titles**: Dynamically names threads based on image content for better organization
- **Automatic Image Handling**: Images are preserved within threads even when original messages are deleted
- **Multiple Analysis Types**:
  - Image Captioning: Generate descriptive captions
  - Visual Question Answering: Ask any question about an image
  - Object Detection: Locate specific objects in images
  - Object Pointing: Get coordinates for specific objects
- **Shorthand Commands**: Use simplified commands like `!c`, `!q`, `!d`, and `!p` for faster interaction
- **Message Length Handling**: Automatically splits large responses to avoid Discord's message length limits
- **Visual Separators**: Clear visual separation between responses for better readability

## Requirements

- Python 3.8 or higher
- Discord Bot Token
- Moondream API Key
- Discord server with permission to add bots and create threads

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/moondream-discord-bot.git
cd moondream-discord-bot
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install discord.py requests python-dotenv Pillow
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following:

```
DISCORD_TOKEN=your_discord_bot_token_here
MOONDREAM_API_KEY=your_moondream_api_key_here
```

## Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and add a bot
3. Enable the following intents:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent
4. Generate an invite link with the following permissions:
   - Read Messages/View Channels
   - Send Messages
   - Create Public Threads
   - Send Messages in Threads
   - Manage Threads
   - Manage Messages (for deleting command messages)
   - Attach Files
   - Read Message History
Link: https://discord.com/oauth2/authorize?client_id=1344794705065672714&permissions=309237721088&integration_type=0&scope=bot
5. Invite the bot to your server using the generated link

## Starting the Bot

```bash
python bot.py
```

## Usage

### Starting an Image Analysis

1. In any channel where the bot has access, upload an image with one of these commands:
   ```
   !moondream
   !caption (or !c)
   !query <question> (or !q <question>)
   !detect <object> (or !d <object>)
   !point <object> (or !p <object>)
   ```

2. The bot will create a new thread dedicated to analyzing that image
3. The thread will be automatically named based on the image content (e.g., "Moondream: Liberty Leading the People" for a painting)

### Commands Inside Threads

Once in a thread, you can use these shorthand commands:

| Command | Description | Example |
|---------|-------------|---------|
| `!c` | Generate a caption for the image | `!c` |
| `!q <question>` | Ask a question about the image | `!q What colors are in this image?` |
| `!d <object>` | Detect specified objects | `!d face` |
| `!p <object>` | Point at specified objects | `!p eyes` |
| `!help` | Display detailed help information | `!help` |

### Example Workflow

1. User uploads image with `!c` in a channel
2. Bot creates a thread with an AI-generated name based on the image content
3. Bot posts the image caption in the thread
4. User asks `!q what is the subject wearing?` in the thread
5. Bot analyzes the same image and answers the question
6. User can continue with more commands in the same thread

## Thread Naming

The bot uses Moondream's AI to generate descriptive thread names:

- Initial threads are created with a temporary timestamp-based name
- The bot then queries the AI with "return a title for this image"
- Thread is renamed to "Moondream: [Generated Title]"
- If title generation fails, the original timestamp-based name is retained
- Titles are automatically shortened if they exceed Discord's 100-character limit

## Message Size Handling

For large API responses (especially with object detection), the bot automatically:
1. Separates formatted responses from raw JSON
2. Splits large JSON responses into multiple parts if needed
3. Labels each part (e.g., "Part 1/3") for clarity

## Advanced Configuration

Edit these values in `bot.py` to customize behavior:

```python
# Discord message size limits
DISCORD_REGULAR_MSG_LIMIT = 1900  # Setting slightly under the 2000 limit for safety
DISCORD_CODE_BLOCK_LIMIT = 1800  # Even smaller limit for code blocks due to backticks

# Bot command aliases (add more as needed)
COMMAND_ALIASES = {
    'caption': ['caption', 'c'],
    'query': ['query', 'q'],
    'detect': ['detect', 'd'],
    'point': ['point', 'p']
}
```

## Troubleshooting

### Bot Doesn't Respond
- Verify that all required intents are enabled in the Discord Developer Portal
- Check that your bot has the necessary permissions in your server
- Ensure your `.env` file contains valid tokens

### API Errors
- Check if your Moondream API key is valid
- Ensure you're within the API rate limits
- Verify that image formats are supported (JPG, PNG recommended)

### Thread Creation Issues
- Ensure the bot has "Create Public Threads" and "Manage Threads" permissions
- Some channels may have thread creation disabled by server settings

### Thread Naming Issues
- If threads aren't being renamed, check that the bot has "Manage Threads" permissions
- Very unusual images might not generate good titles; the bot will fall back to timestamp-based names
- Check API logs for any errors during title generation

### Command Not Working in Thread
- Make sure you're using the correct command format
- Check if the thread was created by the Moondream bot
- Verify that the thread has an associated image

## License

[MIT License](LICENSE)

## Credits

- [Moondream API](https://console.moondream.ai/) - Vision AI API
- [Discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper