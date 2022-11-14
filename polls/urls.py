from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('levels/', views.LevelsView.as_view(), name='levels_index'),
    path('level/', views.level_detail, name='level_detail'),
    path('bs_test/', views.bootstrap_test, name='bs_test'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
