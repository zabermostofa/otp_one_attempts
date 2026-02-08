from django.urls import path
from . import views

urlpatterns = [
    path('',views.base,name='base'),
    path('home/',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('otp_view/',views.otp_view,name='otp_view'),
    path('user_list/',views.user_list,name='user_list'),
]
