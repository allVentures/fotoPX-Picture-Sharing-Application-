import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models.aggregates import Avg, Sum
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpRequest, Http404
from django.views import View
from django.conf import settings
from os import path, rename, remove
from json import dumps
from fotoPXapp.models import User, ExtendUser, Regions, Picture, PictureCategory, PictureTags, PictureRating, \
    PictureComment, Followers, Tags
from fotoPXapp.GlobalFunctions import ReplacePolishCharacters
from PIL import Image
from fotoPXapp.forms import RegisterForm, LoginForm


# ------------MAIN PAGE, HEADER , FOOTER-----------------------
class MainPage(View):
    def get(self, request):
        ctx = {}
        return render(request, "main_page.html", ctx)


# -----------------------------USER-----------------------------
class user_registration(View):
    def get(self, request):
        form = RegisterForm()
        voId = request.GET.get('voivodeship_id')
        countyId = request.GET.get('county_id')

        if voId == None:
            regions = Regions.objects.filter(county_id=None)
            ctx = {"regions": regions, "form": form}
            return render(request, "user_registration.html", ctx)
        if voId and not countyId:
            regions = Regions.objects.filter(voivodeship_id=voId, municipality_id=None, county_id__isnull=False)
            response_data = {}
            for el in regions:
                response_data[el.county_id] = el.city
            return HttpResponse(dumps(response_data), content_type="application/json")
        if voId and countyId:
            regions = Regions.objects.filter(voivodeship_id=voId, county_id=countyId, municipality_id__isnull=False)
            response_data = {}
            for el in regions:
                response_data[el.municipality_id] = el.city
            return HttpResponse(dumps(response_data), content_type="application/json")

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            email_privacy = form.cleaned_data["email_privacy"]
            password = form.cleaned_data["password"]
            password_check = form.cleaned_data["password_check"]
            website = form.cleaned_data["website"]
            website_privacy = form.cleaned_data["website_privacy"]
            phone = form.cleaned_data["phone"]
            phone_privacy = form.cleaned_data["phone_privacy"]
            skype = form.cleaned_data["skype"]
            skype_privacy = form.cleaned_data["skype_privacy"]
            instagram = form.cleaned_data["instagram"]
            instagram_privacy = form.cleaned_data["instagram_privacy"]
            facebook = form.cleaned_data["facebook"]
            facebook_privacy = form.cleaned_data["facebook_privacy"]
            about_me = form.cleaned_data["about_me"]
            voivodeship_id = request.POST["voivodeship_id"]
            county_id = request.POST.get("county_id")
            municipality_id = request.POST.get("municipality_id")

            if int(voivodeship_id) == 0:
                user_region_id = 3000
                print("1szy ", user_region_id)
            else:
                if int(county_id) == 0:
                    user_region_id = Regions.objects.get(voivodeship_id=voivodeship_id, county_id__isnull=True).id
                    print("2ci ", user_region_id)
                else:
                    if int(municipality_id) == 0:
                        user_region_id = Regions.objects.get(voivodeship_id=voivodeship_id, county_id=county_id,
                                                             municipality_id__isnull=True).id
                        print("3ci ", user_region_id)
                    else:
                        user_region_id = Regions.objects.get(voivodeship_id=voivodeship_id, county_id=county_id,
                                                             municipality_id=municipality_id).id
                        print("4ty ", user_region_id)

            errors = {}
            if password != password_check:
                errors["password"] = "wprowadzone hasła nie są jednakowe, wprowadź ponownie"

            try:
                new_user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                new_user.save()
                new_user_id = new_user.id
            except IntegrityError:
                errors["username"] = "wprowadzona nazwa użytkownika jest już zajęta, wybierz inną"
            if errors:
                new_user
                regions = Regions.objects.filter(county_id=None)
                ctx = {"regions": regions, "form": form, "errors": errors}
                return render(request, "user_registration.html", ctx)

            region = Regions.objects.get(id=user_region_id)
            wojewodztwo_id = region.voivodeship_id
            woj = Regions.objects.get(voivodeship_id=wojewodztwo_id, county_id=None)
            woj_lower = woj.city.lower()
            stri = woj_lower
            if stri == "nie podano":
                stri = "polska"
            slug = "fotograf/" + stri + "/" + new_user.first_name + "-" + new_user.last_name + "/" + str(
                new_user.id)
            cleaned_slug = ReplacePolishCharacters(slug)
            # --- start of avatar processing----
            if 'avatar_picture' in request.FILES:
                avatar_picture = request.FILES["avatar_picture"]

                # image format validation and dimesions check
                max_picture_width = 600
                min_picture_width = 400
                min_picture_height = 400
                max_picture_height = 600

                try:
                    im = Image.open(avatar_picture)
                    picture_width = im.size[0]
                    picture_height = im.size[1]
                    print(picture_height)
                    if picture_width < min_picture_width or picture_height < min_picture_height:
                        avatar_error = "Avatar musi miec min 400px x 400px!"
                        im.close()
                        regions = Regions.objects.filter(county_id=None)
                        ctx = {"regions": regions, "form": form, "avatar_error": avatar_error}
                        return render(request, "user_registration.html", ctx)
                except Exception as avatar_error:  # this is gonna be validated by ImageField in Django anyway
                    avatar_error = "ten format nie jest dozwolony, dozwolone formaty: jpg, tif, bmp."
                    regions = Regions.objects.filter(county_id=None)
                    ctx = {"regions": regions, "form": form, "avatar_error": avatar_error}
                    return render(request, "user_registration.html", ctx)

                new_extended_user = ExtendUser.objects.create(
                    avatar_picture=avatar_picture,
                    email_privacy=email_privacy,
                    phone_number=phone,
                    phone_privacy=phone_privacy,
                    skype=skype,
                    skype_privacy=skype_privacy,
                    instagram_id=instagram,
                    instagram_privacy=instagram_privacy,
                    facebook_id=facebook,
                    facebook_privacy=facebook_privacy,
                    website=website,
                    website_privacy=website_privacy,
                    about_me=about_me,
                    region_id=user_region_id,
                    user_id=new_user_id,
                    slug=cleaned_slug,
                )

                full_path_to_file = settings.MEDIA_ROOT + str(new_extended_user.avatar_picture)

                # resize image, convert file to jpg
                ratio = picture_width / picture_height

                if picture_width > max_picture_width or picture_height > max_picture_height:
                    if ratio > 1:
                        picture_height = min_picture_height
                        picture_width = picture_height * ratio
                    else:
                        picture_width = min_picture_width
                        picture_height = picture_width / ratio

                picture_height = int(round(picture_height, 0))
                picture_width = int(round(picture_width, 0))

                filename, extension = path.splitext((str(new_extended_user.avatar_picture).lower()))
                im = im.resize((picture_width, picture_height))
                outfile = filename + ".jpg"

                if new_extended_user.avatar_picture != outfile:
                    try:
                        im.save(settings.MEDIA_ROOT + outfile, "JPEG")
                        new_extended_user.avatar_picture = outfile
                    except IOError as e:
                        e = "Ten format pliku nie moze byc skonwertowany do jpg."
                        return render(request, "standard_error_page.html", {"msg": e})

                    except Exception as e:
                        im.close()
                        return render(request, "standard_error_page.html", {"msg": e})
                else:
                    im.save(settings.MEDIA_ROOT + outfile, "JPEG")
                    new_extended_user.picture = outfile
                    new_extended_user.save()

                im.close()
                # -------avatar picture rename-------

                filename, extension = path.splitext(str(new_extended_user.avatar_picture))
                new_picture_name = "zdjecie-profilowe-" + new_user.first_name + "-" + new_user.last_name + extension

                if ExtendUser.objects.filter(avatar_picture=new_picture_name):
                    new_picture_name = "zdjecie-profilowe-" + new_user.first_name + "-" + new_user.last_name + str(
                        random.randint(1, 1000)) + extension
                else:
                    rename(settings.MEDIA_ROOT + str(new_extended_user.avatar_picture), settings.MEDIA_ROOT + new_picture_name)
                new_extended_user.avatar_picture = new_picture_name
                new_extended_user.save()

            else:
                new_extended_user = ExtendUser.objects.create(
                    email_privacy=email_privacy,
                    phone_number=phone,
                    phone_privacy=phone_privacy,
                    skype=skype,
                    skype_privacy=skype_privacy,
                    instagram_id=instagram,
                    instagram_privacy=instagram_privacy,
                    facebook_id=facebook,
                    facebook_privacy=facebook_privacy,
                    website=website,
                    website_privacy=website_privacy,
                    about_me=about_me,
                    region_id=user_region_id,
                    user_id=new_user_id,
                    slug=cleaned_slug,
                )
                return HttpResponse("User Created, NO AVATAR")

            ctx = {"new_user":new_user, "new_extended_user":new_extended_user}
            return render(request, "user_registration_response.html", ctx)
        else:
            regions = Regions.objects.filter(county_id=None)
            ctx = {"regions": regions, "form": form}
            return render(request, "user_registration.html", ctx)


