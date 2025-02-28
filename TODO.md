# TODO List for Moondream Discord Bot

## Critical Issues

- **Fix message splitting**: The caption command (`!c`) is still hitting Discord's 2000 character limit with a 400 Bad Request error
  - Need to further separate the API response handling for caption results which can be very lengthy
  - Ensure message splitting occurs before sending, not just for code blocks
  - Apply length validation before any message send attempt

- **Handle large responses from all endpoints**: Some endpoints are working but others still fail
  - Test and fix issues with each endpoint individually (caption, query, detect, point)
  - Add specific handling for each response type's format

- **Improve error handling**: Catch Discord errors and retry with split messages
  - Add a try/catch block around all message send operations
  - Automatically split messages when receiving 400 errors
  - Log detailed error information for debugging

## Enhancements

- **Add better response formatting**: Improve readability of large responses
  - Format detect/point results more visually (possibly using Discord embeds)
  - Add visual markers or icons to make different parts of responses clearer

- **Implement retry mechanism**: When API calls fail, retry with exponential backoff
  - Add configurable retry parameters (max attempts, delay between retries)
  - Provide user feedback during retry process

- **Add safeguards for API rate limits**: Implement queuing system for high-traffic servers
  - Track API usage to stay within Moondream's rate limits
  - Queue requests when approaching limits

- **Improve command validation**: Check parameters before making API calls
  - Add validation for each command's parameters
  - Provide helpful error messages for invalid commands

## UI/UX Improvements

- **Enhance image handling UI**: Make it clearer when a new image is being analyzed
  - Add timestamps to image analysis sessions
  - Consider adding reaction buttons for quick actions

- **Add progress indicators**: Show when the bot is processing an image
  - Use typing indicators during API calls
  - Add visual progress updates for long-running operations

- **Refine help command**: Make help more contextual and user-friendly
  - Add examples with each command in help message
  - Create command-specific help (`!help caption`, etc.)

## Testing & Documentation

- **Create automated tests**: Test all commands with various image types
  - Unit tests for utility functions
  - Integration tests for Discord and API interactions
  - Test with edge cases (very large images, unusual formats)

- **Update documentation**: Ensure all features and fixes are documented
  - Update README with troubleshooting for common errors
  - Add developer documentation for extending the bot

## Technical Debt

- **Refactor code structure**: Move to a more modular architecture
  - Separate command handling, API interaction, and Discord interface
  - Create utility modules for common operations

- **Implement better logging**: Add structured logging for easier debugging
  - Log all API calls and responses (excluding image data)
  - Log Discord events and error conditions

- **Add configuration management**: Move hardcoded values to config file
  - Create a config.py file for all constants and settings
  - Allow server-specific configuration