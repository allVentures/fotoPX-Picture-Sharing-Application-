from io import BytesIO
from PIL import Image
from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import RequestFactory, TestCase
from django.test.client import Client
from django.urls import reverse

from fotoPX import settings
from fotoPXapp.models import User, ExtendUser, Picture, PictureTags, PictureCategory, PictureRating, PictureComment, \
    PRIVACY, PICTURE_RATING, Tags
from fotoPXapp.forms import RegisterForm, LoginForm, AddPictureForm
from fotoPXapp.views import AddPicture, AllUsers, PictureView, user_page


# access to upload picture page only to logged users
# admin is logged, user is not logged
class AccesstoUploadPicturePage(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="123", email="paw@ww.pl")
        self.admin = User.objects.create_superuser(username="admin", password="123", email="ww@woep.pl")
        self.admin_client = Client()
        self.user_client = Client()
        self.admin_client.login(username='admin', password='123')
        # user in not logged in

    def test_add_picture_page_access(self):
        response = self.admin_client.get(reverse('add_picture'))
        self.assertEqual(response.status_code, 200)
        response = self.user_client.get(reverse('add_picture'))
        self.assertEqual(response.status_code, 302)  # 302 Found redirect status response


# ---- user login form----
class UserLoginForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="123", email="paw@ww.pl")
        self.user_client = Client()

    def test_LoginForm_valid(self):
        form = LoginForm(data={
            'username': "user",
            'password': "123",
        })
        self.assertTrue(form.is_valid())

    def test_LoginForm_Notvalid(self):
        form = LoginForm(data={
            'username': "",
            'password': "user1234333",
        })
        self.assertFalse(form.is_valid())

    def test_loginValid(self):
        user_login = self.user_client.login(username='user', password='123')
        self.assertTrue(user_login)

    def test_loginInValid(self):
        user_login = self.user_client.login(username='user', password='12ddd3')
        self.assertFalse(user_login)


# ----------Picture upload tests--------------

