import discord
import math

# Discord message size limits
DISCORD_MSG_LIMIT = 2000
DISCORD_SAFE_LIMIT = 1900  # Setting slightly under the 2000 limit for safety
DISCORD_CODE_BLOCK_LIMIT = 1800  # Even smaller limit for code blocks due to backticks

class MessageSplitter:
    @staticmethod
    async def send_message(channel, content, **kwargs):
        """
        Send a message to a Discord channel, automatically splitting if needed.
        Works for any channel-like object (channel, thread, or context).
        
        Supports all kwargs that discord.py's send method supports, including:
        - delete_after: Seconds after which to delete the message
        - file, files: Attachments to include
        - embed, embeds: Embeds to include
        - etc.
        
        Note: For split messages, kwargs like delete_after will apply to all parts.
        """
        # If content is short enough, send it as is
        if len(content) <= DISCORD_SAFE_LIMIT:
            return await channel.send(content, **kwargs)
        
        # For split messages, we need to handle attachments and embeds specially
        # Only include them in the first message
        first_message_kwargs = kwargs.copy()
        rest_message_kwargs = {k: v for k, v in kwargs.items() 
                              if k not in ('file', 'files', 'embed', 'embeds')}
        
        # Otherwise, split it into chunks
        messages = []
        chunks = [content[i:i + DISCORD_SAFE_LIMIT] 
                for i in range(0, len(content), DISCORD_SAFE_LIMIT)]
        
        # Send first chunk with all attachments
        messages.append(await channel.send(chunks[0], **first_message_kwargs))
        
        # Send remaining chunks without attachments
        for chunk in chunks[1:]:
            messages.append(await channel.send(chunk, **rest_message_kwargs))
        
        return messages[-1]  # Return the last message for reference
    
    @staticmethod
    async def edit_message(message, content):
        """Edit a message, splitting it if needed."""
        # If content is short enough, edit it directly
        if len(content) <= DISCORD_SAFE_LIMIT:
            return await message.edit(content=content)
        
        # For longer content, delete original and send as multiple messages
        channel = message.channel
        await message.delete()
        
        return await MessageSplitter.send_message(channel, content)
    
    @staticmethod
    async def send_code_block(channel, content, language=""):
        """Send a code block, splitting it if needed."""
        # Calculate max content per code block (accounting for the backticks and language)
        max_content = DISCORD_CODE_BLOCK_LIMIT - len(language) - 6  # 6 for the ```lang and ``` markers
        
        # If it fits in one message
        if len(content) <= max_content:
            return await channel.send(f"```{language}\n{content}\n```")
        
        # Calculate number of parts needed
        total_parts = math.ceil(len(content) / max_content)
        messages = []
        
        # Split and send
        for i in range(total_parts):
            start_pos = i * max_content
            end_pos = min((i + 1) * max_content, len(content))
            part_content = content[start_pos:end_pos]
            
            # Add part indicator
            part_msg = f"```{language}\n# Part {i+1}/{total_parts}\n{part_content}\n```"
            messages.append(await channel.send(part_msg))
        
        return messages[-1]  # Return the last message for reference
    
    @staticmethod
    async def send_embed(channel, embed):
        """Send an embed, splitting the description if needed."""
        # Check if the embed description exceeds the limit
        if embed.description and len(embed.description) > DISCORD_SAFE_LIMIT:
            # Save the original description
            full_description = embed.description
            
            # Send first part with embed
            embed.description = full_description[:DISCORD_SAFE_LIMIT]
            await channel.send(embed=embed)
            
            # Send remaining parts as regular messages
            remaining = full_description[DISCORD_SAFE_LIMIT:]
            return await MessageSplitter.send_message(channel, remaining)
        
        # If within limits, send normally
        return await channel.send(embed=embed)