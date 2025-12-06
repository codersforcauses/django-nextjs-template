"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter
from rest_framework.routers import APIRootView

from zoo.urls import router as enclosures_router
from bookings.urls import router as feedings_router
from users.urls import router as auth_router

router = DefaultRouter()
router.APIRootView = APIRootView
router.registry.extend(enclosures_router.registry)
router.registry.extend(feedings_router.registry)
router.registry.extend(auth_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/healthcheck/", include("healthcheck.urls")),
    path('api/', include(router.urls)),
]