class PictureUpload(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="123", email="paw@ww.pl")
        self.user.is_active = True
        self.user.save()
        self.user_client = Client()
        user_login = self.user_client.login(username='user', password='123')
        self.assertTrue(user_login)
        self.factory = RequestFactory()
        # PictureCategory.objects.create(category="moda", category_slug="moda-fashion")
        # PictureCategory.objects.create(category="landscape", category_slug="landscape")

    # Valid Form Data
    def test_PictureUploadForm_valid(self):
        picture_file = settings.MEDIA_ROOT + 'avatar_test_029.jpg'
        data = {
            'title': "test title for picture upload",
            'description': "123 d fsdfds gs g ggs g sgs ",
            'picture_tags': "r rr r rrrrrrrr rrrr",
            'picture_category': 1}

        picture_file = open(picture_file, 'rb')
        picture_file = SimpleUploadedFile('avatar_test_029.jpg', picture_file.read())
        files = {'picture': picture_file}

        form = AddPictureForm(data=data, files=files)
        self.assertTrue(form.is_valid(), form.errors)
        picture_file.close()

    # Too long title => Ensure this value has at most 160 characters (it has 252)
    def test_PictureUploadFormNotvalid1(self):
        picture_file = settings.MEDIA_ROOT + 'avatar_test_029.jpg'
        data = {
            'title': "test title for picture upload test title for picture uploadtest title for picture uploadtest "
                     "title for picture uploadtest title for picture uploadtitle for picture uploadtest title for "
                     "picture uploadtitle for picture uploadtest title for picture upload",
            'description': "123 d fsdfds gs g ggs g sgs ",
            'picture_tags': "r rr r rrrrrrrr rrrr",
            'picture_category': 1}

        picture_file = open(picture_file, 'rb')
        picture_file = SimpleUploadedFile('avatar_test_029.jpg', picture_file.read())
        files = {'picture': picture_file}

        form = AddPictureForm(data=data, files=files)
        self.assertFalse(form.is_valid(), form.errors)
        picture_file.close()

    # No picture file = > musisz wybrać zdjęcie
    def test_PictureUploadFormNotvalid2(self):
        picture_file = settings.MEDIA_ROOT + 'avatar_test_029.jpg'
        data = {
            'title': "test title for picture upload test",
            'description': "123 d fsdfds gs g ggs g sgs ",
            'picture_tags': "r rr r rrrrrrrr rrrr",
            'picture_category': 1}

        picture_file = open(picture_file, 'rb')
        picture_file = SimpleUploadedFile('avatar_test_029.jpg', picture_file.read())
        files = {'picture': None}

        form = AddPictureForm(data=data, files=files)
        self.assertFalse(form.is_valid(), form.errors)
        picture_file.close()

    # ---- test of the class AddPicture:
    # EXIF for test picture
    # Camera Manufacturer	NIKON CORPORATION
    # Camera Model	NIKON D300
    # Exposure time [s]	1/5
    # F-Number	6.3
    # Exposure program	Manual (1)
    # ISO speed ratings	200
    # Date taken	16/12/2011 - 14:31:08 CET
    # Shutter speed [s]	1/5
    # Aperture	F6.3
    # Focal length [mm]	98

    def test_AddPicture_View(self):
        picture_file = settings.MEDIA_ROOT + "tests/testimageexif.jpg"
        data = {
            'title': "Piękny widok na Bangkok",
            'description': "description for AddPicture View test. description for AddPicture View test. description "
                           "for AddPicture View test. description for AddPicture View test. description for "
                           "AddPicture View test. description for AddPicture View test. description for AddPicture "
                           "View test. ",
            'picture_tags': "test, view, Picture, upload, add, ",
            'picture_category': 1}
        picture_file = open(picture_file, 'rb')
        picture_file = SimpleUploadedFile('testimageexif.jpg', picture_file.read(), content_type="image/jpeg")
        files = {'picture': picture_file}

        form = AddPictureForm(data=data, files=files)
        self.assertTrue(form.is_valid())

        response = self.user_client.post("/dodaj-zdjecie", data=data, files=files)
        self.assertEqual(response.status_code, 200)

        data['picture'] = picture_file
        request = self.factory.post("/dodaj-zdjecie", data=data)
        request.user = self.user
        response = AddPicture.as_view()(request)
        # print(response.content)

        last_picture = Picture.objects.all().last().id
        tested_picture = Picture.objects.get(id=last_picture)

        self.assertEqual(tested_picture.title, "Piękny widok na Bangkok")
        self.assertEqual(tested_picture.picture_category_id_id, 1)
        self.assertEqual(tested_picture.picture, "Krajobraz-piekny-widok-na-bangkok.jpg")
        self.assertEqual(tested_picture.picture_thumbnail, "krajobraz-piekny-widok-na-bangkok_thumb.jpg")
        self.assertEqual(tested_picture.ISO, 200)
        self.assertEqual(tested_picture.shutter_speed, "1/5")
        self.assertEqual(tested_picture.f_stop, 6.3)
        self.assertEqual(tested_picture.focal_length, 98)
        self.assertEqual(tested_picture.camera_make, "nikon corporation")
        self.assertEqual(tested_picture.camera_model, "nikon d300")
        self.assertEqual(tested_picture.lens, "n/a")

        picture_file.close()


# ------- test copy of procuction database -------------

class AccessToPages(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(id=1)

    def test_user_pages_access(self):
        all_users = ExtendUser.objects.all()
        for usr in all_users:
            request = self.factory.get("/" + usr.slug)
            request.user = self.user
            response = user_page.as_view()(request, voivodeship="xxx", name=usr.slug, id=usr.user_id)
            print(usr.user_id, usr.slug, "=> response code:", response.status_code)
            self.assertEqual(response.status_code, 200)

    def test_picture_view_pages_access(self):
        all_pics = Picture.objects.all()
        for pic in all_pics:
            request = self.factory.get(
                "/" + pic.picture_category_id.category_slug + "/" + pic.pic_slug + "/" + str(pic.id))
            request.user = self.user
            response = PictureView.as_view()(request, category_slug=pic.picture_category_id.category_slug,
                                             picture_slug=pic.pic_slug, id=pic.id)
            print(pic.id, "=> response code:", response.status_code)
            self.assertEqual(response.status_code, 200)

    # run tests => python3 manage.py test
    # python3 manage.py test --keepdb

    # pg_dump -U postgres -W -h localhost fotopx  > fotopx.sql
    # psql -U postgres -W -f fotopx.sql -h localhost fotopxtest
    # python3 manage.py test - -keepdb
