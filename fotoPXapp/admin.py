from django.contrib import admin
from django.contrib.auth.models import User, Permission, ContentType
from fotoPXapp.models import ExtendUser, Picture, PictureCategory, PICTURE_RATING, PRIVACY, PictureComment, \
    PictureRating, PictureTags, Regions, Followers, Tags

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'is_active', 'date_joined')
    ordering = ['id']
    list_filter = ('id', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name', 'email')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'content_type_id', 'codename')
    ordering = ['id']
    search_fields = ['name']
    list_filter = ('content_type', 'name', 'id')


admin.site.register(Permission, PermissionsAdmin)


class ContentTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(ContentType, ContentTypeAdmin)


class UserAdminExtended(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'user', 'name', 'region', 'joined')
    ordering = ['user_id']
    list_filter = ('id', 'user_id', 'skype', 'facebook_id')


admin.site.register(ExtendUser, UserAdminExtended)


class PicturesAdmin(admin.ModelAdmin):
    model = Picture
    list_display = (
        'id', 'title', 'views', "p_rating", 'picture_category_id', 'author', 'picture_user_id', 'picture', 'upload_date')
    ordering = ['id']
    list_filter = ('picture_user_id_id', 'picture_category_id', 'id')
    search_fields = ['title']
    readonly_fields = ['p_rating']


admin.site.register(Picture, PicturesAdmin)


class PictureRatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(PictureRating, PictureRatingAdmin)


class PictureCommentAdmin(admin.ModelAdmin):
    list_display = ('picture_id_id', 'commenter', 'commenter_id', 'comment_date')
    list_filter = ('picture_id', 'commenter_id')
    ordering = ['picture_id_id']


admin.site.register(PictureComment, PictureCommentAdmin)


class PictureCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category',)


admin.site.register(PictureCategory, PictureCategoryAdmin)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_filter = ('tag', 'id')
    search_fields = ['tag', 'slug']
    ordering = ['tag']


admin.site.register(Tags, TagsAdmin)

class PictureTagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'picture_id_id', 'picture_tag_id', 'picture_tag', 'tag_date')
    list_filter = ['id', 'picture_id_id', 'picture_tag_id']
    ordering = ['picture_id_id', 'picture_tag_id']

admin.site.register(PictureTags, PictureTagsAdmin)


class RegionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'voivodeship_id', 'county_id', 'municipality_id', 'city')
    list_filter = ['city', 'municipality_id', 'county_id', 'voivodeship_id', 'id']
    ordering = ['voivodeship_id', 'county_id', 'municipality_id']
    search_fields = ['city']


admin.site.register(Regions, RegionsAdmin)
