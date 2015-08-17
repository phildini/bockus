from django.contrib import admin

from .models import (
    Book,
    BookFileVersion,
    BookEmail,
    BookOnShelf,
    Series,
    Shelf,
)

admin.site.register(Book)
admin.site.register(BookFileVersion)
admin.site.register(BookEmail)
admin.site.register(Series)
admin.site.register(Shelf)
admin.site.register(BookOnShelf)
