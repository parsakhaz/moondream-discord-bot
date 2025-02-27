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

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

# Moondream API configuration
API_BASE_URL = 'https://api.moondream.ai/v1'
API_KEY = os.getenv('MOONDREAM_API_KEY')

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

async def download_image(url):
    """Download an image from a URL and return a PIL Image object"""
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    return Image.open(image_bytes)

async def send_help_message(thread):
    """Send a help message with available commands"""
    help_message = (
        "# Moondream Vision AI\n\n"
        "I can analyze images using Moondream's vision API. Upload an image and use one of these commands:\n\n"
        "**📝 Caption Generation**\n"
        "`!moondream caption` - Generate a description of your image\n\n"
        "**❓ Visual Question Answering**\n"
        "`!moondream query [your question]` - Ask any question about your image\n\n"
        "**🔍 Object Detection**\n"
        "`!moondream detect [object]` - Detect specific objects in your image\n\n"
        "**👉 Object Pointing**\n"
        "`!moondream point [object]` - Point to specific objects in your image\n\n"
        "Upload a new image at any time to analyze it!"
    )
    await thread.send(help_message)

async def process_image_in_thread(thread, attachment, endpoint=None, parameter=None):
    """Process an image within a thread"""
    if not attachment.content_type or not attachment.content_type.startswith('image/'):
        await thread.send("The attachment does not appear to be an image.")
        return
    
    processing_msg = await thread.send("Processing your image...")
    
    try:
        # Download the image
        image = await download_image(attachment.url)
        
        # Convert image to base64
        image_base64 = image_to_base64(image)
        
        # If no endpoint specified, just confirm image is ready and send help
        if not endpoint:
            await processing_msg.edit(content="Image received! What would you like to know about it?")
            return
        
        # Prepare additional parameters based on endpoint
        additional_params = {}
        
        if endpoint == 'query':
            if not parameter:
                await processing_msg.edit(content="Please provide a question for the image.")
                return
            additional_params["question"] = parameter
            
        elif endpoint == 'caption':
            additional_params["length"] = "normal"
            
        elif endpoint in ['detect', 'point']:
            object_to_find = parameter or "subject"  # Default to "subject" if no parameter provided
            additional_params["object"] = object_to_find
        
        # Call the API
        result = await call_moondream_api(endpoint, image_base64, additional_params)
        
        # Check for errors
        if 'error' in result:
            await processing_msg.edit(content=f"Error: {result['error']}")
            return
        
        # Format the response based on the endpoint
        if endpoint == 'caption':
            formatted_result = f"Caption: {result['caption']}"
        elif endpoint == 'query':
            formatted_result = f"Answer to '{parameter}': {result['answer']}"
        elif endpoint == 'detect':
            formatted_result = f"Detected {parameter or 'subject'}: {json.dumps(result['objects'])}"
        elif endpoint == 'point':
            formatted_result = f"Points for {parameter or 'subject'}: {json.dumps(result['points'])}"
        else:
            formatted_result = f"Raw response: {json.dumps(result)}"
        
        # Send the raw API response along with the formatted result
        await processing_msg.edit(content=f"{formatted_result}\n\nRaw API Response:\n```json\n{json.dumps(result, indent=2)}\n```")
        
    except Exception as e:
        await processing_msg.edit(content=f"Error: {str(e)}")

@bot.event
async def on_message(message):
    # Don't process messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if message is in a thread where the bot is active
    if isinstance(message.channel, discord.Thread) and bot.user in message.channel.recipients:
        # If it's an image in a thread
        if message.attachments and any(attachment.content_type and attachment.content_type.startswith('image/') 
                                      for attachment in message.attachments):
            # Get the first image attachment
            image_attachment = next(attachment for attachment in message.attachments 
                                  if attachment.content_type and attachment.content_type.startswith('image/'))
            
            # Check if there are any commands in the message
            parts = message.content.strip().split(' ', 2)
            
            if len(parts) >= 2 and parts[0] == '!moondream':
                endpoint = parts[1].lower()
                parameter = parts[2] if len(parts) > 2 else None
                
                if endpoint in ['caption', 'query', 'detect', 'point']:
                    await process_image_in_thread(message.channel, image_attachment, endpoint, parameter)
                    return
            
            # If no valid command, just process the image
            await process_image_in_thread(message.channel, image_attachment)
        
        # If it's a command without an image, remind them to upload an image
        elif message.content.startswith('!moondream'):
            await message.channel.send("Please upload an image along with your command.")
    
    # Let the command system process commands
    await bot.process_commands(message)

@bot.command()
async def moondream(ctx, endpoint=None, *, parameter=None):
    """
    Process an image with Moondream API
    
    Usage:
    !moondream - Start interactive mode with the attached image
    !moondream caption - Generate a caption for the attached image
    !moondream query What's in this image? - Answer a question about the attached image
    !moondream detect dog - Detect objects in the attached image
    !moondream point cat - Point at objects in the attached image
    """
    # Check if an image is attached
    if not ctx.message.attachments:
        await ctx.send("Please attach an image to analyze.", delete_after=5)
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
        
        # Send welcome message
        await send_help_message(thread)
        
        # Process the image in the thread
        if endpoint and endpoint in ['caption', 'query', 'detect', 'point']:
            await process_image_in_thread(thread, attachment, endpoint, parameter)
        else:
            # Just confirm image received if no specific endpoint
            await process_image_in_thread(thread, attachment)
        
        # Try to delete the original message if the bot has permission
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            await ctx.send("Note: I don't have permission to delete messages. Please grant 'Manage Messages' permission for a cleaner experience.", delete_after=10)
    else:
        await ctx.send("The attachment does not appear to be an image.", delete_after=5)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))