from math import sqrt
from PIL.ExifTags import TAGS

from django.contrib.auth.models import User
from os import path, rename, remove
import re
# import unicodedata
from unicodedata import normalize

from django.core.exceptions import ObjectDoesNotExist
from idna import unicode

from fotoPX import settings
from fotoPXapp import models
from fotoPXapp.GlobalFunctions import ReplacePolishCharacters, RemoveSpecialCharacters
from fotoPXapp.models import ExtendUser, Picture, PictureCategory, PICTURE_RATING, PRIVACY, PictureComment, PictureRating, PictureTags, Regions, Followers, Tags
from faker import Faker, Factory
from faker.providers import date_time, lorem, person, phone_number
import random
from PIL import Image

# -------------------------------------------------------------------------------------------------------------------
# https://faker.readthedocs.io/en/master/locales/pl_PL.html


# User.objects.create_superuser(
#     username="allphoto",
#     password="user1234",
#     first_name="Pawel",
#     last_name="Szewczyk",
#     email="paul@allPhotoBangkok.com",
# )

# ----- CREATE USER --------------

# ExtendUser.objects.create(
#     phone_number="0500-16-77-42",
#     skype="pawel.szewczyk2000",
#     instagram_id="allphotolondon",
#     facebook_id="allphotolondon",
#     website="http://www.allPhotoBangkok.com",
#     about_me="""
# We are able to combine art, science and passion into creating any project for you, without you being worried too much about the details. We have our own studio and cooperate with a number of other studios all over the London / Bangkok. We have access to many interesting indoor and outdoor locations which we use for photo shoots.
#
# We have a team of top photographers, make-up artists, stylists and cooperate with designers and have numerous companies in the apparel industry supplying us with latest design outfits (which can be used during photo shoots).
#
# We are prepared and fully equipped to cater for all kinds of studio, outdoor, commercial, fashion, glamour , event and editorial photography.
# """,
#     user_id=1,
#     region=1455,
#
# )

# --------------------------------FAKER-------------------------------------------
fake = Faker('pl_PL')

# email = fake.email()
# first_name = fake.first_name()
# last_name = fake.last_name()
# tel = fake.phone_number()
# username_base = 'user000'
# url = fake.url(schemes=None)
# skype = fake.first_name() + "." + fake.last_name() + "." + str(random.randint(1, 999))
# instagram = fake.word(ext_word_list=None) + "." + fake.word(ext_word_list=None)
# facebook = fake.word(ext_word_list=None) + "." + fake.word(ext_word_list=None)
# about = fake.text(max_nb_chars=500, ext_word_list=None)

