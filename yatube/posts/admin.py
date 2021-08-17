from django.contrib import admin

from .models import Avatar, Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'description')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text')


class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth')


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Avatar, AvatarAdmin)
