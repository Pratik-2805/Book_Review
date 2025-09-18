from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Books, Review
from .serializers import UserSerializer, LoginSerializer, BookSerializer, ReviewSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ReviewForm, BookForm
from django.db.models import Count
import random
from django.core.paginator import Paginator


# # Signup
# class SignupAPI(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'status': 201,
#                 'message': 'User created successfully',
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response({'status': 400, 'message': 'User creation failed', 'data': serializer.errors})

# # Login
# class LoginAPI(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(username=email, password=password)
#             # try:
#             #     user = User.objects.get(email=email)
#             # except User.DoesNotExist:
#             #     return Response({'status': 400, 'message': 'Invalid credentials'})
#             # user = authenticate(email=email, password=password)
#             if user is not None:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'status': 200,
#                     'message': 'Login successful',
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 })
#             return Response({'status': 400, 'message': 'Invalid credentials'})
#         return Response({'status': 400, 'message': 'Invalid data', 'data': serializer.errors})

# # Book CRUD
# class BookListCreate(generics.ListCreateAPIView):
#     template_name = 'books/book_list.html'
#     model = Books

#     queryset = Books.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'author', 'genre']

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

# class BookDetail(generics.RetrieveAPIView):
#     queryset = Books.objects.all()
#     serializer_class = BookSerializer

# # Review CRUD
# class ReviewCreate(generics.CreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class ReviewUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)

# # Search
# class BookSearch(generics.ListAPIView):
#     queryset = Books.objects.all()
#     serializer_class = BookSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title', 'author']
#     permission_classes = [AllowAny]

# def index(request):
#     return render(request, 'books/base.html')


def home(request):
    all_books = list(Books.objects.all())
    featured_books = random.sample(all_books, min(4, len(all_books))) if all_books else []
    
    # Get featured Google Books
    try:
        service = GoogleBooksService()
        google_featured_books = service.get_featured_books(max_results=4)
    except:
        google_featured_books = []
    
    return render(request, 'books/home.html', {
        'featured_books': featured_books,
        'google_featured_books': google_featured_books
    })

def book_list(request):
    books = Books.objects.all()
    search = request.GET.get('search', '').strip()
    author = request.GET.get('author', '')
    genre = request.GET.get('genre', '')
    if search:
        books = books.filter(
            title__icontains=search
        ) | books.filter(
            author__icontains=search
        ) | books.filter(
            genres__icontains=search
        )
    if author:
        books = books.filter(author__icontains=author)
    if genre:
        books = books.filter(genres__icontains=genre)

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST' and request.user.is_authenticated:
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm() if request.user.is_authenticated else None

    return render(request, 'books/book_list.html', {
        'books': page_obj,
        'form': form,
        'page_obj': page_obj,
        'author': author,
        'genre': genre,
        'search': search,
    })

def review_detail(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('review_detail', pk=book.pk)
    else:
        form = ReviewForm()
    return render(request, 'books/review_detail.html', {
        'book': book,
        'form': form,
    })

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Registration successful. Please log in.')
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'books/register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('book_list')
#             else:
#                 messages.error(request, 'Invalid credentials')
#     else:
#         form = LoginForm()
#     return render(request, 'books/login.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('book_list')  # Change 'home' to your home page name
        else:
            return render(request, 'books/login.html', {'error': 'Invalid credentials'})
    return render(request, 'books/login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'books/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'books/register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def about(request):
    return render(request, 'books/about.html')

def contact(request):
    return render(request, 'books/contact.html')

# Google Books Views
from .services import GoogleBooksService
from .models import GoogleBook
from django.core.paginator import Paginator

def google_books_search(request):
    """
    Search and display Google Books
    """
    service = GoogleBooksService()
    books = []
    total_items = 0
    error = None
    
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    
    if search_query:
        try:
            page_number = int(page_number)
            start_index = (page_number - 1) * 20
            
            result = service.search_books(search_query, max_results=20, start_index=start_index)
            books = result.get('books', [])
            total_items = result.get('total_items', 0)
            error = result.get('error')
            
        except (ValueError, TypeError):
            error = "Invalid page number"
    else:
        # Show featured books if no search query
        books = service.get_featured_books(max_results=20)
    
    # Pagination
    paginator = Paginator(books, 20)
    try:
        page_obj = paginator.page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.page(1)
    
    context = {
        'books': page_obj,
        'search_query': search_query,
        'total_items': total_items,
        'page_obj': page_obj,
        'error': error,
        'is_google_books': True
    }
    
    return render(request, 'books/google_books_search.html', context)

def google_book_detail(request, google_id):
    """
    Display detailed information about a Google Book
    """
    service = GoogleBooksService()
    book = service.get_book_details(google_id)
    
    if not book:
        messages.error(request, 'Book not found or could not be retrieved.')
        return redirect('google_books_search')
    
    context = {
        'book': book,
        'is_google_book': True
    }
    
    return render(request, 'books/google_book_detail.html', context)

def google_book_reader(request, google_id):
    """
    Display the Google Book reader for online reading
    """
    service = GoogleBooksService()
    book = service.get_book_details(google_id)
    
    if not book:
        messages.error(request, 'Book not found or could not be retrieved.')
        return redirect('google_books_search')
    
    if not book.web_reader_url:
        messages.warning(request, 'This book is not available for online reading.')
        return redirect('google_book_detail', google_id=google_id)
    
    context = {
        'book': book,
        'is_google_book': True
    }
    
    return render(request, 'books/google_book_reader.html', context)