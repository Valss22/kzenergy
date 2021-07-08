from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from backend.views import *

from django.conf import settings
from django.conf.urls.static import static

router = SimpleRouter()

router.register(r'gasComposition', GasCompositionViewSet)

FacilityView.model = Compressor
FacilityView.model_serializer = CompressorSerializer

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('user/register/', SignInView.as_view()),
                  path('user/login/', LoginView.as_view()),
                  # path('compressor/', CompressorView.as_view()),
                  path('object/compressor/', FacilityView.as_view()),
                  path('object/powerplant/', FacilityView.as_view()),
                  path('object/boiler/', FacilityView.as_view()),
                  path('compressor/create/', CreateFacilityView.as_view()),
                  path('powerplant/create/', CreateFacilityView.as_view()),
                  path('boiler/create/', CreateFacilityView.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
