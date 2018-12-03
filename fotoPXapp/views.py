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
class AllPictures(View):
    def get(self, request):
        all_pictures = Picture.objects.all()

        ctx = {"pictures": all_pictures}
        return render(request, "all_pictures.html", ctx)

# -----------------------COMMENTS / RATINGS-----------------------------


# ----------------------------TAGS--------------------------------------
