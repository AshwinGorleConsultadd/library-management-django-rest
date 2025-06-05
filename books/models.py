from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    borrowed_copies = models.PositiveIntegerField(default=0)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Update available copies automatically
        self.available_copies = self.total_copies - self.borrowed_copies
        super().save(*args, **kwargs)
