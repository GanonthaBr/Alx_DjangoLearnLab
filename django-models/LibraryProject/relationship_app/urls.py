from django.urls import path
from . import views
from .views import list_books
from .views import LibraryDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/',list_books,name='book-list'),
    path('library/<int:pk>',LibraryDetailView.as_view(),name='library-details'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('admin/',views.admin_view,name='admin-view'),
    path('member/',views.admin_view,name='member-view'),
    path('librarian/',views.admin_view,name='librarian-view'),
    path('add/',views.add_book_view,name='add-book'),
    path('update/<int:pk>',views.update_book_view,name='update-book'),
    path('add/<int:pk>',views.delete_book_view,name='delete-book'),
    
]