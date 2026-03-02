from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_api

router = DefaultRouter()
router.register(r'about', views_api.AboutViewSet)
router.register(r'projects', views_api.ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', views_api.contact_submit, name='contact'),
]
