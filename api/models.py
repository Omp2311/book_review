from django.db import models

# Create your models here.
from django.utils.text import slugify

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13)
    book_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    soft_copy = models.FileField(upload_to='books/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def save(self, *args, **kwargs):
        if not self.book_code:
            last_book = Book.objects.order_by('-id').first()
            next_number = 1 if not last_book else last_book.id + 1
            self.book_code = f"BOOK-{str(next_number).zfill(4)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review of {self.book.title} by {self.reviewer_name}'