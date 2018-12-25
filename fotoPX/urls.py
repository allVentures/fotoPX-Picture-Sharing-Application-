"""fotoPX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from fotoPXapp.views import user_registration, MainPage, AllPictures, PictureView, user_page, TagView, LoginPage, Logout, \
    AddPicture, AllUsers

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', admin.site.urls),
    url(r'^rejestracja', user_registration.as_view(), name="user_registration"),
    url(r'^logout', Logout.as_view(), name="logout"),
    url(r'^login', LoginPage.as_view(), name="login"),
    url(r'^uzytkownicy', AllUsers.as_view(), name="allusers"),
    url(r'^dodaj-zdjecie', AddPicture.as_view(), name="add_picture"),
    url(r'^$', MainPage.as_view(), name="main_page"),
    re_path(r'^kategoria/(?P<category_slug>[A-Za-z-]+)/(?P<id>[0-9]+)$', AllPictures.as_view(), name="all_pictures"),
    re_path(r'^(?P<category_slug>[A-Za-z-]+)/(?P<picture_slug>[A-Za-z0-9-]+)/(?P<id>[0-9]+)$', PictureView.as_view(),
            name="picture_view"),
    re_path(r'^fotograf/(?P<voivodeship>[A-Za-z-]+)/(?P<name>[A-Za-z0-9-]+)/(?P<id>[0-9]+)$', user_page.as_view(),
            name="user_page"),
    re_path(r'^zdjecia/tag/(?P<tag_slug>[A-Za-z0-9-]+)/(?P<id>[0-9]+)$', TagView.as_view(), name="tag_all_pictures"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
