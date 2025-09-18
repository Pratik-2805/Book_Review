# Google Books API Integration

This document explains how to set up and use the Google Books API integration in your Django bookstore project.

## 🚀 Features

- **Search Books**: Search for books by title, author, or topic
- **Browse Categories**: Discover books in various genres and categories
- **Online Reading**: Read books directly in your browser using Google's web reader
- **Book Details**: View comprehensive book information including ratings, descriptions, and pricing
- **Featured Books**: Browse curated collections of popular books
- **Responsive Design**: Mobile-friendly interface for reading on any device
- **Caching**: Intelligent caching to reduce API calls and improve performance

## 📋 Prerequisites

1. **Google Cloud Account**: You need a Google Cloud account to access the Books API
2. **Django Project**: This integration is built for Django projects
3. **Python 3.8+**: Required for the requests library and modern Django features

## 🔑 Setup Instructions

### 1. Get Google Books API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Books API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Books API"
   - Click "Enable"
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy your API key

### 2. Configure Environment Variables

#### Development (Local)
```bash
# Add to your .env file
GOOGLE_BOOKS_API_KEY=your_api_key_here

# Or export in your shell
export GOOGLE_BOOKS_API_KEY="your_api_key_here"
```

#### Production (Render.com)
1. Go to your Render dashboard
2. Select your service
3. Go to "Environment" > "Environment Variables"
4. Add: `GOOGLE_BOOKS_API_KEY` = `your_api_key_here`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requests` library is already added to your requirements.txt.

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🎯 Usage

### For Users

1. **Navigate to Online Reading**: Click "Online Reading" in the navigation menu
2. **Search Books**: Use the search bar to find books by title, author, or topic
3. **Browse Featured Books**: View curated collections when no search is performed
4. **View Book Details**: Click "Details" to see comprehensive book information
5. **Read Online**: Click "Read Online" to start reading the book in your browser

### For Developers

#### API Endpoints

- `GET /google-books/` - Search and browse Google Books
- `GET /google-books/book/<google_id>/` - View book details
- `GET /google-books/book/<google_id>/read/` - Read book online

#### Models

```python
from books.models import GoogleBook

# Get all Google Books
books = GoogleBook.objects.all()

# Search by title
books = GoogleBook.objects.filter(title__icontains='Python')

# Get books with online reading available
online_books = GoogleBook.objects.filter(web_reader_url__isnull=False)
```

#### Services

```python
from books.services import GoogleBooksService

service = GoogleBooksService()

# Search for books
result = service.search_books('Python programming', max_results=10)

# Get book details
book = service.get_book_details('google_book_id')

# Get featured books
featured = service.get_featured_books(max_results=12)
```

## 🏗️ Architecture

### Components

1. **Models** (`books/models.py`):
   - `GoogleBook`: Stores book data from Google Books API

2. **Services** (`books/services.py`):
   - `GoogleBooksService`: Handles API calls and data processing

3. **Views** (`books/views.py`):
   - `google_books_search`: Search and display books
   - `google_book_detail`: Show book details
   - `google_book_reader`: Online reading interface

4. **Templates**:
   - `google_books_search.html`: Search interface and book grid
   - `google_book_detail.html`: Book information display
   - `google_book_reader.html`: Online reading interface

5. **URLs** (`books/urls.py`):
   - Routes for Google Books functionality

### Data Flow

1. User searches for books
2. Service calls Google Books API
3. Results are cached and stored in database
4. Books are displayed in responsive grid
5. User can view details or read online
6. Online reader embeds Google's web reader

## 🔧 Configuration

### Settings (`bookstore/settings.py`)

```python
# Google Books API Configuration
GOOGLE_BOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY', '')
GOOGLE_BOOKS_API_BASE_URL = 'https://www.googleapis.com/books/v1'
```

### Caching

- Search results: 1 hour
- Book details: 2 hours
- Reduces API calls and improves performance

### Rate Limiting

Google Books API has quotas:
- 1,000 requests per day (free tier)
- 100,000 requests per day (paid tier)

## 🎨 Customization

### Styling

The templates use Bootstrap 5 and Font Awesome icons. You can customize:

- Colors and themes in CSS
- Layout and spacing
- Icon choices
- Responsive breakpoints

### Search Categories

Modify featured book categories in `books/services.py`:

```python
featured_queries = [
    'your_category_1',
    'your_category_2',
    # Add more categories
]
```

### Book Display

Customize book card layout in templates:
- Cover image size
- Information displayed
- Button styles
- Grid layout

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify the API key is correct
   - Check if Google Books API is enabled
   - Ensure environment variable is set

2. **No Books Found**
   - Check search terms
   - Verify API is responding
   - Check browser console for errors

3. **Online Reading Not Available**
   - Not all books have web reader access
   - Check if `web_reader_url` exists
   - Try different books

4. **Performance Issues**
   - Check caching is working
   - Monitor API call frequency
   - Consider increasing cache timeouts

### Debug Mode

Enable Django debug mode to see detailed error messages:

```python
DEBUG = True
```

### Logging

Check Django logs for API errors and debugging information.

## 📱 Mobile Support

The interface is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🔒 Security

- API keys are stored in environment variables
- No sensitive data exposed in templates
- Input validation and sanitization
- Rate limiting through Google's API quotas

## 📈 Performance

- Intelligent caching reduces API calls
- Database storage for frequently accessed books
- Responsive design for fast loading
- Optimized queries and pagination

## 🚀 Future Enhancements

Potential improvements:
- User reading lists and favorites
- Reading progress tracking
- Book recommendations
- Social sharing features
- Advanced search filters
- Multiple language support

## 📞 Support

If you encounter issues:

1. Check this documentation
2. Review Django logs
3. Verify API configuration
4. Test with simple queries
5. Check Google Books API status

## 📚 Resources

- [Google Books API Documentation](https://developers.google.com/books/docs/v1/using)
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Font Awesome Icons](https://fontawesome.com/icons)

---

**Note**: This integration requires an active internet connection to access Google Books API. Offline functionality is not supported.
