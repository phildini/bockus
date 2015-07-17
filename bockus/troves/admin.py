from django.contrib import admin

from .models import Trove, TroveLibrarian

admin.site.register(Trove)
admin.site.register(TroveLibrarian)
