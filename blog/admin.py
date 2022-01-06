from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from django.db import models

from django.forms import CheckboxSelectMultiple

from . models import *

# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    }

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'comment', 'article', 'question', 'news', 'date_commented')
    list_filter = ('author', 'name', 'article', 'question', 'news', 'date_commented')
    search_fields = ('name', 'email', 'author', 'comment', )

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'reply', 'comment',)
    list_filter = ('author', 'name', 'comment', 'date_replied')
    search_fields = ('name', 'email', 'author', 'reply')

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Title)
admin.site.register(Post, MyModelAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Question)
admin.site.register(News)
admin.site.register(Notification)
admin.site.register(AdminNotifications)
admin.site.register(Terms_And_Conditions)
admin.site.register(About)
admin.site.register(Contact)
admin.site.register(Community_Standards)