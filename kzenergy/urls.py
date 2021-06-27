
from django.contrib import admin
from django.urls import path

from backend.views import SignInView, LoginView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register/', SignInView.as_view()),
    path('user/login/', LoginView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
