"""
URL configuration for ecomm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import CustomSignupView, login_signup_view
from shop.views import index
from allauth.account import views as allauth_views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    # path('accounts/login/', include('allauth.urls')),
    path('accounts/login/', allauth_views.LoginView.as_view(template_name='accounts/login_signup.html'), name='account_login'),
    # path('accounts/login/', login_signup_view, name='account_login_signup'),

    # path('accounts/signup/', allauth_views.SignupView.as_view(template_name='accounts/login_signup.html'), name='account_signup'),
    # path('accounts/signup/', RedirectView.as_view(url='/accounts/login/#signup', permanent=False), name='account_signup'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),

    path('accounts/', include('allauth.urls')),
    # path('accounts/profile/', index)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
