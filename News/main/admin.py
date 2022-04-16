from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'article', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'content', 'news_site', 'date_published', 'date_modified', 'image', 'summary',)
    list_filter = ('date_published', 'title', 'news_site',)
    search_fields = ('title', 'url', 'news_site', 'summary',)
    actions = ['approve_articles']

    def approve_articles(self, request, queryset):
        queryset.update(active=True)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'profile_image', 'date_of_birth', 'user')
    list_filter = ('email', 'first_name', 'last_name', 'date_of_birth')
    search_fields = ('email', 'first_name', 'last_name', 'date_of_birth')


admin.site.register(NewsSite)
