from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models.aggregates import Avg, Sum
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest, Http404
from django.views import View
from django.conf import settings
from os import path, rename, remove
from json import dumps

# from psycopg2._psycopg import IntegrityError

from fotoPXapp.models import User, ExtendUser, Regions, Picture, PictureCategory, PictureTags, PictureRating, \
    PictureComment, Followers, Tags
from fotoPXapp.GlobalFunctions import ReplacePolishCharacters
from PIL import Image
from fotoPXapp.forms import RegisterForm


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
        print(voId)

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

            try:
                new_user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                new_user.save()
            except IntegrityError:
                regions = Regions.objects.filter(county_id=None)
                error = "wprowadzona nazwa użytkownika jest już zajęta, wybierz inną"
                ctx = {"regions": regions, "form": form, "error": error}
                return render(request, "user_registration.html", ctx)

            if 'avatar_picture' in request.FILES:
                avatar_picture = request.FILES["avatar_picture"]
                im = Image.open(avatar_picture)
                im.save(settings.MEDIA_ROOT + "xxxxxxxxx.jpg", "JPEG")
                return  HttpResponse("SAVED")
            else:
                return HttpResponse("No Picture")
                pass



            return HttpResponse("KONIEC FUNKCJI POST" + first_name + str(voivodeship_id))
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
        user_county = Regions.objects.get(voivodeship_id=user_voivodeship_id, county_id=user_county_id,
                                          municipality_id__isnull=True).city
        user_county = user_county.lower()
        user_stat["user_county"] = user_county
        user_city = Regions.objects.get(voivodeship_id=user_voivodeship_id, county_id=user_county_id,
                                        municipality_id=user_municipality_id).city
        user_city = user_city.lower()
        user_stat["user_city"] = user_city

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
