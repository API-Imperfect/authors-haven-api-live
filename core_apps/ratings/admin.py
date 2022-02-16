from django.contrib import admin

from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ["article", "rated_by", "value"]


admin.site.register(Rating, RatingAdmin)
