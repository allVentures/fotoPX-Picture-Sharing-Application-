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
    voivodeship_id = models.IntegerField(null=True, blank=True)
    county_id = models.IntegerField(null=True, blank=True)
    municipality_id = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'Regions'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return "%s" % (self.city)


class ExtendUser(models.Model):
    avatar_picture = models.ImageField(null=True, blank=True)
    region = models.ForeignKey('Regions', on_delete=models.SET_NULL, null=True, blank=True)
    email_privacy = models.IntegerField(choices=PRIVACY, null=True, blank=True, default=1)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    phone_privacy = models.IntegerField(choices=PRIVACY, null=True, blank=True, default=1)
    skype = models.CharField(max_length=64, null=True, blank=True)
    skype_privacy = models.IntegerField(choices=PRIVACY, null=True, blank=True, default=1)
    instagram_id = models.CharField(max_length=64, null=True, blank=True)
    instagram_privacy = models.IntegerField(choices=PRIVACY, null=True, blank=True, default=1)
    facebook_id = models.CharField(max_length=64, null=True, blank=True)
    facebook_privacy = models.IntegerField(choices=PRIVACY, null=True, blank=True, default=1)
    website = models.URLField(null=True, blank=True, max_length=128)
    website_privacy = models.IntegerField(choices=PRIVACY, null=True, blank=True, default=1)
    about_me = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Username")
    joined = models.DateTimeField(auto_now_add=True, editable=True)
    slug = models.CharField(max_length=200, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Extended User Info'
        verbose_name_plural = 'Extended User Info'

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_date = models.DateTimeField(auto_now_add=True, editable=True)


class PictureCategory(models.Model):
    category = models.CharField(max_length=64, unique=True)
    category_slug = models.CharField(max_length=64, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Picture Categories'
        verbose_name_plural = 'Picture Categories'

    def __str__(self):
        return "%s" % (self.category)


class Picture(models.Model):
    picture = models.ImageField(max_length=160)
    picture_thumbnail = models.ImageField(null=True, blank=True, max_length=160)
    th_width = models.IntegerField(null=True, blank=True)
    th_height = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=160, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pic_slug = models.CharField(max_length=160, unique=True)
    views = models.IntegerField(null=True, blank=True, default=0)
    picture_category_id = models.ForeignKey(PictureCategory, on_delete=models.CASCADE, verbose_name="Picture Category")
    picture_user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Picture Author")
    upload_date = models.DateTimeField(auto_now_add=True, editable=True)
    # EXIF data for picture
    camera_make = models.CharField(max_length=64, null=True, blank=True)
    camera_model = models.CharField(max_length=64, null=True, blank=True)
    lens = models.CharField(max_length=128, null=True, blank=True)
    focal_length = models.IntegerField(null=True, blank=True)
    ISO = models.IntegerField(null=True, blank=True)
    f_stop = models.FloatField(null=True, blank=True)
    shutter_speed = models.CharField(max_length=8, null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s" % (self.id)

    def author(self):
        return "%s %s" % (self.picture_user_id.first_name, self.picture_user_id.last_name)

    def p_rating(self):
        pic_rating = 0
        counter = 0
        all_ratings = PictureRating.objects.filter(picture_id=self.id)
        for rating in all_ratings:
            pic_rating = pic_rating + rating.rating
            counter += 1
        if counter > 0:
            return round(pic_rating / counter, 1)


class PictureRating(models.Model):
    rating = models.IntegerField(choices=PICTURE_RATING, null=True, blank=True)
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE)
    rater = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Picture Rater")
    rating_date = models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        verbose_name = 'Picture Ratings'
        verbose_name_plural = 'Picture Ratings'


class PictureComment(models.Model):
    comment = models.CharField(max_length=1024, null=True, blank=True)
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Pic Commenter")
    comment_date = models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        verbose_name = 'Picture Comments'
        verbose_name_plural = "Pictures Comments"

    def __str__(self):
        return "Comment ID: %s" % (self.id)

    def commenter_name(self):
        return "%s %s" % (self.commenter.last_name, self.commenter.first_name)

    def picture_title(self):
        return "%s" % (self.picture_id)

    def picture_ids(self):
        return "%s" % (self.picture_id.id)


class Tags(models.Model):
    tag = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = 'Tag List'
        verbose_name_plural = 'Tag List'

    def __str__(self):
        return "%s" % (self.tag)


class PictureTags(models.Model):
    picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE, verbose_name='Pic Id')
    picture_tag = models.ForeignKey(Tags, on_delete=models.CASCADE, verbose_name='Pic Tag Name')
    tag_date = models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        verbose_name = 'Picture Tags'
        verbose_name_plural = 'Picture Tags'

    def __str__(self):
        return "pic_id: %s - tag:%s " % (self.picture_id, self.picture_tag)
