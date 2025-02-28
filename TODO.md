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

## Thread & Image Management

- **Enhance dynamic thread naming**: Improve title generation for unusual images
  - Add retry logic for title generation if initial attempt fails
  - Create a list of fallback title formats for different image types
  - Implement option to regenerate titles with a command like `!retitle`

- **Add thread management commands**: Allow users to manage their analysis threads
  - Add command to archive threads after analysis is complete
  - Create a command to list all active analysis threads
  - Implement a thread cleanup system for old/unused threads

- **Improve image reference system**: Better handle multiple images in threads
  - Allow referencing specific images when multiple are uploaded
  - Create a system to track image history within threads
  - Add command to display all images analyzed in a thread

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
  - Include information about thread naming in help documentation

## Testing & Documentation

- **Test thread titling with diverse images**: Ensure naming works correctly for various image types
  - Create test suite with diverse image samples (photos, art, diagrams, etc.)
  - Document common title patterns and edge cases
  - Gather user feedback on title quality and relevance

- **Create automated tests**: Test all commands with various image types
  - Unit tests for utility functions
  - Integration tests for Discord and API interactions
  - Test with edge cases (very large images, unusual formats)

- **Update documentation**: Ensure all features and fixes are documented
  - Update README with troubleshooting for common errors
  - Add developer documentation for extending the bot
  - Create a user guide with examples of dynamic thread titling

## Technical Debt

- **Refactor thread creation process**: Improve the two-step thread creation and naming flow
  - Consider using Discord's deferred responses for smoother UX
  - Optimize the title generation to reduce processing time
  - Add better error handling for thread renaming failures

- **Refactor code structure**: Move to a more modular architecture
  - Separate command handling, API interaction, and Discord interface
  - Create utility modules for common operations
  - Create dedicated module for thread title generation and management

- **Implement better logging**: Add structured logging for easier debugging
  - Log all API calls and responses (excluding image data)
  - Log Discord events and error conditions
  - Add specific logging for thread creation and renaming events

- **Add configuration management**: Move hardcoded values to config file
  - Create a config.py file for all constants and settings
  - Allow server-specific configuration
  - Add configuration options for thread naming behavior