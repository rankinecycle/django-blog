"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from personal.views import (
	home_screen_view,
	)

from account.views import (
        registration_view,
        logout_view,
        login_view,
        account_view,
        must_authenticate_view,
    )


urlpatterns = [
    path('', home_screen_view, name = 'home'),
    path('admin/', admin.site.urls),
    path('account/', account_view, name="account"),
    path('blog/', include('blog.urls' , "blog" )), 
    # to include urls.py form blog folder, and any URL from blog folder will start from blog/
    path('comments/', include('comments.urls' , "comments" )),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('register/', registration_view, name="register"),


    #path('account/', include('django.contrib.auth.urls')),
    # Copied links from mitch github. Ex =auth_views.PasswordChangeDoneView ==these are default views created in django.contrib.auth. 
    #link: https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/views/
    # password_change_done.html== Thse are the custom templates we will create to modify these default views
    # 'password_change/done/' == These URLs must be present for password reset, (shown in django doc)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'), # use exact same names to avoid errors

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
]

if settings.DEBUG: #if in dev env, this is telling where the media and static urls are
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
