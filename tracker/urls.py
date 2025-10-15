from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('skills/', views.SkillListView.as_view(), name='skill_list'),
    path('skills/add/', views.SkillCreateView.as_view(), name='skill_add'),
    path('progress/', views.ProgressListView.as_view(), name='progress_list'),
    path('progress/add/', views.ProgressCreateView.as_view(), name='progress_add'),
    path('goals/', views.GoalListView.as_view(), name='goal_list'),
    path('goals/add/', views.GoalCreateView.as_view(), name='goal_add'),
    path('goals/<int:pk>/toggle/', views.GoalToggleView.as_view(), name='goal_toggle'),
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/add/', views.ResourceCreateView.as_view(), name='resource_add'),
    path('resources/<int:pk>/toggle/', views.ResourceToggleView.as_view(), name='resource_toggle'),
    
    path('api/progress-chart/', views.ProgressChartDataView.as_view(), name='progress_chart_data'),
    path('api/skill-stats/<int:skill_id>/', views.SkillStatsView.as_view(), name='skill_stats'),
]
