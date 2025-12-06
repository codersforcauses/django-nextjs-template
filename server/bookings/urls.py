from rest_framework_nested import routers

from . import views

# /api/ prefix
router = routers.SimpleRouter()
router.register(r'feedings', views.FeedingViewSet, basename='feedings')
