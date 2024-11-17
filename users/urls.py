from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig

from . import views

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path(
        "logout/", LogoutView.as_view(next_page="mailing:index"), name="logout"
    ),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", views.email_verification, name="email-confirm"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
