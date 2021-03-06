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
    url(
        r'^merge/$',
        books.views.MergeBookView.as_view(),
        name='books-merge',
    ),
    url(r'^shelve/$',
        books.views.ShelveBooksView.as_view(),
        name='books-shelve',
    ),
    url(r'^delete/$',
        books.views.DeleteBooksView.as_view(),
        name='books-delete',
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

shelfpatterns = patterns('',
    url(r'^$', books.views.ShelfListView.as_view(), name='shelf-list'),
    url(
        r'^(?P<pk>\d+)/$',
        books.views.ShelfView.as_view(),
        name='shelf-detail',
    ),
    url(
        r'^new$',
        books.views.CreateShelfView.as_view(),
        name='shelf-create',
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        books.views.EditShelfView.as_view(),
        name='shelf-edit',
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        books.views.DeleteShelfView.as_view(),
        name='shelf-delete',
    ),
    url(
        r'^lastweek$',
        books.views.LastWeekShelfView.as_view(),
        name='shelf-last-week',
    ),
    url(
        r'^lastmonth$',
        books.views.LastMonthShelfView.as_view(),
        name='shelf-last-month',
    ),
)