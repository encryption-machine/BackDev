from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls', namespace='api'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

schema_view = get_schema_view(
   openapi.Info(
      title="Encryption machine API",
      default_version='v1',
      description='Документация для проекта "Шифровальная машина"'
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
]
