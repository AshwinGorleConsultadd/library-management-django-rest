from django.db import models
from django.conf import settings
from books.models import Book
from datetime import date

class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def calculate_fine(self):
        if self.return_date and self.return_date > self.due_date:
            delta = (self.return_date - self.due_date).days
            return delta * 10  # ₹10 per day
        return 0