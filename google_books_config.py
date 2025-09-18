"""
Google Books API Configuration

This file contains configuration and instructions for setting up the Google Books API
integration in your Django bookstore project.

SETUP INSTRUCTIONS:
1. Get a Google Books API Key:
   - Go to Google Cloud Console: https://console.cloud.google.com/
   - Create a new project or select an existing one
   - Enable the Google Books API
   - Create credentials (API Key)
   - Copy your API key

2. Set Environment Variable:
   - Add your API key to your environment variables:
     export GOOGLE_BOOKS_API_KEY="your_api_key_here"
   
   - Or add it to your .env file:
     GOOGLE_BOOKS_API_KEY=your_api_key_here

3. For Production (Render.com):
   - Add the environment variable in your Render dashboard
   - Go to your service > Environment > Environment Variables
   - Add: GOOGLE_BOOKS_API_KEY = your_api_key_here

FEATURES:
- Search books by title, author, or topic
- View book details and ratings
- Read books online using Google's web reader
- Browse featured books from various categories
- Caching for improved performance

API ENDPOINTS:
- /google-books/ - Search and browse Google Books
- /google-books/book/<google_id>/ - View book details
- /google-books/book/<google_id>/read/ - Read book online

CACHING:
- Search results are cached for 1 hour
- Book details are cached for 2 hours
- Reduces API calls and improves performance

ERROR HANDLING:
- Graceful fallback when API is unavailable
- User-friendly error messages
- Logging for debugging

SECURITY:
- API key is stored in environment variables
- No sensitive data exposed in templates
- Rate limiting through Google's API quotas
"""

# Default API configuration
DEFAULT_API_CONFIG = {
    'base_url': 'https://www.googleapis.com/books/v1',
    'max_results': 20,
    'cache_timeout': 3600,  # 1 hour
    'featured_categories': [
        'bestseller fiction',
        'popular science books',
        'classic literature',
        'modern romance novels',
        'business books',
        'self-help books'
    ]
}

# Search query examples
SEARCH_EXAMPLES = [
    'Harry Potter',
    'Stephen King',
    'science fiction',
    'romance novels',
    'business strategy',
    'cooking recipes',
    'travel guides',
    'history books'
]

# Error messages
ERROR_MESSAGES = {
    'api_unavailable': 'Google Books API is currently unavailable. Please try again later.',
    'book_not_found': 'Book not found or could not be retrieved.',
    'no_online_reading': 'This book is not available for online reading.',
    'search_failed': 'Search failed. Please try different search terms.'
}

