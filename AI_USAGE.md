# AI Usage Disclosure

This project was developed with the assistance of AI tools. Below is a detailed record of how AI was used, what was verified, and any corrections made.

## AI Tools Used
- **Claude (OpenClaude)**: Used for code generation, explanation, and debugging assistance
- **GitHub Copilot**: Used for autocomplete suggestions during development

## How AI Was Used

### 1. Initial Code Generation
AI helped generate the initial structure and boilerplate code for:
- HTTP session creation with retry logic (`base_scraper.py`)
- Basic scraper templates with pagination loops
- Cleaning functions for text, price, and rating
- Validation logic structure
- Duplicate detection fingerprinting approach

### 2. Specific Implementations
- **Snippet 5.1** (HTTP session): AI provided the base implementation which was adapted with minor modifications
- **Snippet 5.2** (Pagination loop): AI provided the core loop structure that was customized for both scrapers
- **Snippet 5.3** (Field extraction): AI showed safe extraction patterns that were implemented in both scrapers
- **Snippet 5.4** (Cleaning functions): AI provided the base cleaning functions that were extended with additional edge case handling
- **Snippet 5.5** (Validation): AI showed the validation pattern that was expanded to include detailed reason tracking
- **Snippet 5.6** (Duplicate detection): AI provided the fingerprint concept that was implemented with specific rules for books vs quotes
- **Snippet 5.7** (Summary report): AI showed the JSON structure that was expanded with timing information

### 3. Testing Assistance
AI helped generate test case structures for:
- Cleaning function tests
- Validation function tests  
- Deduplication function tests

## What I Verified and Fixed

### 1. HTTP Session
**AI-generated**: Basic retry logic
**My fixes**: 
- Added proper User-Agent header
- Made session creation a separate function
- Added delay parameter to fetch_page for rate limiting
- Verified status_forcelist included appropriate HTTP codes

### 2. Scrapers
**AI-generated**: Basic pagination and parsing loops
**My fixes**:
- Added proper error handling with try/catch blocks
- Implemented null checks before accessing elements
- Added logging for debugging
- Verified CSS selectors matched actual site structure
- Fixed URL joining logic to handle relative paths correctly
- Added source-specific parsing functions

### 3. Cleaning Functions
**AI-generated**: Basic text, price, and rating cleaning
**My fixes**:
- Added handling for non-breaking spaces (\xa0)
- Improved price cleaning to handle commas in numbers
- Enhanced rating cleaning to be case-insensitive
- Added tag cleaning that lowercases, sorts, and deduplicates
- Added URL normalization with proper validation
- Added comprehensive edge case handling (None values, empty strings)

### 4. Validation
**AI-generated**: Basic validation returning True/False
**My fixes**:
- Modified to return list of problem reasons for better reporting
- Added validation for all required fields
- Implemented specific error codes for easier counting
- Added validation for price >= 0 and rating in 1-5 range
- Ensured URL validation checks for http/https prefix

### 5. Duplicate Detection
**AI-generated**: Basic fingerprinting concept
**My fixes**:
- Implemented different fingerprint rules for books vs quotes as specified
- Added proper normalization (lowercase, remove punctuation, collapse whitespace)
- Used SHA256 for reliable hashing
- Added comprehensive test cases for edge cases

### 6. Main Orchestrator
**AI-generated**: Basic main function structure
**My fixes**:
- Added proper logging configuration to both file and console
- Implemented source-specific processing functions
- Added statistics tracking throughout the pipeline
- Implemented proper CSV writing with DictWriter
- Added JSON summary report with timing information
- Wrapped each source in try/catch to prevent total failure
- Added proper directory creation for outputs

### 7. Testing
**AI-generated**: Basic test function structures
**My fixes**:
- Added comprehensive test cases for edge cases
- Verified all functions handle None and empty values properly
- Added tests for duplicate detection with various spacing/case combinations
- Ensured tests run without internet access

## Manual Corrections Made

1. **Import Organization**: Fixed circular imports and organized imports properly
2. **Error Handling**: Enhanced try/catch blocks throughout to prevent crashes
3. **Logging**: Added appropriate log levels (INFO, WARNING, ERROR) and messages
4. **Type Safety**: Added proper type checking and conversion
5. **Edge Cases**: Handled None values, empty strings, and missing elements
6. **Performance**: Verified delay between requests is appropriate (0.5 seconds)
7. **Completeness**: Ensured all required fields from the data model are included
8. **Output Format**: Verified CSV and JSON output match specifications

## What I Did Not Use AI For

- Website inspection and selector determination (done manually via browser DevTools)
- Final integration testing and end-to-end verification
- Documentation writing (README.md and this file)
- Virtual environment setup and dependency management
- Code style and formatting decisions (followed PEP 8 with manual adjustments)

## Verification Process

1. **Unit Testing**: All processing functions tested in isolation
2. **Integration Testing**: Ran full scraping cycle and verified outputs
3. **Output Validation**: 
   - Checked CSV contains expected columns and data types
   - Verified JSON summary numbers reconcile correctly
   - Confirmed log file contains appropriate entries
4. **Manual Spot Checking**: Verified random records against source websites
5. **Edge Case Testing**: Tested with malformed data and network simulations

The AI provided valuable starting points and patterns, but all code was reviewed, tested, and modified as needed to ensure correctness, completeness, and adherence to the project requirements.