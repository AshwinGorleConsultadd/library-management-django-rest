# from django.contrib import admin
# from django.urls import path, include
# from home.views import home
# from rest_framework import permissions
# from django.urls import re_path
# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
#
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Library Management API",
#       default_version='v1',
#       description="API documentation for the library system",
#       terms_of_service="https://www.example.com/terms/",
#       contact=openapi.Contact(email="support@example.com"),
#       license=openapi.License(name="MIT License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )
#
# urlpatterns = [
#     path('', home, name='home'),
#     path('admin/', admin.site.urls),
#     path('api/auth/', include('user.urls')),
#     path('api/books/', include('books.urls')),
#     path('api/transactions/', include('transactions.urls')),
# ]
#
#

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path, include
from django.contrib import admin
from home.views import home

schema_view = get_schema_view(
    openapi.Info(
        title="Library Management API",
        default_version='v1',
        description="API documentation for the library system",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # Your existing API URLs
        path('', home, name='home'),
        path('api/auth/', include('user.urls')),
        path('api/books/', include('books.urls')),
        path('api/transactions/', include('transactions.urls')),

    # Swagger UI
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # ReDoc UI
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Raw schema
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
