# Modulos
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import Priority, Project, Task
from .forms import CreateTask, CreateProject

"""
Pagina de inicio
"""
def index(request):
    return render(request, "index.html")

"""
Pagina de inicio (usuario)
"""
@login_required
def home(request):
    projects = Project.objects.all()
    return render(request, "home.html", {'projects': projects,})

"""
Funcion para registrar a los nuevos usuario
"""
def register_user(request):
    # Si el metodo HTTP es "GET", el servidor va a renderizar el Formulario de Registro
    if request.method == "GET":
        return render(request, "register.html", {"form": UserCreationForm})
    # Si el metodo es otro, en este caso va a ser "POST", el servidor va a verificar que ambas contraseñas coincidan
    else:
        # Si ambas coinciden, va a intentar registrar el usuario y la contraseña
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                # Se guarda en la base de datos
                user.save()
                login(request, user)
                # Y se lo redirecciona a la pagina de los proyectos.
                return redirect("proyectos")
            # De existir un error, va a renderizar nuevamente el formulario
            except IntegrityError:
                return render(
                    request,
                    "register.html",
                    {"form": UserCreationForm, "error": "Usuario ya existente"},
                )
        return render(
            request,
            "register.html",
            {"form": UserCreationForm, "error": "Las contraseñas no coinciden"},
        )

"""
Funcion para iniciar sesion
"""
def login_user(request):
    # Cuando la solicitud que hace el cliente es "POST"
    if request.method == "POST":
        # El servidor va a verificar si el usuario y la contraseña se encuentran en la base de datos.
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Y luego de inciar sesion, se los redirecciona a la pagina de proyectos.
            return redirect("home")
        else:
            # Si existe algun error, se le informa el error.
            return render(
                request, "login.html", {"error": "Usuario y/o contraseña incorrectos."}
            )
    # En caso de que el cliente no ejecute un metodo "POST", el servidor no hara nada.
    else:
        return render(request, "login.html")

"""
Funcion para crear las tareas
"""
@login_required
def create_task(request):
    projects = Project.objects.all()
    users = User.objects.all()
    priority = Priority.objects.all()

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': CreateTask,
            'users': users,
            'projects': projects,
            'prioritys': priority,
        })
    else:
        try:
            form = CreateTask(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('home')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': CreateTask,
                'error': 'Por favor ingrese informacion valida'
            })

"""
Funcion para crear los proyectos
"""
@login_required
def create_project(request):
    projects = Project.objects.all()
    if request.method == 'GET':
        return render(request, 'create_project.html', {
            'form': CreateProject,
            'projects': projects,
        })
    else:
        form = CreateProject(request.POST)
        new_project = form.save(commit=False)
        new_project.user = request.user
        new_project.save()
        return redirect("home")


"""
Funcion para ver la vista detallada de cada proyecto
"""
@login_required
def main_section(request, project_id):
    projects = Project.objects.all()
    project = get_object_or_404(Project, pk = project_id)
    tasks = Task.objects.filter(project_id = project_id)
    return render(request, "main_section.html", {
        'project': project,
        'projects': projects,
        'tasks': tasks,
    })

"""
Funcion para cerrar la sesion del usuario
"""
@login_required
def signout_user(request):
    # Función para cerrar sesión, al hacerlo nos redirigirá a nuestro index
    logout(request)
    return redirect("index")