# -----User Page------
class user_page(View):
    def get(self, request, voivodeship, name, id):
        user_data = User.objects.get(id=id)
        user_pictures = Picture.objects.filter(picture_user_id_id=id)
        user_stat = {}
        pictures_views = user_pictures.aggregate(Sum('views'))
        pictures_views = pictures_views['views__sum']
        if pictures_views == None:
            pictures_views = 0
        user_stat["views"] = pictures_views

        ratings_sum = 0
        ratings_num = 0
        for pic in user_pictures:
            ratings = pic.picturerating_set.all()
            for rat in ratings:
                ratings_sum = ratings_sum + rat.rating
                ratings_num += 1
        if ratings_num == 0:
            picture_rating_average = 'n/a'
        else:
            picture_rating_average = ratings_sum / ratings_num
            picture_rating_average = round(picture_rating_average, 1)
        user_stat["av_rating"] = picture_rating_average

        user_region_id = user_data.extenduser.region_id
        user_voivodeship_id = Regions.objects.get(id=user_region_id).voivodeship_id
        user_county_id = Regions.objects.get(id=user_region_id).county_id
        user_municipality_id = Regions.objects.get(id=user_region_id).municipality_id

        user_voivodeship = Regions.objects.get(voivodeship_id=user_voivodeship_id, county_id__isnull=True,
                                               municipality_id__isnull=True).city
        user_voivodeship = user_voivodeship.lower()
        user_stat["user_voivodeship"] = user_voivodeship

        if user_county_id == None and user_municipality_id == None:
            user_county = "nie podano"
            user_city = "nie podano"
        elif user_county_id == None:
            user_city = "nie podano"
        else:
            user_county = Regions.objects.get(voivodeship_id=user_voivodeship_id, county_id=user_county_id,
                                              municipality_id__isnull=True).city

            user_city = Regions.objects.get(voivodeship_id=user_voivodeship_id, county_id=user_county_id,
                                            municipality_id=user_municipality_id).city

        user_city = user_city.lower()
        user_stat["user_city"] = user_city
        user_county = user_county.lower()
        user_stat["user_county"] = user_county

        ctx = {"user": user_data, "pictures": user_pictures, "user_stat": user_stat}
        return render(request, "user_page.html", ctx)


