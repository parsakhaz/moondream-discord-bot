import discord
from discord.ext import commands
import requests
import base64
import json
import io
import os
from PIL import Image
from dotenv import load_dotenv
import datetime
import re
import math

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

# Moondream API configuration
API_BASE_URL = 'https://api.moondream.ai/v1'
API_KEY = os.getenv('MOONDREAM_API_KEY')

# Dictionary to store the last image information for each thread
thread_images = {}

# Command aliases mapping
COMMAND_ALIASES = {
    'caption': ['caption', 'c'],
    'query': ['query', 'q'],
    'detect': ['detect', 'd'],
    'point': ['point', 'p']
}

# Reverse mapping for alias lookup
ALIAS_TO_COMMAND = {}
for cmd, aliases in COMMAND_ALIASES.items():
    for alias in aliases:
        ALIAS_TO_COMMAND[alias] = cmd

# Discord message size limits
DISCORD_REGULAR_MSG_LIMIT = 1900  # Setting slightly under the 2000 limit for safety
DISCORD_CODE_BLOCK_LIMIT = 1800  # Even smaller limit for code blocks due to backticks

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

def image_to_base64(image):
    """Convert a PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"

async def call_moondream_api(endpoint, image_base64, additional_params=None):
    """Call Moondream API and return the response"""
    url = f"{API_BASE_URL}/{endpoint}"
    
    # Prepare request body
    payload = {
        "image_url": image_base64,
        "stream": False
    }
    
    # Add additional parameters if provided
    if additional_params:
        payload.update(additional_params)
    
    # Prepare headers
    headers = {
        "X-Moondream-Auth": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Make the API call
    response = requests.post(url, headers=headers, json=payload)
    
    # Check for success
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API Error: {response.status_code} - {response.text}"}

async def download_image_bytes(url):
    """Download an image from a URL and return the bytes"""
    response = requests.get(url)
    return io.BytesIO(response.content)

async def send_help_message(thread, user):
    """Send a simplified help message with available commands"""
    help_message = (
        f"# Welcome {user.mention} to Moondream Vision AI\n\n"
        "I can analyze images using Moondream's vision API. Use these commands with the image below:\n\n"
        "**📝 Caption Generation**\n"
        "`!c` - Generate a description of your image\n\n"
        "**❓ Visual Question Answering**\n"
        "`!q [your question]` - Ask any question about your image\n\n"
        "**🔍 Object Detection**\n"
        "`!d [object]` - Detect specific objects in your image\n\n"
        "**👉 Object Pointing**\n"
        "`!p [object]` - Point to specific objects in your image\n\n"
        "Upload a new image at any time to analyze it! Use `!help` for more details."
    )
    await thread.send(help_message)

async def send_detailed_help(channel):
    """Send a detailed help message with all command options"""
    help_message = (
        "# Moondream Vision AI - Command Reference\n\n"
        "## Short Commands (Recommended in threads)\n"
        "- `!c` - Generate an image caption\n"
        "- `!q [question]` - Ask a question about the image\n"
        "- `!d [object]` - Detect objects in the image\n"
        "- `!p [object]` - Point to objects in the image\n\n"
        
        "## Standard Commands (Also work in threads)\n"
        "- `!caption` - Generate an image caption\n"
        "- `!query [question]` - Ask a question about the image\n"
        "- `!detect [object]` - Detect objects in the image\n"
        "- `!point [object]` - Point to objects in the image\n\n"
        
        "## Full Commands (For main channels)\n"
        "- `!moondream caption` - Generate an image caption\n"
        "- `!moondream query [question]` - Ask a question about the image\n"
        "- `!moondream detect [object]` - Detect objects in the image\n"
        "- `!moondream point [object]` - Point to objects in the image\n\n"
        
        "## Tips\n"
        "- Upload an image with any command to start a new analysis thread\n"
        "- In a thread, use short commands without re-uploading the image\n"
        "- To analyze a new image, start fresh in a main channel"
    )
    await channel.send(help_message)

async def save_image_to_thread(thread, image_bytes, filename):
    """Save an image to a thread and store its reference for later use"""
    # Reposition to the start of the BytesIO object
    image_bytes.seek(0)
    
    # Save a copy of the image in the thread
    image_message = await thread.send(
        "🖼️ **Analyzing this image:**",
        file=discord.File(fp=image_bytes, filename=filename)
    )
    
    # Store the image information
    thread_images[thread.id] = {
        'url': image_message.attachments[0].url,
        'filename': filename,
        'message_id': image_message.id
    }
    
    # Return the image message for reference
    return image_message

async def split_and_send_message(channel, content):
    """Split a long message and send it in chunks to avoid Discord's limit"""
    # If content is short enough, send it as is
    if len(content) <= DISCORD_REGULAR_MSG_LIMIT:
        await channel.send(content)
        return

    # Otherwise, split it into chunks
    chunks = [content[i:i + DISCORD_REGULAR_MSG_LIMIT] 
              for i in range(0, len(content), DISCORD_REGULAR_MSG_LIMIT)]
    
    for chunk in chunks:
        await channel.send(chunk)

