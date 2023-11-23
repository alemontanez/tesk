from django.urls import path
from . import views

urlpatterns = [
    # Paginas principales
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),

    # Sistema de logeo
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.signout_user, name="signout_user"),
    path("register/", views.register_user, name="register_user"),

    # Rutas de proyectos
    path("project/create/", views.create_project, name="create_project"),
    path("project/<int:project_id>/", views.main_section, name="main_section"),

    # Rutas de tareas
    path("task/create/", views.create_task, name="create_task"),
]