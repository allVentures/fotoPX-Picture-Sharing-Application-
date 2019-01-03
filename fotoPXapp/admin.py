from django.contrib.auth.models import User, Permission, ContentType
from django.db.models import Avg, Count
from django.forms import Textarea
from django.utils.html import format_html
from fotoPXapp.models import ExtendUser, Picture, PictureCategory, PICTURE_RATING, PRIVACY, PictureComment, \
    PictureRating, PictureTags, Regions, Followers, Tags
from django.contrib import admin
from django.db import models




# ------------- InLine Models----------------

class ExtendedUserInline(admin.StackedInline):
    model = ExtendUser
    extra = 0
    readonly_fields = ["avatar"]

    def avatar(self, obj):
        return format_html('<img src="{}" style="width:280px"/>'.format(obj.avatar_picture.url))
    show_change_link = True

class PictureInline(admin.StackedInline):
    model = Picture
    extra = 0
    fields = ['title', 'picture_category_id', "pic_thumbnail", "views", "pic_rating", "pic_comments"]
    readonly_fields = ['title', "pic_thumbnail", "views",  "pic_rating", "pic_comments"]

    def pic_thumbnail(self, obj):
        return format_html('<a href="/admin/fotoPXapp/picture/{}/change"><img src="{}" style="width:280px"/></a>'.format(obj.id, obj.picture_thumbnail.url))

    def pic_rating(self, obj):
        return obj.p_rating()
    pic_rating.short_description = 'Avg Picture Rating'

    def pic_comments(self, obj):
        return obj.picturecomment_set.all().count()

    pic_comments.short_description = 'No of Comments'
    show_change_link = True

class UserCommentsInline(admin.StackedInline):
    model = PictureComment
    extra = 0
    readonly_fields = ['id', 'comment', "picture_id", "comment_date", "pic_thumbnail"]
    ordering = ["-comment_date"]
    show_change_link = True

    def pic_thumbnail(self, obj):
        return format_html('<img src="{}" style="width:150px"/>'.format(obj.picture_id.picture_thumbnail.url))

# ------------- Standard Models----------------
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'is_active', 'date_joined')
    ordering = ['id']
    list_filter = ('id', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    save_on_top = True
    inlines = [ExtendedUserInline, PictureInline, UserCommentsInline]


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
    list_display = (
        'id', 'title', 'views', "p_rating", 'p_comments', 'picture_category_id', 'author', 'picture_user_id', 'picture',
        'upload_date', 'image_tag')
    ordering = ['id']
    list_filter = ('picture_user_id_id', 'picture_category_id', 'id')
    search_fields = ['title']
    readonly_fields = ['image_tag_big', 'p_rating', 'p_comments', 'author']
    exclude = ['th_width', 'th_height']

    def get_queryset(self, request):
        qs = super(PicturesAdmin, self).get_queryset(request)
        qs = qs.annotate(p_comments=Count('picturecomment', distinct=True), p_rating=Avg('picturerating__rating'))
        return qs

    def p_rating(self, obj):
        return round(obj.p_rating, 2)

    p_rating.admin_order_field = 'p_rating'
    p_rating.short_description = 'avg rating'

    def p_comments(self, obj):
        return obj.p_comments

    p_comments.admin_order_field = 'p_comments'
    p_comments.short_description = 'No of comments'

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width:100px"/>'.format(obj.picture_thumbnail.url))

    def image_tag_big(self, obj):
        return format_html('<img src="{}" style="width:280px"/>'.format(obj.picture_thumbnail.url))


admin.site.register(Picture, PicturesAdmin)


class PictureRatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(PictureRating, PictureRatingAdmin)


class PictureCommentAdmin(admin.ModelAdmin):
    list_display = ('picture_id_id', 'commenter', 'commenter_id', 'comment_date')
    list_filter = ('picture_id', 'commenter_id')
    ordering = ['picture_id_id']
    readonly_fields = ['pic_thumbnail']

    formfield_overrides = {
        models.CharField: {'widget': Textarea},
    }

    def pic_thumbnail(self, obj):
        return format_html('<img src="{}" style="width:250px"/>'.format(obj.picture_id.picture_thumbnail.url))


admin.site.register(PictureComment, PictureCommentAdmin)


class PictureCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category',)


admin.site.register(PictureCategory, PictureCategoryAdmin)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'p_num', 'slug')
    list_filter = ('tag', 'id')
    search_fields = ['tag', 'slug']
    ordering = ['tag']

    def get_queryset(self, request):
        qs = super(TagsAdmin, self).get_queryset(request)
        return qs.annotate(p_num=Count('picturetags'))

    def p_num(self, obj):
        return obj.p_num

    p_num.admin_order_field = 'p_num'
    p_num.short_description = "No of tagged Pictures"


admin.site.register(Tags, TagsAdmin)


class PictureTagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'picture_id_id', 'picture_tag_id', 'picture_tag', 'tag_date')
    list_filter = ['id', 'picture_id_id', 'picture_tag_id']
    ordering = ['picture_id_id', 'picture_tag_id']
    search_fields = ['picture_tag__tag']


admin.site.register(PictureTags, PictureTagsAdmin)


class RegionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'voivodeship_id', 'county_id', 'municipality_id', 'city')
    list_filter = ['city', 'municipality_id', 'county_id', 'voivodeship_id', 'id']
    ordering = ['voivodeship_id', 'county_id', 'municipality_id']
    search_fields = ['city']


admin.site.register(Regions, RegionsAdmin)
