from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('profile', views.profile, name="profile"),
    path('define_rate', views.define_rate_view, name="define_rate"),
    path('bibliotheque', views.bibliotheque_view, name="bibliotheque"),
    path('control', views.control_view, name="control"),

]
