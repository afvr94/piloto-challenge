from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import EventViewSet
from .views import index
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(
    r"events", EventViewSet, "events"
)

# TODO: Change route to something like /piloto_admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
