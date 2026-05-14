from django.urls import path

from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_behavior, name='create_behavior'),
    path('<int:behavior_id>/', views.behavior_dashboard, name='behavior_dashboard'),
]