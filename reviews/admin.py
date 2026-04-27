from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'sentiment', 'created_at')
    list_filter = ('sentiment', 'rating')
    search_fields = ('user__username', 'product__name', 'review_text')
