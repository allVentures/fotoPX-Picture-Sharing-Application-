from django.contrib import admin
from django.contrib.auth.models import User
from fotoPXapp.models import ExtendUser, Picture, PictureCategory, PICTURE_RATING, PRIVACY, PictureComment, \
    PictureRating, PictureTags, Regions, Followers, Tags
from jet.admin import CompactInline


class PicturesAdmin(admin.ModelAdmin):
    pass
    # fields = ('photo', 'name', 'owner')
    # readonly_fields = ('grades_list', )
    list_display = ('title', 'picture_category_id', 'author', 'picture',)
    # ordering = ['id']
    # list_filter = ('first_name', 'last_name', 'school_class')
    # actions = [remove_grades, ]


admin.site.register(Picture, PicturesAdmin)


class UserAdminExtended(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'name', 'city', 'joined')
    ordering = ['user_id']
    list_filter = ('user', 'skype', 'facebook_id')
    # search_fields = ('user', 'skype')


admin.site.register(ExtendUser, UserAdminExtended)


class PictureRatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(PictureRating, PictureRatingAdmin)


class PictureCommentAdmin(admin.ModelAdmin):
    pass


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
