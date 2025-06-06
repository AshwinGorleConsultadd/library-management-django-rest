# 📚 Django Library Management System – Short Notes by Ashwin
These notes explain the entire Django + DRF flow with definitions and examples. Suitable for beginners, especially those coming from Node.js or FastAPI backgrounds.

---

## 🔧 1. Project and App Setup

### ➤ What is this?
This step sets up your Django project and the app where your business logic (library system) lives.

### ✅ Commands:
```bash
django-admin startproject library_project
cd library_project
python manage.py startapp books
```

### ✅ Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',  # Django REST framework
    'books',           # Our books app
]
```

---

##  2. Routing

### ➤ What is Routing?
Routes (URLs) tell Django what to do when a specific path is visited.

### ✅ In `library_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', include('books.urls')),  # Directs to app-level URLs
]
```

---

## 3. Models

### ➤ What is a Model?
A model is a Python class that defines your database table structure. Each model = one table.

### ✅ In `books/models.py`
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    total_copies = models.IntegerField()
    borrowed_copies = models.IntegerField(default=0)

    def available_copies(self):
        return self.total_copies - self.borrowed_copies

    def __str__(self):
        return self.title
```

---

## 4. Migrations

### ➤ What are Migrations?
They sync your Python models with the database.

### ✅ Commands:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5. Serializers

### ➤ What is a Serializer?
Serializers convert model instances to JSON and vice versa.

### ✅ In `books/serializers.py`
```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    available_copies = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
```

---

## 👀 6. Views

### ➤ What is a View?
A view handles the logic of the request — how to fetch, create, update, or delete data.

### ✅ In `books/views.py`
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookListCreate(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return None

    def get(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({'error': 'Book not found'}, status=404)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({'error': 'Book not found'}, status=404)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({'error': 'Book not found'}, status=404)
        book.delete()
        return Response(status=204)
```

---

## 7. URL Patterns

### ➤ What are URL patterns?
They connect endpoints (e.g. `/api/books/`) to their view classes.

### ✅ In `books/urls.py`
```python
from django.urls import path
from .views import BookListCreate, BookDetail

urlpatterns = [
    path('', BookListCreate.as_view(), name='book-list-create'),
    path('<int:pk>/', BookDetail.as_view(), name='book-detail'),
]
```

---

## 8. Sample Request/Response

### ➤ POST `/api/books/` (Create a Book)
```json
{
    "title": "Harry Potter",
    "author": "J.K. Rowling",
    "total_copies": 10,
    "borrowed_copies": 2
}
```

### ➤ Sample JSON Response
```json
{
    "id": 1,
    "title": "Harry Potter",
    "author": "J.K. Rowling",
    "total_copies": 10,
    "borrowed_copies": 2,
    "available_copies": 8
}
```

---

## 9. Authentication (JWT with DRF)

### ➤ What is JWT Auth?
JWT is a secure way to authenticate users using tokens instead of sessions.

### ✅ Install:
```bash
pip install djangorestframework-simplejwt
```

### ✅ In `settings.py`
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

---

## 10. RBAC – Role-Based Access Control

### ➤ What is RBAC?
Restrict access to specific endpoints based on user roles (admin, student, etc).

### ✅ Example Permission Class
```python
from rest_framework.permissions import IsAuthenticated, BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class BookCreateOnlyAdmin(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
```

---

## ✅ 11. Example – Borrow Book Logic

### ➤ In `views.py`
```python
class BorrowBook(APIView):
    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        if book.available_copies() <= 0:
            return Response({'error': 'No copies available'}, status=400)
        book.borrowed_copies += 1
        book.save()
        return Response({'message': 'Book borrowed'})
```

---

## Final Flow Summary

### ➤ What happens when a request is made?
```
Client → URL (Router) → View → Serializer → Model → DB → Response
```

This is how Django REST Framework handles API requests internally.
