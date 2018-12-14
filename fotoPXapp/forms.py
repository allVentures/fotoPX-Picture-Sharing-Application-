from django import forms
from django.core.validators import EmailValidator

from fotoPXapp.models import User, ExtendUser, Picture, PictureTags, PictureCategory, PictureRating, PictureComment, \
    PRIVACY, PICTURE_RATING, Tags


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32, widget=forms.TextInput(attrs={"class": "form-control"}),
                               error_messages={'required': 'to pole jest wymagane'})
    password = forms.CharField(label="Password", max_length=32,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}),
                               error_messages={'required': 'to pole jest wymagane'})
    password_check = forms.CharField(label="Password Check", max_length=32,
                                     widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                     error_messages={'required': 'to pole jest wymagane'})
    first_name = forms.CharField(label="First Name", max_length=32,
                                 widget=forms.TextInput(attrs={"class": "form-control"}),
                                 error_messages={'required': 'to pole jest wymagane'})
    last_name = forms.CharField(label="Last Name", max_length=32,
                                widget=forms.TextInput(attrs={"class": "form-control"}),
                                error_messages={'required': 'to pole jest wymagane'})
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={"class": "form-control privacyInput"}),
                             max_length=64, error_messages={'invalid': 'wprowadź poprawny email adres',
                                                            'required': 'to pole jest wymagane'})
    email_privacy = forms.CharField(label="Email Privacy",
                                    widget=forms.Select(choices=PRIVACY, attrs={"class": "form-control privacy"}))
    website = forms.URLField(label="website", max_length=128, required=False,
                             widget=forms.URLInput(attrs={"class": "form-control privacyInput"}),
                             error_messages={'invalid': 'wprowadz poprawny adres URL zaczynający sie od http://www '})
    website_privacy = forms.CharField(label="Website Privacy", required=False,
                                      widget=forms.Select(choices=PRIVACY, attrs={"class": "form-control privacy"}))
    phone = forms.CharField(label="Phone", required=False,
                            widget=forms.TextInput(attrs={"class": "form-control privacyInput"}), max_length=20)
    phone_privacy = forms.CharField(label="Phone Privacy", required=False,
                                    widget=forms.Select(choices=PRIVACY, attrs={"class": "form-control privacy"}))
    skype = forms.CharField(label="skype", required=False,
                            widget=forms.TextInput(attrs={"class": "form-control privacyInput"}), max_length=64)
    skype_privacy = forms.CharField(label="skype Privacy", required=False,
                                    widget=forms.Select(choices=PRIVACY, attrs={"class": "form-control privacy"}))
    instagram = forms.CharField(label="instagram", required=False,
                                widget=forms.TextInput(attrs={"class": "form-control privacyInput"}), max_length=64)
    instagram_privacy = forms.CharField(label="Instagram Privacy", required=False,
                                        widget=forms.Select(choices=PRIVACY, attrs={"class": "form-control privacy"}))
    facebook = forms.CharField(label="facebook", required=False,
                               widget=forms.TextInput(attrs={"class": "form-control privacyInput"}), max_length=64)
    facebook_privacy = forms.CharField(label="Facebook Privacy", required=False,
                                       widget=forms.Select(choices=PRIVACY, attrs={"class": "form-control privacy"}))
    about_me = forms.CharField(label="about me", required=False, max_length=512, widget=forms.Textarea(
        attrs={"class": "form-control privacy"}))
    avatar_picture = forms.ImageField(label="avatar picture", required=False, error_messages={
        'invalid_image': 'zaladuj poprawny plik ze zdjeciem. dozwolone formaty: .jpg, .tif, .bmp'})


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32,
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "username"}),
                               error_messages={'required': 'to pole jest wymagane'})
    password = forms.CharField(label="Password", max_length=32,
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "hasło"}),
                               error_messages={'required': 'to pole jest wymagane'})


class AddPictureForm(forms.Form):
    CAT = []
    categories = PictureCategory.objects.all()
    for cat in categories:
        CAT.append((cat.id, cat.category))
        CATEGORIES = tuple(CAT)

    # this tuple is here just for testing purposes; otherwise use the dynamically generated tuple above
    # CATEGORIES = (
    # (1, "Moda"),
    # (2, "Krajobraz"),
    # (3, "Portret"),
    # )

    picture = forms.ImageField(label="picture", max_length=160, required=True, error_messages={
        'invalid_image': 'zaladuj poprawny plik ze zdjeciem. dozwolone formaty: .jpg, .tif, .bmp',
        'required': 'musisz wybrać zdjęcie'})
    title = forms.CharField(label="title", required=False, max_length=160,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="description", required=False, max_length=512, widget=forms.Textarea(
        attrs={"class": "form-control"}))
    picture_category = forms.CharField(label="category", required=True,
                                       widget=forms.Select(choices=CATEGORIES, attrs={"class": "form-control"}),
                                       error_messages={'required': 'to pole jest wymagane'})
    picture_tags = forms.CharField(label="picture_tags", required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}), max_length=256)


class AddComment(forms.Form):
    comment = forms.CharField(label="comment", required=False, max_length=256, widget=forms.Textarea(
        attrs={"class": "form-control commentInput", "rows": 2}))
