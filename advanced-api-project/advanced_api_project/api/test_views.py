from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from api.models import Book, Author
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status


class TestBookAPI(APITestCase):
    def setUp(self):
        # create a user for Authentication
        self.user = User.objects.create_user(username='TestUser',password='passwordTest')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        print(self.token.key)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)            #Login

        
        #create a Book
        self.author = Author.objects.create(name='Author')
        self.book = Book.objects.create(title='The Rich',author=self.author,publication_year=2012)
        self.book_url = reverse('book-detail',kwargs={'pk':self.book.id})

        # Retrieve a list of books
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)

        #test cases
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data,list)
        self.assertGreaterEqual(len(response.data),1)

        #Create a Book
    def test_create_book(self):
        url = reverse('book-create')
        data = {
            "title":'New Book',
            "author":self.author,
            "publication_year":2021
        }

        # response = self.client.post(url,data)
        response = self.client.post(url,data,format='json')
        last_book = Book.objects.last()
        last_book_title = last_book.title
        #test cases
        self.assertGreaterEqual(Book.objects.count(),1) #new book added to 1 previous
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(last_book_title,'New Book')
        
        #Retrieve a single Book
    def test_retrieve_book(self):
        response = self.client.get(self.book_url)

        #test cases
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['title'],self.book.title)

        #Delete a Book
    # def test_delete_book(self):
    #     url = reverse('book-delete')
    #     response = self.client.delete(url)


