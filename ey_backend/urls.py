"""
URL configuration for ey_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from user.views import GoogleLogin,VerifyCode,CompleteSignup,PasswordResetView
from dj_rest_auth import urls
urlpatterns = [

    path('admin/', admin.site.urls),
    path("user/",include("user.urls")),
    path('/api/', include('rest_framework.urls')),
    path('api/auth/password/reset/',PasswordResetView.as_view(),name="start_password_reset"),
    path("api/auth/completesignup", CompleteSignup.as_view(),name="complete_signup"),
    path("api/auth/verifyotp", VerifyCode.as_view(),name="verify_otp_code"),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)