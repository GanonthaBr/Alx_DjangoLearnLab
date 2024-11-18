from django.urls import path
from . import views
from .views import list_books
from .views import LibraryDetailView
from .views import LoginView
from .views import LogoutView
from django.contrib.auth import views as auth_views

# "LogoutView.as_view(template_name=", "LoginView.as_view(template_name="
urlpatterns = [
    path('books/',list_books,name='book-list'),
    path('library/<int:pk>',LibraryDetailView.as_view(),name='library-details'),
    path('register/',views.register,name='register'),
    path('logout/',LogoutView.as_view(templage_name=""),name='logout'),
    path('logout/',LoginView.as_view(templage_name=""),name='login'),
    path('admin/',views.admin_view,name='admin-view'),
    path('member/',views.admin_view,name='member-view'),
    path('librarian/',views.admin_view,name='librarian-view'),
    path('add/',views.add_book_view,name='add-book'),
    path('update/<int:pk>',views.update_book_view,name='update-book'),
    path('add/<int:pk>',views.delete_book_view,name='delete-book'),
    
]