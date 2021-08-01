from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from backend.views import *

from django.conf import settings
from django.conf.urls.static import static

router = SimpleRouter()


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('user/register/', SignInView.as_view()),
                  path('user/login/', LoginView.as_view()),
                  path('object/compressor/', FacilityView.as_view()),
                  path('object/powerplant/', FacilityView.as_view()),
                  path('object/boiler/', FacilityView.as_view()),
                  path('chemical/', GasCompositionView.as_view()),
                  path('mining/', MiningDepartmentView.as_view()),
                  path('environment/', EnvironmentDepartmentView.as_view()),
                  path('archive/', ArchiveView.as_view()),
                  path('main/', MainView.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
