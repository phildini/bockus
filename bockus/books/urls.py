from django.conf.urls import patterns, include, url

import books.views

urlpatterns = patterns('',
    url(r'^$', books.views.BookListView.as_view(), name='book-list'),
    url(
        r'^(?P<pk>\d+)/$',
        books.views.BookView.as_view(),
        name='book-detail',
    ),
    url(
        r'^(?P<pk>\d+)/send/$',
        books.views.SendBookView.as_view(),
        name='book-send',
    )
)