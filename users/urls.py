from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


app_name = "users" 

urlpatterns = [
    path("register",views.register,name="register"),
    path("login",views.userlogin,name="login"),
    path("logout",views.HandleLogout,name="logout"),
    path("profile",views.profile,name="profile"),
    path("update_profile",views.updateProfile,name="updateprofile"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path("password-reset",
        auth_views.PasswordResetView.as_view(
                template_name="users/password_reset.html",
                email_template_name = 'users/password_reset_email.html'
            ),
        name="password_reset"),
    path("password-reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
            ),
        name="password_reset_done"),
    # path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    # path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),

    # path("logout",auth_views.LogoutView.as_view(template_name="users/logout.html"),name="logout"),
]
#  owxynejqccfqlpdw