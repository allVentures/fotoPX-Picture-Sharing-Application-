from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpRequest, Http404
from django.conf import settings
from os import path, rename, remove
from json import dumps
from fotoPXapp.models import User, Regions
from PIL import Image


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
        # voId = request.POST
        # form = AddStudentForm(request.POST)
        print("ddd")
        voId = request.POST.get('voivodeship_id')
        print(voId)


            # new_student.first_name = form.cleaned_data['name']

        return None

# -----------------------------PICTURES-----------------------------