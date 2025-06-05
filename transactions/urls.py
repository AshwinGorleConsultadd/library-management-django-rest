
from django.contrib import admin
from django.urls import path, include
from .views import BorrowBookView, ReturnBookView, BorrowHistoryView
urlpatterns = [
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
    path('history/', BorrowHistoryView.as_view(), name='borrow-history')
]