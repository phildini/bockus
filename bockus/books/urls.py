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
        r'^(?P<pk>\d+)/send/(?P<reader>\d+)/$',
        books.views.SendBookView.as_view(),
        name='book-send',
    ),
    # url(
    #     r'^new$',
    #     books.views.CreateBookView.as_view(),
    #     name='book-new',
    # ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        books.views.EditBookView.as_view(),
        name='book-edit',
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        books.views.DeleteBookView.as_view(),
        name='book-delete',
    ),
)