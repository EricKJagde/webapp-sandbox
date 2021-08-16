from django.urls import path

from . import views


app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('post/', views.post, name='post'),
    path('roster/', views.roster, name='roster'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_spec, name='profile_spec'),
    path('about/', views.about, name='about'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
