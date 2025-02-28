# TODO List for Moondream Discord Bot

## ✅ Completed Items

- **Optimized image processing workflow**: Eliminated redundant encoding operations
  - Added pre-encoded base64 support to process_image_in_thread
  - Modified thread creation to reuse encoded images
  - Improved caching efficiency for initial operations
  - Reduced memory usage from duplicate image data

- **Added image caching system**: Implemented LRU cache for processed images
  - Created `ImageCache` class with hit/miss tracking
  - Modified image processing workflow to use cache
  - Added admin commands for cache management
  - Added periodic cache statistics logging

- **Improved thread management**: Added automated cleanup for old threads
  - Added timestamp tracking for thread creation
  - Implemented periodic task to remove stale references
  - Added admin command to view thread statistics
  - Added check for archived threads

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

- **Add thread management commands for users**: Allow users to manage their analysis threads
  - Add command to archive threads after analysis is complete
  - Create a command to list all active analysis threads for the user
  - Add option for users to manage thread archive duration

- **Improve image reference system**: Better handle multiple images in threads
  - Allow referencing specific images when multiple are uploaded
  - Create a system to track image history within threads
  - Add command to display all images analyzed in a thread

## Performance Optimizations

- **Optimize image cache further**:
  - Implement image resizing for very large images before caching
  - Add configurable parameters for JPEG quality vs size
  - Consider implementing partial cache persistence between restarts
  - Add cache warmup for frequently used images

- **Implement async HTTP client**:
  - Replace synchronous requests with aiohttp for API calls
  - Add connection pooling for better performance
  - Implement proper retry logic for failed requests

- **Add safeguards for API rate limits**: Implement queuing system for high-traffic servers
  - Track API usage to stay within Moondream's rate limits
  - Queue requests when approaching limits
  - Add prioritization for different types of requests

## UI/UX Improvements

- **Add better response formatting**: Improve readability of large responses
  - Format detect/point results more visually (possibly using Discord embeds)
  - Add visual markers or icons to make different parts of responses clearer

- **Enhance image handling UI**: Make it clearer when a new image is being analyzed
  - Add timestamps to image analysis sessions
  - Consider adding reaction buttons for quick actions

- **Add progress indicators**: Show when the bot is processing an image
  - Use typing indicators during API calls
  - Add visual progress updates for long-running operations

- **Refine help command**: Make help more contextual and user-friendly
  - Add examples with each command in help message
  - Create command-specific help (`!help caption`, etc.)
  - Include information about caching in help documentation

## Testing & Documentation

- **Test cache performance**: Create benchmarks for different cache sizes and usage patterns
  - Test with various image sizes and types
  - Measure memory usage under different loads
  - Determine optimal cache size for different server types

- **Test thread cleanup**: Ensure thread cleanup works correctly over long periods
  - Verify memory usage remains stable
  - Check for edge cases with thread deletion and archiving
  - Test with high thread volume

- **Create automated tests**: Test all commands with various image types
  - Unit tests for utility functions
  - Integration tests for Discord and API interactions
  - Test with edge cases (very large images, unusual formats)

- **Update documentation**: Ensure all features and fixes are documented
  - Update README with troubleshooting for common errors
  - Add developer documentation for extending the bot
  - Create a user guide with examples of caching benefits

## Technical Debt

- **Refactor code structure**: Move to a more modular architecture
  - Separate command handling, API interaction, and Discord interface
  - Create utility modules for common operations
  - Create dedicated modules for caching and thread management

- **Implement better logging**: Add structured logging for easier debugging
  - Log all API calls and responses (excluding image data)
  - Log Discord events and error conditions
  - Add specific logging for cache hits/misses in production

- **Add configuration management**: Move hardcoded values to config file
  - Create a config.py file for all constants and settings
  - Allow server-specific configuration
  - Add configuration options for cache size and behavior