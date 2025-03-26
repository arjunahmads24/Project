"""heypo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.urls import path
from articles.views import (
    front_page,
    search_page,
    article_page,
    ew_page,
    category_page,
    topic_page,
    activate_email,
    error_404_page,
    about_us_page,
    privacy_policy_page,
    terms_and_conditions_page,
)


urlpatterns = [
    path('', front_page),
    path(os.environ.get('DJANGO_ADMIN_URL'), admin.site.urls),
    path('about-us/', about_us_page),
    path('privacy-policy/', privacy_policy_page),
    path('terms-and-conditions/', terms_and_conditions_page),
    path('search/<int:page>/', search_page),
    path('article/<str:slug>/', article_page, name='article'),
    path('ew/<str:ew>/<int:page>/', ew_page),
    path('topic/<str:topic>/<int:page>/', topic_page),
    path('<str:category>/<int:page>/', category_page),
    path('activate/<uidb64>/<token>', activate_email, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = error_404_page
# handler404 = 'articles.views.error_404_page'
