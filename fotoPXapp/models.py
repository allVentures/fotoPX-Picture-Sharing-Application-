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


class ExtendUser(models.Model):
    avatar_picture = models.ImageField(null=True)
    region = models.ForeignKey('Regions', on_delete=models.SET_NULL, null=True)
    email_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    phone_number = models.CharField(max_length=14, null=True)
    phone_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    skype = models.CharField(max_length=64, null=True)
    skype_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    instagram_id = models.CharField(max_length=64, null=True)
    instagram_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    facebook_id = models.CharField(max_length=64, null=True)
    facebook_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    website = models.URLField(null=True)
    website_privacy = models.IntegerField(choices=PRIVACY, null=True, default=1)
    about_me = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)


class Followers(models.Model):
    follower = models.ManyToManyField(User)
    following_date = models.DateTimeField(auto_now_add=True)


class PictureCategory(models.Model):
    category = models.CharField(max_length=64)


class Picture(models.Model):
    picture = models.ImageField()
    pic_thumb = models.ImageField()
    title = models.CharField(max_length=160, null=True)
    description = models.TextField()
    views = models.IntegerField(null=True, default=0)
    picture_category_id = models.ForeignKey(PictureCategory, on_delete=models.CASCADE)
    picture_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    # EXIF data for picture
    camera_make = models.CharField(max_length=64, null=True)
    lens = models.CharField(max_length=64, null=True)
    focal_length = models.IntegerField(null=True)
    ISO = models.IntegerField(null=True)
    f_stop = models.FloatField(null=True)
    shutter_speed = models.FloatField(null=True)


class PictureRating(models.Model):
    rating = models.IntegerField(choices=PICTURE_RATING, null=True)
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_date = models.DateTimeField(auto_now_add=True)


class PictureComment(models.Model):
    comment = models.CharField(max_length=1024, null=True)
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)

class Tags(models.Model):
    tag = models.CharField(max_length=64)

class PictureTags(models.Model):
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE)
    picture_tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    tag_date = models.DateTimeField(auto_now_add=True)




# add later:
# - url slugr for Pictures/Tags/Users
