from django.contrib import admin

from .models import Book, BookFileVersion

admin.site.register(Book)
admin.site.register(BookFileVersion)
