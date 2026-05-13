from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:book_id>/borrow/", views.borrow_book, name="borrow_book"),
]