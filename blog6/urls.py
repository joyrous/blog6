"""blog6 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from post import views as post_views
from users import views as users_views


urlpatterns = [
    path('', post_views.home),
    path('post/home/', post_views.home),
    path('post/article/', post_views.article),
    path('post/editor/', post_views.editor),
    path('post/create/', post_views.create),
    path('post/comment/', post_views.comment),
    path('post/search/', post_views.search),

    path('users/register',users_views.register),
    path('user/login/', users_views.login),
    path('user/logout/', users_views.logout),
    path('user/info/', users_views.info),

]
