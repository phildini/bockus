"""bockus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from bockus.views import HomeView
import books.urls
from books.views import LibrarySearchView
import readers.urls

from invites.views import (
    CreateInviteView,
    AcceptInviteView,
    ChangePasswordView,
)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^set-password/$',
        ChangePasswordView.as_view(),
        name='set-password',
    ),
    url(r'^invites/add$', CreateInviteView.as_view(), name='create-invite'),
    url(
        r'^invites/accept/(?P<key>[\w-]+)/$',
        AcceptInviteView.as_view(),
        name='accept-invite',
    ),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^invitations/', include('invitations.urls', namespace='invitations')),
    url(r'^books/', include(books.urls.bookpatterns)),
    url(r'^series/', include(books.urls.seriespatterns)),
    url(r'^readers/', include(readers.urls.readerpatterns)),
    url(r'^shelves/', include(books.urls.shelfpatterns)),
    url(r'^search/', LibrarySearchView.as_view(), name='search'),
    url(r'^$', HomeView.as_view(), name='home-view'),
]
