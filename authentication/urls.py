from . import views
from django.urls import path
from django.views import generic


urlpatterns = [
    path(
        "signup/",
        views.UserCreationView.as_view(),
        name="signup"
    ),

    path(
        'login/',
        views.LoginView.as_view(),
        name='login'

    ),

    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'

    ),

    path(
        'activate/<uidb64>/<token>/',
        views.AccountActivationView.as_view(),
        name='activate'
    ),


    path(
        'activate-account-message/',
        generic.TemplateView.as_view(
            template_name="auth/activate-account-message.html"),
        name='activate-account-message'
    ),


    path(
        'create-profile/',
        views.CreateProfileView.as_view(),
        name='create-profile'
    ),

]
