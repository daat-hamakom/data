from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .maps.views import *

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'annotations', AnnotationViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'people', PersonViewSet)
router.register(r'organizations', OrganizationViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^s3direct/', include('s3direct.urls')),
    url(r'^select2/', include('django_select2.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
