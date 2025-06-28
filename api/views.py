from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
# Create your views here.
from .models import Book,Review
from django.contrib import messages
def dashboard(request):
    books = Book.objects.all().order_by('-created_at')
    context = {
        'total_books': books.count(),
        'available_stock': books.filter(stock__gt=0).count(),
        'recent_books': books[:5]
    }
    return render(request, 'dashboard.html', context)

def book(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        book = Book(
            title=data.get('title'),
            author=data.get('author'),
            isbn=data.get('isbn'),
            category=data.get('category'),
            language=data.get('language'),
            publisher=data.get('publisher'),
            published_date=data.get('published_date') or None,
            price=data.get('price') or None,
            stock=data.get('stock') or 0,
            description=data.get('description'),
            cover_image=files.get('cover_image'),
            soft_copy=files.get('soft_copy')
        )
        book.save()
        return redirect('list')

    books = Book.objects.all().order_by('-id')[:5]

    return render(request, 'add_book.html', {'books': books})

def book_list(request):
    cache_key = 'book_list'
    books = cache.get(cache_key)
    if books is None:
        books = Book.objects.all()
        cache.set(cache_key, books, timeout=60*1)
    return render(request, 'book_list.html', {'books': books})
    
def book_grid(request):
    books = Book.objects.all()
    return render(request, 'book_grid.html', {'books': books})


def book_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        name = request.POST.get('reviewer_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if name and rating and comment:
            Review.objects.create(book=book, reviewer_name=name, rating=rating, comment=comment)
            messages.success(request, "Thank you for your review!")
            return redirect('book_review', book_id=book.id)
        else:
            messages.error(request, "Please fill all fields.")

    return render(request, 'book_review.html', {
        'book': book,
        'reviews': reviews
    })
    