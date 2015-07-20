from django.conf.urls import patterns, include, url

import books.views

bookpatterns = patterns('',
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
        r'^(?P<pk>\d+)/edit/$',
        books.views.EditBookView.as_view(),
        name='book-edit',
    ),
    url(
        r'^(?P<pk>\d+)/delete/$',
        books.views.DeleteBookView.as_view(),
        name='book-delete',
    ),
    url(
        r'^import/$',
        books.views.ImportBooksView.as_view(),
        name='books-import',
    ),
)

seriespatterns = patterns('',
    url(r'^$', books.views.SeriesListView.as_view(), name='series-list'),
    url(
        r'^(?P<pk>\d+)/$',
        books.views.SeriesView.as_view(),
        name='series-detail',
    ),
    url(
        r'^new$',
        books.views.CreateSeriesView.as_view(),
        name='series-create',
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        books.views.EditSeriesView.as_view(),
        name='series-edit',
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        books.views.DeleteSeriesView.as_view(),
        name='series-delete',
    ),
)