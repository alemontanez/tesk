# Modulos
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import CreateTask

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
    return render(request, "home.html")


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
    # Si el metodo HTTP es "GET", el servidor va a renderizar el Formulario de Tareas
    if request.method == 'GET':
        return render(request, 'tasks.html', {
            'form': CreateTask
        })
    # Si el metodo es "POST", crea la tarea y la guarda en la BBDD
    else:
        form = CreateTask(request.POST)
        new_task = form.save(commit=False)
        # Aca verifica que el usuario este logeado
        new_task.user = request.user
        new_task.save()
        return redirect('proyectos')

@login_required
def projects_view(request):
    return render(request, "proyectos.html")

@login_required
def signout_user(request):
    # Función para cerrar sesión, al hacerlo nos redirigirá a nuestro index
    logout(request)
    return redirect("index")
