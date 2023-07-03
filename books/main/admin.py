from django.contrib import admin
from django.utils.html import mark_safe

from .models import Book, Comment


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'published_at',
        'comments_count',
        'is_achieved'
    )
    search_fields = ('name',)
    list_editable = (
        'name',
        'is_achieved'
    )

    def comments_count(self, obj):
        return obj.comments.count()


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'book'
    )
    list_filter = (
        'author',
        'book'
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Comment, CommentAdmin)
