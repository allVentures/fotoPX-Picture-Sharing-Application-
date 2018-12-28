from django.contrib.auth.models import User
from django.db import models

PRIVACY = (
    (1, "Global"),
    (2, "Logged"),
    (3, "OnlyMe"),
)

PICTURE_RATING = (
    (1, "*"),
    (2, "**"),
    (3, "***"),
    (4, "****"),
    (5, "*****"),
)


class Regions(models.Model):
    voivodeship_id = models.IntegerField(blank=True, null=True)
    county_id = models.IntegerField(blank=True, null=True)
    municipality_id = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.city)


class ExtendUser(models.Model):
    avatar_picture = models.ImageField(null=True)
    region = models.ForeignKey('Regions', on_delete=models.SET_NULL, null=True)
    email_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    phone_number = models.CharField(max_length=20, null=True)
    phone_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    skype = models.CharField(max_length=64, null=True)
    skype_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    instagram_id = models.CharField(max_length=64, null=True)
    instagram_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    facebook_id = models.CharField(max_length=64, null=True)
    facebook_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    website = models.URLField(null=True, max_length=128)
    website_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    about_me = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Username")
    joined = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name = 'Extended User Info'

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_date = models.DateTimeField(auto_now_add=True)


class PictureCategory(models.Model):
    category = models.CharField(max_length=64, unique=True)
    category_slug = models.CharField(max_length=64, unique=True, null=True)

    class Meta:
        verbose_name = 'Picture Categories'

    def __str__(self):
        return "%s" % (self.category)


class Picture(models.Model):
    picture = models.ImageField(max_length=160)
    picture_thumbnail = models.ImageField(null=True, max_length=160)
    th_width = models.IntegerField(null=True)
    th_height = models.IntegerField(null=True)
    title = models.CharField(max_length=160, null=True)
    description = models.TextField()
    pic_slug = models.CharField(max_length=160, null=True, unique=True)
    views = models.IntegerField(null=True, default=0)
    picture_category_id = models.ForeignKey(PictureCategory, on_delete=models.CASCADE, verbose_name="Picture Category")
    picture_user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Picture Author")
    upload_date = models.DateTimeField(auto_now_add=True)
    # EXIF data for picture
    camera_make = models.CharField(max_length=64, null=True)
    camera_model = models.CharField(max_length=64, null=True)
    lens = models.CharField(max_length=128, null=True)
    focal_length = models.IntegerField(null=True)
    ISO = models.IntegerField(null=True)
    f_stop = models.FloatField(null=True)
    shutter_speed = models.CharField(max_length=8, null=True)
    creation_date = models.DateTimeField(null=True)

    def __str__(self):
        return "%s" % (self.id)

    def author(self):
        return "%s %s" % (self.picture_user_id.first_name, self.picture_user_id.last_name)


class PictureRating(models.Model):
    rating = models.IntegerField(choices=PICTURE_RATING, null=True)
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Picture Rater")
    rating_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Picture Ratings'


class PictureComment(models.Model):
    comment = models.CharField(max_length=1024, null=True)
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Pic Commenter")
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Picture Comments'

    def commenter_name(self):
        return "%s %s" % (self.commenter.last_name, self.commenter.first_name)

    def picture_title(self):
        return "%s" % (self.picture_id)

    def picture_ids(self):
        return "%s" % (self.picture_id.id)


class Tags(models.Model):
    tag = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=128, unique=True, null=True)

    class Meta:
        verbose_name = 'Tag list'

    def __str__(self):
        return "%s" % (self.tag)


class PictureTags(models.Model):
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE, verbose_name='Pic Id')
    picture_tag = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name='Pic Tag Name')
    tag_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Picture Tags'
