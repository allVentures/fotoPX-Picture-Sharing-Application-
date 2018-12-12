from io import BytesIO
from PIL import Image
from django.contrib.auth.models import AnonymousUser, User
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import response
from django.test import RequestFactory, TestCase
from django.test.client import Client
from django.urls import reverse

from fotoPX import settings
from fotoPXapp.models import User, ExtendUser, Picture, PictureTags, PictureCategory, PictureRating, PictureComment, \
    PRIVACY, PICTURE_RATING, Tags
from fotoPXapp.forms import RegisterForm, LoginForm, AddPictureForm
from fotoPXapp.views import AddPicture


# access to upload picture page only to logged users
# admin is logged, user is not logged
# class AccesstoUploadPicturePage(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="user", password="123", email="paw@ww.pl")
#         self.admin = User.objects.create_superuser(username="admin", password="123", email="ww@woep.pl")
#         self.admin_client = Client()
#         self.user_client = Client()
#         self.admin_client.login(username='admin', password='123')
#         # user in not logged in
#
#     def test_add_picture_page_access(self):
#         response = self.admin_client.get(reverse('add_picture'))
#         self.assertEqual(response.status_code, 200)
#         response = self.user_client.get(reverse('add_picture'))
#         self.assertEqual(response.status_code, 302)  # 302 Found redirect status response

# ---- user login form----
# class UserLoginForm(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="user", password="123", email="paw@ww.pl")
#         self.user_client = Client()
#
#     def test_LoginForm_valid(self):
#         form = LoginForm(data={
#             'username': "user",
#             'password': "123",
#         })
#         self.assertTrue(form.is_valid())
#
#     def test_LoginForm_Notvalid(self):
#         form = LoginForm(data={
#             'username': "",
#             'password': "user1234333",
#         })
#         self.assertFalse(form.is_valid())
#
#     def test_loginValid(self):
#         user_login = self.user_client.login(username='user', password='123')
#         self.assertTrue(user_login)
#
#     def test_loginInValid(self):
#         user_login = self.user_client.login(username='user', password='12ddd3')
#         self.assertFalse(user_login)
#


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

    # # Valid Form Data
    # def test_PictureUploadForm_valid(self):
    #     picture_file = settings.MEDIA_ROOT + 'avatar_test_029.jpg'
    #     data = {
    #         'title': "test title for picture upload",
    #         'description': "123 d fsdfds gs g ggs g sgs ",
    #         'picture_tags': "r rr r rrrrrrrr rrrr",
    #         'picture_category': 1}
    #
    #     picture_file = open(picture_file, 'rb')
    #     picture_file = SimpleUploadedFile('avatar_test_029.jpg', picture_file.read())
    #     files = {'picture': picture_file}
    #
    #     form = AddPictureForm(data=data, files=files)
    #     self.assertTrue(form.is_valid(), form.errors)
    #
    # # Too long title => Ensure this value has at most 160 characters (it has 252)
    # def test_PictureUploadFormNotvalid1(self):
    #     picture_file = settings.MEDIA_ROOT + 'avatar_test_029.jpg'
    #     data = {
    #         'title': "test title for picture upload test title for picture uploadtest title for picture uploadtest "
    #                  "title for picture uploadtest title for picture uploadtitle for picture uploadtest title for "
    #                  "picture uploadtitle for picture uploadtest title for picture upload",
    #         'description': "123 d fsdfds gs g ggs g sgs ",
    #         'picture_tags': "r rr r rrrrrrrr rrrr",
    #         'picture_category': 1}
    #
    #     picture_file = open(picture_file, 'rb')
    #     picture_file = SimpleUploadedFile('avatar_test_029.jpg', picture_file.read())
    #     files = {'picture': picture_file}
    #
    #     form = AddPictureForm(data=data, files=files)
    #     self.assertFalse(form.is_valid(), form.errors)
    #
    # # No picture file = > musisz wybrać zdjęcie
    # def test_PictureUploadFormNotvalid2(self):
    #     picture_file = settings.MEDIA_ROOT + 'avatar_test_029.jpg'
    #     data = {
    #         'title': "test title for picture upload test",
    #         'description': "123 d fsdfds gs g ggs g sgs ",
    #         'picture_tags': "r rr r rrrrrrrr rrrr",
    #         'picture_category': 1}
    #
    #     picture_file = open(picture_file, 'rb')
    #     picture_file = SimpleUploadedFile('avatar_test_029.jpg', picture_file.read())
    #     files = {'picture': None}
    #
    #     form = AddPictureForm(data=data, files=files)
    #     self.assertFalse(form.is_valid(), form.errors)
    # ADD CLOSE

# ---- test of the class AddPicture(LoginRequiredMixin, View):

    def test_AddPicture_View(self):
        picture_file = settings.MEDIA_ROOT + "tests/test_image_exif.jpg"
        data = {
            'title': "This is the total test for the AddPicture View",
            'description': "description for AddPicture View test. description for AddPicture View test. description "
                           "for AddPicture View test. description for AddPicture View test. description for "
                           "AddPicture View test. description for AddPicture View test. description for AddPicture "
                           "View test. ",
            'picture_tags': "test, view, Picture, upload, add, ",
            'picture_category': 1}
        picture_file = open(picture_file, 'rb')
        picture_file = SimpleUploadedFile('test_image_exif.jpg', picture_file.read(), content_type="image/jpeg")
        picture_file.read()
        files = {'picture': picture_file}

        form = AddPictureForm(data=data, files=files)
        self.assertFalse(form.is_valid(), form.errors)

        response = self.user_client.post("/dodaj-zdjecie", data=data, files=files)
        self.assertEqual(response.status_code, 200)



    # run tests => python3 manage.py test
