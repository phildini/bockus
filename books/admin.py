from django.contrib import admin

from .models import Book, BookFileVersion, Series

admin.site.register(Book)
admin.site.register(BookFileVersion)
admin.site.register(Series)
