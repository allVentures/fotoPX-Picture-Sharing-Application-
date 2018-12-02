from django.contrib.auth.models import User
from fotoPXapp.models import ExtendUser, Picture, PictureCategory, PICTURE_RATING, PRIVACY, PictureComment, \
    PictureRating, PictureTags, Regions, Followers
from faker import Faker, Factory
from faker.providers import date_time, lorem, person, phone_number
import random

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

email = fake.email()
first_name = fake.first_name()
last_name = fake.last_name()
tel = fake.phone_number()
username_base = 'user000'
url = fake.url(schemes=None)
skype = fake.first_name() + "." + fake.last_name() + "." + str(random.randint(1, 999))
instagram = fake.word(ext_word_list=None) + "." + fake.word(ext_word_list=None)
facebook = fake.word(ext_word_list=None) + "." + fake.word(ext_word_list=None)
about = fake.text(max_nb_chars=500, ext_word_list=None)

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


# # ----- Create Picture Categories-------
for x in range(1,1000):
    PictureCategory.objects.create(
        category=fake.word(ext_word_list=None)
    )






# students=Departament.objects.get(id=3).student_set.all()
# for x in students:
#     print(x.name)
#
# art=Article.objects.get(id=5).category.all()
# for x in art:
#     print(x.name)
#
# cat=Category.objects.get(id=3).article_set.all()
# for x in cat:
#     print(x.title)

# st=Student.objects.filter(dep_id=3)
# for x in st:
#     x.dep_id=1
#     x.save()

# stud=Student.objects.get(id=2)
# stud.dep_id=None
# stud.save()
# art=Article.objects.get(id=5)
# cat=Category.objects.get(id=4)
# art.category.remove(cat)

# dep=Departament.objects.get(id=2)
# dep_students=dep.student_set.all()
# for x in dep_students:
#     print(x.name)


# Room.objects.create(
#     name="Sala Richard Wagner",
#     capacity=15,
#     projector=False,
# )

# Booking.objects.create(
#     booking_date="2018-12-06",
#     room_id=3,
#     comment="this is some comment xxxxx"
# )

# print(Booking.objects.filter(booking_date="2018-12-01"))


# odpalamy w konsoli
# python3 ../manage.py shell < working_scripts.py
