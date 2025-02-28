# Changelog

All notable changes to the Moondream Discord Bot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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