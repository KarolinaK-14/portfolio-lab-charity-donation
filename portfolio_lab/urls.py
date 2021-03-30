"""portfolio_lab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from charity_donation import views as v
from .settings import DEBUG
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', v.Login.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page="landing_page"), name="logout"),
    path('', v.LandingPage.as_view(), name='landing_page'),
    path('add-donation/', v.AddDonation.as_view(), name='add_donation'),
    path('donation-confirmation/', v.DonationConfirmation.as_view(), name='donation_confirmation'),
    path('register/', v.Register.as_view(), name='register'),
    path('user/', v.User.as_view(), name='user'),
    path('archive/<int:pk>/', v.Archive.as_view(), name='archive'),
    path('edit-user/', v.UserUpdate.as_view(), name='edit-user'),
    path('change-password/', v.PasswordChange.as_view(), name='change-password'),
    path('activate/<uidb64>/<token>/', v.ActivateAccount.as_view(), name='activate'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     v.activate, name='activate')
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
