from django.conf.urls import url
from . import views

urlpatterns = [
    # direct to index page
    url(r'^$', views.index),
    # dirext to process_login def
    url(r'^process_login$', views.process_login),
    # direct to welcome page
    url(r'^books$', views.books),
    # direct to create_book def
    url(r'^create_book$', views.create_book),
    # direct to edit page
    url(r'^books/(?P<id>\d+)$', views.edit),
    # direct to edit def
    url(r'^books/(?P<id>\d+)/edit$', views.edit),
    # direct to book_info page
    url(r'^book_info/(?P<id>\d+)$', views.book_info),
    # direct to add_favorites def
    url(r'^add_favorites/(?P<id>\d+)$', views.add_favorites),
    # direct to un_favorites def
    url(r'^un_favorites/(?P<id>\d+)$', views.un_favorites),
    # direct to delete def
    url(r'^books/(?P<id>\d+)/delete$', views.delete),
    # log out user from their page
    url(r'^logout$', views.logout),
]