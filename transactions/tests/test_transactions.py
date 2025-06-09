import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book
from transactions.models import Borrow
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    return User.objects.create_user(username="user", password="pass")


@pytest.fixture
def auth_client(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    return api_client


@pytest.fixture
def book():
    return Book.objects.create(title="Borrowable Book", author="Author", total_copies=5, borrowed_copies=0)


@pytest.fixture
def borrow_record(create_user, book):
    due = timezone.now().date() + timedelta(days=5)
    return Borrow.objects.create(user=create_user, book=book, borrow_date=timezone.now().date(), due_date=due)


@pytest.mark.django_db
def test_return_book_on_time(auth_client, borrow_record):
    url = reverse("return-book", args=[borrow_record.id])
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Book returned successfully."
    assert response.data["fine"] == 0


@pytest.mark.django_db
def test_return_book_with_fine(auth_client, borrow_record):
    # Simulate an overdue book
    borrow_record.due_date = timezone.now().date() - timedelta(days=3)
    borrow_record.save()

    url = reverse("return-book", args=[borrow_record.id])
    response = auth_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["fine"] == 30  # 3 days * ₹10


@pytest.mark.django_db
def test_return_book_twice(auth_client, borrow_record):
    url = reverse("return-book", args=[borrow_record.id])
    # First return
    auth_client.post(url)
    # Second return attempt
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "Book already returned."


@pytest.mark.django_db
def test_return_invalid_borrow(auth_client):
    url = reverse("return-book", args=[999])  # Nonexistent record
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_borrow_history(auth_client, borrow_record):
    url = reverse("borrow-history")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_borrow_book(auth_client, book):
    url = reverse("borrow-book")
    payload = {"book": book.id}

    response = auth_client.post(url, data=payload)

    # assert response.status_code == status.HTTP_201_CREATED
    # assert Borrow.objects.count() == 1
    # borrow = Borrow.objects.first()
    # assert borrow.book == book
    # assert borrow.user.username == "testuser"