from django.contrib import admin
from .models import User, Books, Review, GoogleBook
from django.utils.html import format_html


# Register your models here.
admin.site.register(Books)
admin.site.register(User)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'gold_stars', 'comment', 'updated_at')

    def gold_stars(self, obj):
        return format_html(''.join([
            '<span style="color:gold;">&#9733;</span>' if i < obj.rating else '<span style="color:#ccc;">&#9733;</span>'
            for i in range(5)
        ]))
    gold_stars.short_description = 'Rating'

admin.site.register(Review, ReviewAdmin)

@admin.register(GoogleBook)
class GoogleBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors_display', 'published_date', 'average_rating', 'is_ebook', 'created_at')
    list_filter = ('is_ebook', 'published_date', 'categories', 'created_at')
    search_fields = ('title', 'authors', 'description')
    readonly_fields = ('google_id', 'created_at', 'updated_at')
    list_per_page = 25
    
    def get_authors_display(self, obj):
        return obj.get_authors_display()
    get_authors_display.short_description = 'Authors'
    
    def get_categories_display(self, obj):
        return obj.get_categories_display()
    get_categories_display.short_description = 'Categories'