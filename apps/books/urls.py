from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="login_reg"),
    url(r'^login', views.login, name="login"),
    url(r'^register', views.register, name="register"),
    url(r'^logout', views.logout, name="logout"),
    url(r'^users/(?P<user_id>[0-9]*)', views.show_user, name="users_show"),
    url(r'^books$', views.books, name="books_index"),
    url(r'^books/add$', views.add_book, name="books_add"),
    url(r'^books/create$', views.create_book, name="books_create"),
    url(r'^books/review/(?P<book_id>[0-9]*)$', views.add_book_review, name="books_review"),
    url(r'^books/(?P<book_id>[0-9]*)', views.show_book, name="books_show"),
    url(r'^books/(?P<review_id>[0-9]*)/delete$', views.delete_review, name="reviews_delete"),
]
