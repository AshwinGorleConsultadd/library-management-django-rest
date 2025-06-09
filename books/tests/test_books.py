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
def create_user(db):
    return User.objects.create_user(username="testuser", password="pass")


@pytest.fixture
def create_book(db):
    return Book.objects.create(
        title="Borrowable Book", author="Author", total_copies=5, borrowed_copies=0
    )


@pytest.fixture
def create_borrow_record(db, create_user, create_book):
    due_date = timezone.now().date() + timedelta(days=5)
    return Borrow.objects.create(
        user=create_user,
        book=create_book,
        borrow_date=timezone.now().date(),
        due_date=due_date
    )


# ---------- TEST CASES ---------- #

@pytest.mark.django_db
def test_borrow_book(create_user, create_book):
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("borrow-book")
    payload = {"book": create_book.id}

    response = client.post(url, data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert Borrow.objects.count() == 1

    borrow = Borrow.objects.first()
    assert borrow.book == create_book
    assert borrow.user == create_user


@pytest.mark.django_db
def test_return_book_on_time(create_user, create_borrow_record):
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("return-book", args=[create_borrow_record.id])
    response = client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Book returned successfully."
    assert response.data["fine"] == 0


@pytest.mark.django_db
def test_return_book_with_fine(create_user, create_borrow_record):
    client = APIClient()
    client.force_authenticate(user=create_user)

    # Make the book overdue
    create_borrow_record.due_date = timezone.now().date() - timedelta(days=3)
    create_borrow_record.save()

    url = reverse("return-book", args=[create_borrow_record.id])
    response = client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["fine"] == 30  # 3 days * ₹10


@pytest.mark.django_db
def test_return_book_twice(create_user, create_borrow_record):
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("return-book", args=[create_borrow_record.id])

    # First return
    client.post(url)

    # Second return attempt
    response = client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["message"] == "Book already returned."


@pytest.mark.django_db
def test_return_invalid_borrow(create_user):
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("return-book", args=[999])  # Invalid ID
    response = client.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "error" in response.data


@pytest.mark.django_db
def test_borrow_history(create_user, create_borrow_record):
    client = APIClient()
    client.force_authenticate(user=create_user)

    url = reverse("borrow-history")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) >= 1
    # assert response.data[0]["book"]["id"] == create_borrow_record.book.id
    assert response.data[0]["book_title"] == create_borrow_record.book.title

