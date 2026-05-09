from django.urls import path

from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:behavior_id>/', views.behavior_dashboard, name='behavior_dashboard'),
]