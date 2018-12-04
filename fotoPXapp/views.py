from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest, Http404
from django.conf import settings
from os import path, rename, remove
from json import dumps
from fotoPXapp.models import User, ExtendUser, Regions, Picture, PictureCategory, PictureTags, PictureRating, \
    PictureComment, Followers, Tags
from PIL import Image


# ------------MAIN PAGE, HEADER , FOOTER-----------------------
class MainPage(View):
    def get(self, request):
        ctx = {}
        return render(request, "main_page.html", ctx)


# -----------------------------USER-----------------------------
class user_registration(View):
    def get(self, request):
        voId = request.GET.get('voivodeship_id')
        if voId == None:
            regions = Regions.objects.filter(county_id=None)
            ctx = {"regions": regions}
            return render(request, "user_registration.html", ctx)
        else:
            regions = Regions.objects.filter(voivodeship_id=voId, municipality_id=None, county_id__isnull=False)
            response_data = {}
            for el in regions:
                response_data[el.county_id] = el.city
            return HttpResponse(dumps(response_data), content_type="application/json")

    def post(self, request):
        voId = request.POST.get('voivodeship_id')
        print(voId)

        return None


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
        all_commenters = []
        for usr in picture_comments:
            commenter = ExtendUser.objects.get(user_id=usr.commenter)
            all_commenters.append(commenter)
        print(all_commenters)


        ctx = {"picture": picture_to_display, "owner": picture_owner_info, "comments": picture_comments,
               "commenters_array": all_commenters}
        return render(request, "picture_view.html", ctx)

# -----------------------COMMENTS / RATINGS-----------------------------


# ----------------------------TAGS--------------------------------------
