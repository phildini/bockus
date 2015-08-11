from django.contrib import admin

from .models import (
    Book,
    BookFileVersion,
    BookEmail,
    Series,
)

admin.site.register(Book)
admin.site.register(BookFileVersion)
admin.site.register(BookEmail)
admin.site.register(Series)