async def split_and_send_code_block(channel, content, language="json"):
    """Split a code block into multiple messages if needed"""
    # Calculate max content per code block (accounting for the backticks and language)
    max_content = DISCORD_CODE_BLOCK_LIMIT - len(language) - 6  # 6 for the ```lang and ``` markers
    
    # If it fits in one message
    if len(content) <= max_content:
        await channel.send(f"```{language}\n{content}\n```")
        return
    
    # Calculate number of parts needed
    total_parts = math.ceil(len(content) / max_content)
    
    # Split and send
    for i in range(total_parts):
        start_pos = i * max_content
        end_pos = min((i + 1) * max_content, len(content))
        part_content = content[start_pos:end_pos]
        
        # Add part indicator
        part_msg = f"```{language}\n# Part {i+1}/{total_parts}\n{part_content}\n```"
        await channel.send(part_msg)

async def process_image_in_thread(thread, image_bytes, image_filename, endpoint=None, parameter=None):
    """Process an image within a thread"""
    # Add a divider before the new response
    await thread.send("───────────────────────────────────────")
    
    # Create an initial message that preserves the command context
    command_display = ""
    if endpoint:
        # Show the exact command used
        command_used = f"!{endpoint}"
        if parameter:
            command_used += f" {parameter}"
        command_display = f"**Command:** `{command_used}`"
    
    # Send the "processing" message
    processing_msg = await thread.send(f"{command_display}\n\nProcessing your image...")
    
    try:
        # Open the image from bytes
        image_bytes.seek(0)
        image = Image.open(image_bytes).convert('RGB')
        
        # Convert image to base64
        image_base64 = image_to_base64(image)
        
        # If no endpoint specified, just confirm image is ready and send help
        if not endpoint:
            await processing_msg.edit(content="Image received! What would you like to know about it?")
            return
        
        # Map endpoint alias to actual endpoint if needed
        actual_endpoint = endpoint
        if endpoint in ALIAS_TO_COMMAND:
            actual_endpoint = ALIAS_TO_COMMAND[endpoint]
        
        # Prepare additional parameters based on endpoint
        additional_params = {}
        
        if actual_endpoint == 'query':
            if not parameter:
                await processing_msg.edit(content=f"{command_display}\n\nPlease provide a question for the image.")
                return
            additional_params["question"] = parameter
            
        elif actual_endpoint == 'caption':
            additional_params["length"] = "normal"
            
        elif actual_endpoint in ['detect', 'point']:
            object_to_find = parameter or "subject"  # Default to "subject" if no parameter provided
            additional_params["object"] = object_to_find
        
        # Call the API
        result = await call_moondream_api(actual_endpoint, image_base64, additional_params)
        
        # Check for errors
        if 'error' in result:
            await processing_msg.edit(content=f"{command_display}\n\nError: {result['error']}")
            return
        
        # Format the response based on the endpoint
        if actual_endpoint == 'caption':
            formatted_result = f"**Caption:** {result['caption']}"
        elif actual_endpoint == 'query':
            formatted_result = f"**Question:** {parameter}\n**Answer:** {result['answer']}"
        elif actual_endpoint == 'detect':
            formatted_result = f"**Detecting:** {parameter or 'subject'}\n**Found:** {json.dumps(result['objects'])}"
        elif actual_endpoint == 'point':
            formatted_result = f"**Pointing at:** {parameter or 'subject'}\n**Points:** {json.dumps(result['points'])}"
        else:
            formatted_result = f"**Raw response:** {json.dumps(result)}"
        
        # Update the processing message with just the formatted result
        await processing_msg.edit(content=f"{command_display}\n\n{formatted_result}")
        
        # Send the raw API response as a separate message with proper splitting
        raw_response = json.dumps(result, indent=2)
        await split_and_send_code_block(thread, raw_response)
        
    except Exception as e:
        await processing_msg.edit(content=f"{command_display}\n\nError: {str(e)}")

