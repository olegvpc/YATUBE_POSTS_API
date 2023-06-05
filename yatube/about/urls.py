from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    # path('author/', views.AboutAuthorView.as_view(), name='author'),
    path('author/', views.AboutAuthorView.as_view(), name='portfolio'),
    path('author/en', views.AboutAuthorViewEng.as_view(), name='portfolio_eng'),
    path('tech/', views.AboutTechView.as_view(), name='tech'),

]
