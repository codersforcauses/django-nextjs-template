from rest_framework_nested import routers

from . import views

# /api/ prefix
router = routers.SimpleRouter()
router.register(r'enclosures', views.EnclosureViewSet, basename='enclosures')
router.register(r'habitats', views.HabitatViewSet, basename='habitats')
