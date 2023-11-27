from django.contrib import admin

import favorites.models


# Register your models here.
@admin.register(favorites.models.Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ['id']
