from django.contrib import admin
from django.contrib.auth.models import User
from fotoPXapp.models import ExtendUser, Picture, PictureCategory, PICTURE_RATING, PRIVACY, PictureComment, \
    PictureRating, PictureTags, Regions, Followers, Tags
from jet.admin import CompactInline


# some CSS classsed for the (Jets) admin panel have been rewwritten:
# /home/paul/.local/lib/python3.6/site-packages/jet/static/jet/css/themes/default/base.css

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'last_login')
    ordering = ['id']
    list_filter = ('id', 'username', 'first_name', 'last_name')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class UserAdminExtended(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'name', 'city', 'joined')
    ordering = ['user_id']
    list_filter = ('user_id', 'user', 'skype', 'facebook_id')
    # search_fields = ('user', 'skype')


admin.site.register(ExtendUser, UserAdminExtended)

class PicturesAdmin(admin.ModelAdmin):
    pass
    list_display = ('title', 'views', 'picture_category_id', 'author', 'picture',)
    # ordering = ['id']
    list_filter = ('title', 'picture_user_id_id')
    # fields = ('photo', 'name', 'owner')
    # readonly_fields = ('grades_list', )


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
    list_display = ('id', 'tag')
    # search_fields = ('tag',)
    list_filter = ('tag',)


admin.site.register(Tags, TagsAdmin)


class PictureTagsAdmin(admin.ModelAdmin):
    pass


admin.site.register(PictureTags, PictureTagsAdmin)


class RegionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'voivodeship_id', 'county_id', 'municipality_id', 'city')
    list_filter = ('id', 'voivodeship_id', 'county_id', 'municipality_id', 'city')


admin.site.register(Regions, RegionsAdmin)
