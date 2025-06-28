from django.test import TestCase, Client
from django.urls import reverse
from .models import Book, Review
from django.core.cache import cache
class BookListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123"
        )

    def test_book_list_view(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertTemplateUsed(response, 'book_list.html')

class BookReviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123"
        )
        self.review = Review.objects.create(
            book=self.book,
            reviewer_name="Test Reviewer",
            rating=5,
            comment="Great book!"
        )

    def test_book_review_view(self):
        response = self.client.get(reverse('book_review', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertContains(response, "Great book!")
        self.assertTemplateUsed(response, 'book_review.html')

    def test_book_review_post(self):
        response = self.client.post(reverse('book_review', args=[self.book.id]), {
            'reviewer_name': 'New Reviewer',
            'rating': 4,
            'comment': 'Nice book!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)

