from django.contrib.auth.models import User
from fotoPXapp.models import ExtendUser, Picture, PictureCategory, PICTURE_RATING, PRIVACY, PictureComment, \
    PictureRating, PictureTags, Regions, Followers

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
