from django.contrib import admin

from .models import Library, Librarian, LibraryImport

admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(LibraryImport)