async def try_delete_message(message):
    """Try to delete a message and handle permission errors"""
    try:
        await message.delete()
        return True
    except discord.Forbidden:
        await message.channel.send(
            "Note: I don't have permission to delete messages. Please grant 'Manage Messages' permission for a cleaner experience.", 
            delete_after=10
        )
        return False
    except Exception as e:
        print(f"Error deleting message: {e}")
        return False

async def is_moondream_thread(thread):
    """Check if this is a thread created by the Moondream bot"""
    if not isinstance(thread, discord.Thread):
        return False
    
    # Check thread name
    if "Moondream Analysis" in thread.name:
        return True
    
    # If we can't determine from the name, check if we have stored image data for this thread
    return thread.id in thread_images

@bot.event
async def on_message(message):
    # Don't process messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if message is in a thread created by Moondream
    if await is_moondream_thread(message.channel):
        thread = message.channel
        
        # Check for all possible command formats, including shortcuts
        # 1. Check for !moondream command format
        moondream_match = re.match(r'!moondream\s+(\w+)(?:\s+(.+))?', message.content.strip())
        # 2. Check for !command shortcut format
        shortcut_match = re.match(r'!(\w+)(?:\s+(.+))?', message.content.strip())
        
        command_match = moondream_match
        if not command_match:
            command_match = shortcut_match
        
        if command_match:
            endpoint = command_match.group(1).lower()
            parameter = command_match.group(2) if command_match.group(2) else None
            
            # Check if help command
            if endpoint == 'help':
                await send_detailed_help(thread)
                return
            
            # Check if the command is a valid endpoint or an alias
            valid_endpoint = endpoint in ['caption', 'query', 'detect', 'point'] or endpoint in ALIAS_TO_COMMAND
            
            if valid_endpoint:
                # If there's an image attachment, use that
                if message.attachments and any(att.content_type and att.content_type.startswith('image/') for att in message.attachments):
                    image_attachment = next(att for att in message.attachments if att.content_type and att.content_type.startswith('image/'))
                    image_bytes = await download_image_bytes(image_attachment.url)
                    
                    # Save the new image to the thread
                    await save_image_to_thread(thread, image_bytes, image_attachment.filename)
                    
                    # Process with the new image
                    image_bytes.seek(0)
                    await process_image_in_thread(thread, image_bytes, image_attachment.filename, endpoint, parameter)
                
                # Otherwise, use the last saved image for this thread
                elif thread.id in thread_images:
                    # Get the last image info
                    image_info = thread_images[thread.id]
                    
                    # Download the image
                    image_bytes = await download_image_bytes(image_info['url'])
                    
                    # Process with the saved image
                    await process_image_in_thread(thread, image_bytes, image_info['filename'], endpoint, parameter)
                
                else:
                    await thread.send("I can't find an image to analyze. Please start a new thread with an image.")
                
                # Try to delete the command message
                await try_delete_message(message)
                return
            
        # If a new image is uploaded without a command, save it for later use
        elif message.attachments and any(att.content_type and att.content_type.startswith('image/') for att in message.attachments):
            image_attachment = next(att for att in message.attachments if att.content_type and att.content_type.startswith('image/'))
            image_bytes = await download_image_bytes(image_attachment.url)
            
            # Save the new image to the thread
            await save_image_to_thread(thread, image_bytes, image_attachment.filename)
            
            # Acknowledge the image
            await thread.send("New image received! What would you like to know about it?")
            return
    
    # Let the command system process commands
    await bot.process_commands(message)

