from django.urls import path
from . import api_views

urlpatterns = [
    path('books/', api_views.BookListCreateAPIView.as_view(), name='api-book-list-create'),
    path('books/<int:pk>/', api_views.BookRetrieveAPIView.as_view(), name='api-book-detail'),
    path('books/<int:pk>/reviews/', api_views.ReviewCreateAPIView.as_view(), name='api-review-create'),
    path('reviews/<int:pk>/', api_views.ReviewUpdateDeleteAPIView.as_view(), name='api-review-update-delete'),
    path('search/', api_views.BookSearchAPIView.as_view(), name='api-book-search'),
] 