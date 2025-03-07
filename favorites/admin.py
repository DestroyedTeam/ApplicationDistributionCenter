from django.contrib import admin

from favorites import models


# Register your models here.
@admin.register(models.Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ["id", "visitor", "correlation_article", "correlation_software", "created_time"]
