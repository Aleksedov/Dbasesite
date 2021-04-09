from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('victims/', views.victims, name='victims'),
    path('guiltys/', views.guiltys, name='guiltys'),
    path('cases/', views.cases, name='cases'),
    path('victims/<int:pk>', views.VictimDetailView.as_view(), name='victim'),
    path('guiltys/<int:pk>', views.GuiltyDetailView.as_view(), name='guilty'),
    path('persecution/<int:pk>', views.PersDetailView.as_view(), name='persecution'),
    path('cases/<int:pk>', views.CaseDetailView.as_view(), name='case'),
]