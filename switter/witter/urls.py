from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list', views.profile_list, name="profile_list"),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register, name="register"),
    path('update_user', views.update_user, name="update_user"),
    path('update_password/<int:pk>', views.update_password, name="update_password"),
    path('profile/follows/<int:pk>', views.follows, name="follows"),
    path('profile/followers/<int:pk>', views.followers, name="followers"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('swit_like/<int:pk>', views.swit_like, name="swit_like"),
    path('swit_show/<int:pk>', views.swit_show, name="swit_show"),
    path('delete_swit/<int:pk>', views.delete_swit, name="delete_swit"),
    path('edit_swit/<int:pk>', views.edit_swit, name="edit_swit"),
    path('search_swit', views.search_swit, name="search_swit"),
    path('search_user', views.search_user, name="search_user"),
]
