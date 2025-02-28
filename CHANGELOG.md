# Changelog

All notable changes to the Moondream Discord Bot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2025-03-01

### Added
- Smart image scaling system using PIL's `draft()` method for optimized loading
- Adaptive image size reduction based on dimensions:
  - 1/4 scale for images larger than 3200×3200
  - 1/3 scale for images larger than 2400×2400
  - 1/2 scale for images larger than 1600×1600
- New `optimize_image_load()` function for intelligent image preprocessing
- Diagnostic logging of image scaling operations

### Changed
- Completely redesigned `image_to_base64()` function with intelligent processing flow
- Enhanced caching system to store optimized versions of images
- Updated image processing pipeline to prioritize cache hits
- Modified visualization functions to work with optimized images
- Improved memory usage tracking in cache statistics

### Fixed
- Performance bottleneck with large images (especially from smartphone cameras)
- Excessive memory usage when processing high-resolution images
- Slow loading times for initial image processing
- Redundant processing for detect/point visualization operations

## [1.5.2] - 2025-02-29

### Added
- Enhanced visualization for object detection with thick bright red bounding boxes
- Improved point detection visualization with concentric circles in bright red and neon green
- Better visibility and contrast for all visual elements

### Changed
- Simplified bounding box design to use a single thick bright red border
- Optimized point visualization with increased spacing and thicker borders
- Adjusted center dot size and circle spacing for better visibility

## [1.5.1] - 2025-02-29

### Changed
- Optimized image processing workflow to avoid redundant encoding operations
- Modified `process_image_in_thread` to accept pre-encoded base64 images
- Updated thread creation process to reuse encoded images between title generation and initial command
- Enhanced caching efficiency by ensuring images are cached on first use
- Improved memory usage by reducing duplicate image data in memory

### Fixed
- Eliminated redundant image encoding during thread creation and initial command processing
- Fixed cache misses during thread title generation
- Resolved inefficient image processing in command handling

## [1.5.0] - 2025-02-29

### Added
- Image caching system using LRU (Least Recently Used) eviction strategy
- `ImageCache` class that stores processed base64 image data
- Cache hit/miss statistics tracking for performance monitoring
- Admin commands: `!cache_stats` and `!clear_cache` for cache management
- Thread cleanup system that removes old thread references automatically
- Admin command `!thread_stats` to monitor thread tracking and memory usage
- Timestamps to thread tracking for age-based cleanup
- Scheduled tasks for periodic cache statistics logging
- Scheduled tasks for thread cleanup (runs every 24 hours)

### Changed
- Image processing workflow now checks cache before encoding
- Improved memory usage by cleaning up stale thread references
- Enhanced API calls with consistent User-Agent header "MoondreamDiscordBot/1.4.0"
- Thread dictionary now stores creation timestamps
- Image to base64 conversion now uses cached data when available
- Thread matching now accepts all threads with "Moondream" in the name

### Fixed
- Memory leaks from accumulated thread references
- Repeated image encoding for the same image
- Unnecessary API load for repeated operations on the same image
- Thread identification for renamed threads

## [1.4.0] - 2025-02-28

### Added
- Dynamic thread titling that uses Moondream's query capability to name threads based on image content
- New function `get_image_title()` to generate meaningful titles for image analysis threads
- Title cleaning and formatting to ensure Discord thread name compatibility
- Thread renaming after initial creation to replace timestamp with descriptive title
- Automatic fallback to timestamp-based naming if title generation fails
- Logging for successful thread renaming operations

### Changed
- Thread creation process now uses a two-step approach: create with temporary name, then update with AI-generated title
- Thread naming convention changed from "Moondream Analysis [timestamp]" to "Moondream: [Generated Title]"
- Improved user experience with more descriptive thread names for easier navigation
- Enhanced thread management system to handle title updates

### Fixed
- Title length issues with Discord's 100-character thread name limit

## [1.3.0] - 2025-02-28

### Added
- Message splitting functionality to handle Discord's message length limitations
- Separate message for raw API responses to avoid 400 errors
- Support for multi-part JSON responses that exceed Discord's character limits
- Part indicators for split messages (e.g., "Part 1/3")
- Constants for Discord message size limits

### Changed
- Improved formatting of command responses for better readability
- Separated formatted results from raw JSON data
- Enhanced error handling for API responses
- Optimized command display format to be more concise

### Fixed
- Fixed 400 Bad Request errors when responses exceeded Discord's size limits
- Resolved issues with detect and point commands failing on complex images
- Improved handling of large JSON payloads

## [1.2.0] - 2025-02-27

### Added
- Shorthand command aliases (`!c`, `!q`, `!d`, `!p`)
- Visual separators between responses for better readability
- Simplified help menu focused on shorthand commands
- Detailed help command via `!help`
- Command alias lookup system

### Changed
- Updated help message to prioritize shorthand commands
- Improved command formatting in responses
- Enhanced thread navigation with better user notifications
- Refined message deletion handling

### Fixed
- Thread identification issues
- Inconsistent command recognition

## [1.1.0] - 2025-02-26

### Added
- Thread-based conversation support
- Image preservation within threads
- Automatic thread creation for each image analysis
- Thread image memory to avoid re-uploading images
- Support for using the last saved image for new commands
- User mentions in welcome messages

### Changed
- Commands now operate within dedicated threads
- Original messages are deleted after processing to keep channels clean
- Enhanced user experience with thread notifications
- Improved image handling workflow

### Fixed
- Messages being lost when original content was deleted
- Confusion about where to continue conversations
- Thread navigation clarity

## [1.0.0] - 2025-02-25

### Added
- Initial implementation of Discord bot with Moondream API integration
- Support for caption, query, detect, and point commands
- Direct integration with Moondream's Vision AI API
- Basic command structure using `!moondream <command>`
- Image analysis capabilities
- Environment variable configuration
- Basic help messages
- Error handling for API calls

### Changed
- Migrated from using Moondream client library to direct API calls
- Optimized image processing workflow
- Improved response formatting

### Fixed
- Initial implementation issues
- Base64 image encoding