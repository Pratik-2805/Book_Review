from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import Books, Review
from .serializers import BookSerializer, ReviewSerializer

# POST /books, GET /books (with pagination and filtering)
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'genre']
    ordering_fields = ['title', 'author', 'price']

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get('author')
        genre = self.request.query_params.get('genre')
        if author:
            queryset = queryset.filter(author__icontains=author)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

# GET /books/:id (details, avg rating, paginated reviews)
class BookRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        # Add paginated reviews
        reviews = instance.reviews.all()
        page = self.request.query_params.get('page', 1)
        page_size = 5
        start = (int(page) - 1) * page_size
        end = start + page_size
        reviews_page = reviews[start:end]
        data['reviews'] = ReviewSerializer(reviews_page, many=True).data
        data['reviews_count'] = reviews.count()
        data['average_rating'] = instance.average_rating()
        return Response(data)

# POST /books/:id/reviews (one per user per book)
class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs['pk']
        user = self.request.user
        book = Books.objects.get(pk=book_id)
        if Review.objects.filter(book=book, user=user).exists():
            raise PermissionDenied('You have already reviewed this book.')
        serializer.save(book=book, user=user)

# PUT, DELETE /reviews/:id (user can update/delete own review)
class ReviewUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('You can only modify your own reviews.')
        return obj

# GET /search (search by title or author, partial, case-insensitive)
class BookSearchAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Books.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)) 