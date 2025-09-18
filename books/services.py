import requests
import json
from django.conf import settings
from django.core.cache import cache
from .models import GoogleBook
import logging

logger = logging.getLogger(__name__)

class GoogleBooksService:
    def __init__(self):
        self.api_key = settings.GOOGLE_BOOKS_API_KEY
        self.base_url = settings.GOOGLE_BOOKS_API_BASE_URL

    def search_books(self, query, max_results=20, start_index=0):
        """
        Search for books using Google Books API
        """
        cache_key = f"google_books_search_{query}_{start_index}_{max_results}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result

        try:
            params = {
                'q': query,
                'maxResults': max_results,
                'startIndex': start_index,
                'key': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/volumes", params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            books = []
            
            if 'items' in data:
                for item in data['items']:
                    book_data = self._parse_book_data(item)
                    book, created = GoogleBook.objects.get_or_create(
                        google_id=book_data['google_id'],
                        defaults=book_data
                    )
                    if not created:
                        # Update existing book with latest data
                        for key, value in book_data.items():
                            if key != 'google_id':
                                setattr(book, key, value)
                        book.save()
                    
                    books.append(book)
            
            result = {
                'books': books,
                'total_items': data.get('totalItems', 0),
                'start_index': start_index,
                'max_results': max_results
            }
            
            # Cache for 1 hour
            cache.set(cache_key, result, 3600)
            return result
            
        except requests.RequestException as e:
            logger.error(f"Google Books API request failed: {e}")
            return {'books': [], 'total_items': 0, 'error': str(e)}
        except Exception as e:
            logger.error(f"Error processing Google Books API response: {e}")
            return {'books': [], 'total_items': 0, 'error': str(e)}

    def get_book_details(self, google_id):
        """
        Get detailed information about a specific book
        """
        cache_key = f"google_book_detail_{google_id}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result

        try:
            params = {'key': self.api_key}
            response = requests.get(f"{self.base_url}/volumes/{google_id}", params=params, timeout=10)
            response.raise_for_status()
            
            book_data = self._parse_book_data(response.json())
            book, created = GoogleBook.objects.get_or_create(
                google_id=book_data['google_id'],
                defaults=book_data
            )
            
            if not created:
                # Update existing book with latest data
                for key, value in book_data.items():
                    if key != 'google_id':
                        setattr(book, key, value)
                book.save()
            
            # Cache for 2 hours
            cache.set(cache_key, book, 7200)
            return book
            
        except requests.RequestException as e:
            logger.error(f"Google Books API request failed for book {google_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing Google Books API response for book {google_id}: {e}")
            return None

    def _parse_book_data(self, item):
        """
        Parse Google Books API response into our model format
        """
        volume_info = item.get('volumeInfo', {})
        sale_info = item.get('saleInfo', {})
        
        # Extract price information
        price = None
        currency = 'USD'
        if sale_info.get('saleability') == 'FOR_SALE':
            list_price = sale_info.get('listPrice', {})
            if list_price:
                price = list_price.get('amount')
                currency = list_price.get('currencyCode', 'USD')

        # Extract image URL
        image_url = None
        if 'imageLinks' in volume_info:
            image_url = volume_info['imageLinks'].get('thumbnail') or volume_info['imageLinks'].get('smallThumbnail')

        # Extract preview and web reader URLs
        preview_url = volume_info.get('previewLink')
        web_reader_url = None
        if 'accessInfo' in item:
            web_reader_url = item['accessInfo'].get('webReaderLink')

        return {
            'google_id': item.get('id'),
            'title': volume_info.get('title', 'Unknown Title'),
            'authors': volume_info.get('authors', []),
            'description': volume_info.get('description', ''),
            'published_date': volume_info.get('publishedDate', ''),
            'page_count': volume_info.get('pageCount'),
            'categories': volume_info.get('categories', []),
            'average_rating': volume_info.get('averageRating'),
            'ratings_count': volume_info.get('ratingsCount', 0),
            'image_url': image_url,
            'preview_url': preview_url,
            'web_reader_url': web_reader_url,
            'is_ebook': volume_info.get('accessInfo', {}).get('pdf', {}).get('isAvailable', False),
            'price': price,
            'currency': currency,
        }

    def get_featured_books(self, max_results=12):
        """
        Get featured books (popular books in various categories)
        """
        featured_queries = [
            'bestseller fiction',
            'popular science books',
            'classic literature',
            'modern romance novels',
            'business books',
            'self-help books'
        ]
        
        all_books = []
        for query in featured_queries:
            result = self.search_books(query, max_results=2)
            if result['books']:
                all_books.extend(result['books'])
        
        # Remove duplicates and limit results
        unique_books = list({book.google_id: book for book in all_books}.values())
        return unique_books[:max_results]
