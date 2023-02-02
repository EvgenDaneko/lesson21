from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginUser, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('account/', views.userAccount, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('create-skill/', views.createSkill, name='create-skill'),
    path('update-skill/<slug:skill_slug>', views.updateSkill, name='update-skill'),
    path('delete-skill/<slug:skill_slug>', views.deleteSkill, name='delete-skill'),


    path('', views.profiles, name='profiles'),
    path('profile/<str:username>', views.userProfile, name='user-profile'),
    path('skill/<slug:skill_slug>', views.profiles_by_skill, name='skill'),
]