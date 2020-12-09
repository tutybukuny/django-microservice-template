"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import rest_framework
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from apps.auths.views import LoginView
from apps.users.views import UserViewSet

swagger_info = openapi.Info(
    title="Loc-Sharing API",
    default_version="v1",
    description="""Microservice""",
    contact=openapi.Contact(email="thienthn@ftech.ai"),
    license=openapi.License(name="Private")
)

schema_view = get_schema_view(
    info=swagger_info,
    public=True,
    authentication_classes=[rest_framework.authentication.SessionAuthentication],
    permission_classes=[permissions.IsAdminUser],
)

api_router = SimpleRouter(trailing_slash=False)
api_router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/v1/', include(api_router.urls)),
    path(r'api/v1/login', LoginView.as_view()),
]

urlpatterns.extend([
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
])
