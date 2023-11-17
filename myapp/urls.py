from django.urls import path
from . import views

urlpatterns = [
    # Index
    path("", views.home, name="home"),
    # Login de usuarios
    path("login/", views.login_user, name="login_user"),
    # Registro de usuarios
    path("register/", views.register_user, name="register_user"),
    # Vista de proyectos despues del registro o inicio de sesion
    path("proyectos/", views.projects_view, name="proyectos"),
    # Cerrar sesion
    path("logout/", views.signout, name="logout"),
]