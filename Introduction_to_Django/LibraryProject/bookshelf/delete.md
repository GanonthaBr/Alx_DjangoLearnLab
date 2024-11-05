from bookshelf.models import Book

book = Book.objects.get(pk=id)
book.delete()

Remove one book with the given id
