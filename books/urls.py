from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    # path('signup/', SignupAPI.as_view(), name='signup'),
    # path('login/', LoginAPI.as_view(), name='login'),
    # path('books/', BookListCreate.as_view(), name='books'),
    # path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    # path('books/<int:pk>/reviews/', ReviewCreate.as_view(), name='review-create'),
    # path('reviews/<int:pk>/', ReviewUpdateDelete.as_view(), name='review-update-delete'),
    # path('search/', BookSearch.as_view(), name='book-search'),
    
]

urlpatterns += [
    path('', home, name='home'),
    path('book_list/', book_list, name='book_list'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('api/', include('books.api_urls')),
    
    # Google Books URLs
    path('google-books/', views.google_books_search, name='google_books_search'),
    path('google-books/book/<str:google_id>/', views.google_book_detail, name='google_book_detail'),
    path('google-books/book/<str:google_id>/read/', views.google_book_reader, name='google_book_reader'),
]