@bot.command()
async def moondream(ctx, endpoint=None, *, parameter=None):
    """
    Process an image with Moondream API
    
    Usage:
    !moondream - Start interactive mode with the attached image
    !moondream caption - Generate a caption for the attached image
    !moondream query What's in this image? - Ask a question about the attached image
    !moondream detect dog - Detect objects in the attached image
    !moondream point cat - Point at objects in the attached image
    """
    # Check if we're already in a thread - if so, redirect to use thread commands
    if isinstance(ctx.channel, discord.Thread) and await is_moondream_thread(ctx.channel):
        await ctx.send("You're already in a Moondream thread! Just use shorthand commands like `!c`, `!q`, `!d`, or `!p`.")
        return
    
    # Format the command for display
    command_display = f"**Command:** `{ctx.message.content}`"
    
    # Check if an image is attached
    if not ctx.message.attachments:
        reminder = await ctx.send(f"{command_display}\n\nPlease attach an image to analyze.", delete_after=10)
        # Try to delete the original message
        await try_delete_message(ctx.message)
        return
    
    # Get the first attached image
    attachment = ctx.message.attachments[0]
    
    # Process only if the attachment is an image
    if attachment.content_type and attachment.content_type.startswith('image/'):
        # Create a thread name based on the current time
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        thread_name = f"Moondream Analysis {timestamp}"
        
        # Create a thread
        thread = await ctx.message.create_thread(name=thread_name, auto_archive_duration=60)
        
        # Send a notification in the original channel pointing to the thread
        notification = await ctx.send(
            f"✅ Image received from {ctx.author.mention}! Please continue in the thread: {thread.mention}", 
            delete_after=5
        )
        
        # Send welcome message with user mention in the thread
        await send_help_message(thread, ctx.author)
        
        # Download the image to bytes
        image_bytes = await download_image_bytes(attachment.url)
        
        # Save the image to the thread
        await save_image_to_thread(thread, image_bytes, attachment.filename)
        
        # Process the image in the thread (map endpoint alias to actual endpoint if needed)
        image_bytes.seek(0)
        actual_endpoint = endpoint
        if endpoint and endpoint in ALIAS_TO_COMMAND:
            actual_endpoint = ALIAS_TO_COMMAND[endpoint]
            
        if actual_endpoint and actual_endpoint in ['caption', 'query', 'detect', 'point']:
            await process_image_in_thread(thread, image_bytes, attachment.filename, actual_endpoint, parameter)
        else:
            # Just confirm image received if no specific endpoint
            # No divider needed for first message in thread
            await thread.send("Image received! What would you like to know about it?")
        
        # Try to delete the original message
        await try_delete_message(ctx.message)
    else:
        notice = await ctx.send(f"{command_display}\n\nThe attachment does not appear to be an image.", delete_after=10)
        # Try to delete the original message
        await try_delete_message(ctx.message)

# Add command aliases for the main channel
@bot.command(aliases=['c'])
async def caption(ctx, *, parameter=None):
    """Shortcut for !moondream caption"""
    await moondream(ctx, 'caption', parameter=parameter)

@bot.command(aliases=['q'])
async def query(ctx, *, parameter=None):
    """Shortcut for !moondream query"""
    await moondream(ctx, 'query', parameter=parameter)

@bot.command(aliases=['d'])
async def detect(ctx, *, parameter=None):
    """Shortcut for !moondream detect"""
    await moondream(ctx, 'detect', parameter=parameter)

@bot.command(aliases=['p'])
async def point(ctx, *, parameter=None):
    """Shortcut for !moondream point"""
    await moondream(ctx, 'point', parameter=parameter)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))