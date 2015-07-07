from django.conf.urls import patterns, include, url

import books.views

urlpatterns = patterns('',
    url(r'^$', books.views.BookListView.as_view(), name='book-list'),
)