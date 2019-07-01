"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from usuario.views import indexView, login , loginView, logout, adminView, adminUserView,comprar, adminView, saveuser,deleteuser
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.conf import settings

from defender.decorators import watch_login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexView),
    path('login/', watch_login()(loginView)),
    path('auth/login/', login),
    path('auth/logout/', logout),
    path('administrador/', adminView),
    path('administrador/users/delete/', deleteuser),
    path('administrador/users/save/', saveuser),
    path('administrador/users/', adminUserView),
    path ('comprar/', comprar)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
