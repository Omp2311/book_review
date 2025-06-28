from django.test import TestCase, Client
from django.urls import reverse
from api.models import Book
from django.core.cache import cache
class BookListCacheMissTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123"
        )
        cache.clear()

    def test_book_list_cache_miss(self):
        # Ensure cache is empty
        cache_key = 'book_list'
        self.assertIsNone(cache.get(cache_key))

        # Make a request to the book list view
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)

        # Check that the cache has been populated
        books = cache.get(cache_key)
        self.assertIsNotNone(books)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Test Book")