# -----------------------------PICTURES-----------------------------
# ----------All pictures & all pictures in categories--------

class AllPictures(View):
    def get(self, request, category_slug, id):
        categ_id = int(id)
        if categ_id == 0:
            all_pictures = Picture.objects.all()
            category = "wszystkie zdjecia"
        else:
            try:
                all_pictures = Picture.objects.filter(picture_category_id=categ_id)
                category = PictureCategory.objects.get(id=categ_id)
            except ObjectDoesNotExist:
                ctx = {"msg": "Nie ma takiej kategorii"}
                return render(request, "standard_error_page.html", ctx)
        ctx = {"pictures": all_pictures, "category": category}
        return render(request, "all_pictures.html", ctx)


class PictureView(View):
    def get(self, request, category_slug, picture_slug, id):
        picture_to_display = Picture.objects.get(id=id)
        picture_owner_id = picture_to_display.picture_user_id_id
        picture_owner_info = ExtendUser.objects.get(user_id=picture_owner_id)
        picture_comments = PictureComment.objects.filter(picture_id_id=id)
        average_picture_rating = PictureRating.objects.filter(picture_id_id=id).aggregate(Avg('rating'))
        average_picture_rating = round(average_picture_rating['rating__avg'], 2)

        all_commenters = []
        for usr in picture_comments:
            commenter = ExtendUser.objects.get(user_id=usr.commenter)
            all_commenters.append(commenter)

        ctx = {"picture": picture_to_display, "owner": picture_owner_info, "comments": picture_comments,
               "commenters_array": all_commenters, "picture_rating": average_picture_rating}
        return render(request, "picture_view.html", ctx)


# -----------------------COMMENTS / RATINGS-----------------------------


# ----------------------------TAGS--------------------------------------
class TagView(View):
    def get(self, request, tag_slug, id):
        tag_id = int(id)
        try:
            all_tagged_pictures = PictureTags.objects.filter(picture_tag_id=id)
            tag = Tags.objects.get(id=id)
        except ObjectDoesNotExist:
            ctx = {"msg": "Nie ma takiego Tag'a"}
            return render(request, "standard_error_page.html", ctx)
        ctx = {"pictures": all_tagged_pictures, "tag": tag}

        return render(request, "tag_pictures.html", ctx)

# -------------------------SYSTEM----------------------------------
class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            msg = "jesteś już zalogowany!"
            return render(request, "standard_error_page.html", {"msg": msg})
        else:
            form = LoginForm()
            ctx = {"form": form}
            return render(request, "login_page.html", ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            User = authenticate(username=username, password=password)
            if User is not None:
                login(request, User)
                msg = 'zalogowano!'
            else:
                msg = 'niepoprawny login, spróbuj ponownie!'
        else:
            return redirect('login')
        return render(request, "login_page.html", {'form': form, 'msg': msg, "user":User})

class Logout(View):
    def get(self, request):
        logout(request);
        return redirect('main_page')