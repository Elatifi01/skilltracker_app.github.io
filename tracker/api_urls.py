from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import SkillViewSet, ProgressEntryViewSet, GoalViewSet, LearningResourceViewSet, DashboardAPIView

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'progress', ProgressEntryViewSet, basename='progress')
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'resources', LearningResourceViewSet, basename='resource')
router.register(r'dashboard', DashboardAPIView, basename='dashboard')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
]
