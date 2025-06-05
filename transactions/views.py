from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Borrow
from .serializers import BorrowSerializer, ReturnSerializer, BorrowHistorySerializer
from datetime import date
from rest_framework.views import APIView
from . import permissions
from django.utils import timezone

class BorrowBookView(generics.CreateAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReturnBookView(APIView):


    def post(self, request, pk):

        try:
            borrow = Borrow.objects.get(pk=pk, user=request.user)
        except Borrow.DoesNotExist:
            return Response({"error": "Borrow record not found"}, status=status.HTTP_404_NOT_FOUND)

        if borrow.return_date:
            return Response({"message": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST)

        borrow.return_date = timezone.now().date()

        # Calculate fine if overdue
        if borrow.due_date and borrow.return_date > borrow.due_date:
            delta = borrow.return_date - borrow.due_date
            borrow.fine = delta.days * 10  # ₹10 fine per day

        borrow.save()
        return Response({
            "message": "Book returned successfully.",
            "fine": borrow.fine
        }, status=status.HTTP_200_OK)

class BorrowHistoryView(generics.ListAPIView):
    serializer_class = BorrowHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user)