# ----- Create Users-------
# for x in range(1, 99):
#     email = fake.email()
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     User.objects.create_user(
#         username=username_base + str(x),
#         password="user1234",
#         first_name=first_name,
#         last_name=last_name,
#         email=email,
#     )

# ----- Create Extended User Info-------

# for x in range (227,244):
#     tel = fake.phone_number()
#     skype = fake.first_name() + "." + fake.last_name() + "."+str(random.randint(1,999))
#     instagram = fake.word(ext_word_list=None) + "." + fake.word(ext_word_list=None)
#     facebook = fake.word(ext_word_list=None) + "." + fake.word(ext_word_list=None)
#     url = fake.url(schemes=None)
#     about = fake.text(max_nb_chars=500, ext_word_list=None)
#     ExtendUser.objects.create(
#         email_privacy=2,
#         phone_number=tel,
#         phone_privacy=2,
#         skype=skype,
#         instagram_id=instagram,
#         instagram_privacy=2,
#         facebook_id=facebook,
#         facebook_privacy=2,
#         website=url,
#         website_privacy=2,
#         about_me=about,
#         region_id=1998,
#         user_id=x,
#     )


# # ----- Create Followers-------
# for x in range(146, 243):
#     random_follower = random.randint(146, 243)
#     if x!=random_follower:
#         Followers.objects.create(
#             following_id=x,
#             follower_id=random_follower,
#         )


# # ----- Create Picture Tags-------
# for x in range(1,200):
#     new_tag=fake.word(ext_word_list=None);
#     if not Tags.objects.filter(tag__contains=new_tag):
#         Tags.objects.create(tag=new_tag)


# # ----- Create Picture Categories-------
# - manual

# # ----- Add Pictures -------
#
# users_id = [150, 167, 187, 207, 212, 229, 158, 172, 196, 191]
# ISO = [100, 200, 400, 800, 1600, 3200, 6400, 50, 320, 250]
# f_stop = [1.4, 1.8, 2, 3.5, 4, 5.6, 8, 11, 16, 22]
# camera = ["Nikon", "Canon", "Sony", "Minolta", "Nikon", "Canon", "Sony", "Minolta", "Canon", "Sony"]
# lens = ["Canon EF-S 10-18mm", "Canon EF-S 18-135mm f/3.5-5.6", "150-600mm F5-6.3 SSM",
#         "Canon EF-S 10-18mm", "Canon EF-S 18-135mm f/3.5-5.6", "150-600mm F5-6.3 SSM",
#         "Canon EF-S 10-18mm", "Canon EF-S 18-135mm f/3.5-5.6", "150-600mm F5-6.3 SSM",
#         "Canon EF-S 10-18mm", "Canon EF-S 18-135mm f/3.5-5.6", "150-600mm F5-6.3 SSM",
#         "Canon EF-S 10-18mm", "Canon EF-S 18-135mm f/3.5-5.6", "150-600mm F5-6.3 SSM", ]
# shutter = [1 / 1000, 1 / 500, 1 / 250, 1 / 125, 1 / 60, 1 / 30, 1 / 15, 1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8]
# focal = [12, 18, 24, 35, 50, 70, 85, 100, 105, 150, 180, 300]
#
# user_counter = 80
# for y in range(1, 2):
#     usr_id = users_id[y] + 6
#     iso_i = ISO[y]
#     f = f_stop[y]
#     cam = camera[y]
#     lenS = lens[y]
#     shutt = shutter[y]
#     mm = focal[y]
#     user_counter += 10
#     for x in range(user_counter, user_counter + 10):
#         Picture.objects.create(
#             picture='portret_0' + str(x) + '.jpg',
#             title=fake.text(max_nb_chars=110, ext_word_list=None),
#             description=fake.text(max_nb_chars=180, ext_word_list=None),
#             picture_category_id_id=4,
#             picture_user_id_id=usr_id,
#             camera_make=cam,
#             lens=lenS,
#             focal_length=mm,
#             ISO=iso_i,
#             f_stop=f,
#             shutter_speed=shutt,
#         )

# ----- Picture Comments-------
# for each picture we generate 15 comments from 15 random users

# comment = fake.text(max_nb_chars=150, ext_word_list=None)
#
# all_users = User.objects.all()
# all_users_count = all_users.count()
#
# all_pictures = Picture.objects.all()
# all_pictures_count = all_pictures.count()

# for pic in all_pictures:
#     for comm in range(1,16):
#         f_comment = fake.text(max_nb_chars=150, ext_word_list=None)
#         random_user = random.randint(1, all_users_count - 1)
#         commenter = all_users[random_user].id
#         PictureComment.objects.create(
#             comment=f_comment,
#             commenter_id=commenter,
#             picture_id_id=pic.id,
#         )


# ----- Picture Ratings-------
# for each picture we generate 10 ratings from 10 random users
# all_users = User.objects.all()
# all_users_count = all_users.count()
#
# all_pictures = Picture.objects.all()
# all_pictures_count = all_pictures.count()
#
# for pic in all_pictures:
#     for rati in range(1,16):
#         rating = random.randint(1,5)
#         random_user = random.randint(1, all_users_count - 1)
#         rater = all_users[random_user].id
#         PictureRating.objects.create(
#             rating=rating,
#             picture_id_id=pic.id,
#             rater_id=rater
#         )

# ----- Picture Tags-------
# for each picture we generate 7 random tags
# all_pictures = Picture.objects.all()
# all_pictures_count = all_pictures.count()
#
# all_tags = Tags.objects.all()
# all_tags_count = all_tags.count()
#
# for pic in all_pictures:
#     for t in range(1, 8):
#         random_t = random.randint(1, all_tags_count - 1)
#         random_tag = all_tags[random_t].id
#         PictureTags.objects.create(
#             picture_tag_id=random_tag,
#             picture_id_id=pic.id,
#         )


# --------Picture Thumbnails--------
# ---pattern => fashion_001_thumb.jpg

# all_pictures = Picture.objects.all()
# for pic in all_pictures:
#     full_size = pic.picture
#     filename, extension = path.splitext(str(full_size))
#     outfile = filename +  "_thumb.jpg"
#     pic.picture_thumbnail = outfile
#     pic.save()

# ------Create----Picture----Slugs-------
# sample title => Wieża słuchać różowy blisko. Piękny dziedzina naprawdę siedemdziesiąt dziewięćdziesiąt umożliwiać wiosna. Powinien fakt maj.

# all_pictures = Picture.objects.all()
# pic_slug = ""
# for pic in all_pictures:
#     title = pic.title
#     pic_category = pic.picture_category_id.category_slug
#
#     # remove special characters, prepare initail slug/
#     output = re.sub('[^A-Za-z0-9]+', ' ', output)
#     output = output.replace(' ', '-')
#     output = output[0:-1].lower()
#
#     if len(output) < 5:
#         pic_slug = pic_category + "-" + str(random.randint(1, 10000))
#
#     if len(output) > 100:  # shorten slug to max 100 characters
#         while len(output) > 100:
#             k = output.rfind("-")
#             output = output[:k]
#             pic_slug = output
#     else:
#         pic_slug = output
#
#     if PictureCategory.objects.filter(category_slug__exact=pic_slug):
#         pic_slug = pic_slug+"-"+str(random.randint(1,1000))
#
#     pic.pic_slug=pic_slug
#     pic.save()


# -----------Change Category slugs-------------
# x = PictureCategory.objects.get(id=5)
# x.category_slug="fotografia-dokumentalna"
# x.save()
# print(x.category_slug)


# -----------Thumbnails dimansions -------------
#
# all_pictures = Picture.objects.all()
# for thumb in all_pictures:
#     thumbnail = thumb.picture_thumbnail
#     full_path_to_file = "../" + settings.MEDIA_ROOT + str(thumbnail)
#     im = Image.open(full_path_to_file)
#     picture_width = im.size[0]
#     picture_height = im.size[1]
#     thumb.th_width = int(picture_width)
#     thumb.th_height = int(picture_height)
#     thumb.save()
#     im.close()

# -----------ADD AVATAR PICTURES-----------------
# all_users = ExtendUser.objects.all().order_by('id')
# x = 10
# y = 90
# while (x < 18):
#     avatar = "avatar_test_0" + str(x) + ".jpg"
#     # print("=> ", avatar)
#     usr = all_users[y]
#     usr.avatar_picture=avatar
#     usr.save()
#     y = y + 1
#     x = x + 1

# ---------------CHANGE USER SLUGS ------------------------------
# -----------Change Category slugs-------------


# users = ExtendUser.objects.all()
# for us in users:
#     region = Regions.objects.get(id=us.region_id)
#     wojewodztwo_id = region.voivodeship_id
#     woj = Regions.objects.get(voivodeship_id=wojewodztwo_id, county_id=None)
#     woj_lower = woj.city.lower()
#     stri = woj_lower
#     slug = "fotograf/" + stri + "/" + us.user.first_name + "-" + us.user.last_name + "/" + str(us.user.id)
#     slug = slug.lower()
#     slug = ReplacePolishCharacters(slug)

    # remove polish characters:
    # polishChars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ż', 'ź']
    # replaceChar = ['a', 'c', 'e', 'l', 'n', 'o', 's', 'z', 'z']
    # arr_len = 9
    # i = 0
    # while i < 9:
    #     slug = slug.replace(polishChars[i], replaceChar[i])
    #     i = i + 1
    # slug = "fotograf/" + stri + "/" + us.user.first_name + "-"+us.user.last_name + "/" + str(us.id)
    # print(slug)
    # us.slug = slug
    # us.save()

# print(ReplacePolishCharacters("dolnośląskie"))

# ------Generate random picture Views------
# pictures = Picture.objects.all()
# for el in pictures:
#     views = random.randint(1,155)
#     el.views=views
#     el.save()

# ----------Generate slugs for Picture tags--------------
# tags = Tags.objects.all()
# for el in tags:
#     tag = el.tag
#     tag = ReplacePolishCharacters(tag)
#     tag = RemoveSpecialCharacters (tag).lower()
#     slug = tag
#     el.slug=slug
#     el.save()

# ---------------------EXIF DATA----------------------
# def getExifData(full_path_to_file):
#     from PIL import Image
#     from PIL.ExifTags import TAGS
#     from math import sqrt
#
#     im = Image.open(full_path_to_file)
#
#     exif_tags = im._getexif()
#     if exif_tags != None:
#         # print all avilable exif TAGS codes and descriptions
#         for key in exif_tags:
#             try:
#                 print(key, ":", TAGS[key]);
#             except Exception as e:
#                 print("blad", e)
#         # test tags
#         date_taken = exif_tags[36867]
#         camera_make = exif_tags[271]
#         camera_model = exif_tags[272]
#
#         try:
#             print("lens:", exif_tags[42036])
#         except Exception:
#             print("no lens info")
#
#         # lens_make=exif_tags[42035]
#
#         try:
#             focal_length = round(exif_tags[37386][0] / exif_tags[37386][1])
#         except Exception:
#             focal_length = "n/a"
#
#         try:
#             ISO = exif_tags[34855]
#         except Exception:
#             ISO = "n/a"
#         # shutter_speed_apex = exif_tags[37377][0] / 1000000
#         # shutter_speed = round(1/(1 / (2 ** shutter_speed_apex)))
#
#         exposure_time = round((exif_tags[33434][1] / exif_tags[33434][0]), 5)
#         print(exposure_time)
#         print("EXPOSURE: ", exif_tags[33434])
#         if exposure_time > 1:
#             exposure_time = "1/"+str(round(exposure_time))+" s"
#         else:
#             exposure_time = str(round(1/exposure_time,1))+" s"
#
#         try:
#             aperture_apex = exif_tags[37378][0] / 1000000
#             aperture = round(sqrt(2 ** aperture_apex), 1)
#         except Exception:
#             aperture = "n/a"
#         FNumber = exif_tags[33437][0] / exif_tags[33437][1]
#         print("date: ", date_taken)
#         print("camera make: ", camera_make)
#         print("camera model: ", camera_model)
#         # print("lens: ", lens_make)
#         print("mm: ", focal_length)
#         print("iso: ", ISO)
#         # print("speed: ", shutter_speed)
#         print("exposure time: ", exposure_time)
#         print("aperture: ", aperture)
#         print("Fnumber: ", FNumber)
#
#
# # ----TEST IMAGES -- for exif
# full_path_to_file = "dubai_exif.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "Story_picture_3__2011_12_16_Lost_in_Bangkok_RAW_123AB.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "APH_7468.jpg"
# full_path_to_file = "Commercial-Food-Restaurant1.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "pies_damsung.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "2010_12_16_Ferrari_Shoot_RAW_447_ps.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "2010_06_13_Julia_RAW_300.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "APH_6702.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "dscf2127.jpg" #FUJI
# getExifData(full_path_to_file)
# full_path_to_file = "Cat004849C.JPG" #Lumix
# getExifData(full_path_to_file)
# full_path_to_file = "APH_7468.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "Death-Valley-NP-5.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "moon-1-35.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "Julia-Anna-Gospodarou_Fujifilm-GFX-50S_Long-Exposure-270-sec_800.jpg"  # only copyrights exif data
# getExifData(full_path_to_file)
# full_path_to_file = "IMG_4412.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "nikon_d80.jpg"
# getExifData(full_path_to_file)
# full_path_to_file = "nikon_d300.JPG"
# getExifData(full_path_to_file)
# full_path_to_file = "nikon_d70.JPG"
# getExifData(full_path_to_file)
# full_path_to_file = "long_exposure.JPG"
# getExifData(full_path_to_file)

# pics = PictureComment.objects.all()
# for p in pics:
#     try:
#         ExtendUser.objects.get(user_id=p.commenter_id)
#     except ObjectDoesNotExist:
#         print(p.commenter_id)
#     except Exception:
#         print("xxxxxxxx")

# pics = PictureComment.objects.filter(commenter_id=146)
# pics.delete()

# add last login date
# users = User.objects.all().order_by('id')[82:99]
# day = 9
# for u in users:
#     day +=1
#     u.last_login = "2018-08-"+str(day)+ " 19:10"
#     u.save()



    # -----------------------------------------------------------------------------------------------------------------------
    # odpalamy w konsoli
    # python3 ../manage.py shell < working_scripts.py
