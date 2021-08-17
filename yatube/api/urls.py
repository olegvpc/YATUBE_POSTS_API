from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# pip install -U drf-yasg
# pip install -U drf-yasg[validation]
# INSTALLED_APPS = [
#    ...
#    'django.contrib.staticfiles',  # required for serving swagger ui's css/js files
#    'drf_yasg',
#    ...
# ]

# SWAGGER_SETTINGS = {
#    'SECURITY_DEFINITIONS': {
#       # 'Basic': {
#       #       'type': 'basic'
#       # },
#       'Token': {
#             'type': 'apiKey',
#             'name': 'Authorization',
#             'in': 'header'
#       }
#    }
# }

from django.conf.urls import include, url
from django.urls import path

from .views import CommentViewSet, GroupViewSet, PostViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                                 CommentViewSet, basename='comments')

urlpatterns = [
    url(r'^', include(router_v1.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
