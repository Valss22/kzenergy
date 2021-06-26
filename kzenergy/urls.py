
from django.contrib import admin
from django.urls import path

from backend.views import SignInView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register/', SignInView.as_view()),
    path('user/login/', LoginView.as_view()),
]
