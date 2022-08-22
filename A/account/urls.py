from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserloginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset2/', views.UserPasswordResetView2.as_view(), name='reset_password2'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>', views.UserUnfollowView.as_view(), name='user_unfollow'),
    path('edit-user', views.EditUserView.as_view(), name='edit_user'),
]