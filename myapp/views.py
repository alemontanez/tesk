# Modulos
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone

"""
get_object_or_404: Sirve para obtener un objeto de la base de datos por su clave primaria (pk). Si el objeto no existe, devuelve una página de error 404.
redirect: Redirige a los usuarios a una URL específica.
render: Renderiza una plantilla con datos específicos y devuelve la página HTML resultante como respuesta.
UserCreationForm: Es un formulario proporcionado por Django para la creación de nuevos usuarios. Contiene campos como username y password.
UserChangeForm: Es un formulario proporcionado por Django para la modificación de usuarios existentes. Permite cambiar campos como username y password.
User: Es el modelo de usuario predeterminado en Django. Contiene campos como username, password, email, etc.
login, logout, authenticate: Funciones para gestionar la autenticación de usuarios en Django. login inicia sesión, logout cierra la sesión y authenticate verifica las credenciales del usuario.
login_required: Un decorador que asegura que la vista solo sea accesible para usuarios autenticados.
IntegrityError: Excepción que se levanta cuando hay violación de integridad en la base de datos, como un intento de insertar un registro duplicado.
timezone: Proporciona funciones para trabajar con zonas horarias y obtener la hora actual teniendo en cuenta la zona horaria del sistema.
"""

from .models import Priority, Project, Task, TaskCondition
# Importamos los modelos de nuestro archivo models.py para poder usarlos y extraer información de la base de datos
from .forms import CreateTask, CreateProject
# Importamos los formularios creados en nuestro archivo forms.py

"""
Pagina de inicio
"""
def index(request):
    # Si hay una sesión iniciada e intenta moverse a la url de index, lo redirige a home
    if request.user.is_authenticated:
        return redirect("home")
    # Sino renderiza nuestro index.html, donde podrá seleccionar login o register, o solo visualizar el index
    else:
        return render(request, "index.html")

"""
Página de inicio con usuario logueado.
La función realiza una solicitud GET, con los proyectos para renderizar en el aside.
Solicita que usuario está logueado, y almacena su id en una variable aparte.
Consulta y almacena en una variable la hora y fecha actual de la zona establecida. Luego comienza una sentencia if, la cual dependiendo el horario va a almacenar en la variable momento un string, el cual usaremos para renderizar en el título del home y será dinámico según el horario.
Luego renderizamos al template home.html solicitando el diccionario con los objetos que se fueron obteniendo en la función.
"""
@login_required
def home(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        user = request.user
        user_id = request.user.id
        time = timezone.now()
        tasks = Task.objects.all()
        
        # Compara solo la hora, minutos y segundos
        if time.time() >= timezone.make_aware(timezone.datetime(time.year, time.month, time.day, 7, 0, 0)).time() and time.time() < timezone.make_aware(timezone.datetime(time.year, time.month, time.day, 12, 0, 0)).time():
            moment = 'Buen día'
        elif time.time() >= timezone.make_aware(timezone.datetime(time.year, time.month, time.day, 12, 0, 0)).time() and time.time() < timezone.make_aware(timezone.datetime(time.year, time.month, time.day, 20, 0, 0)).time():
            moment = 'Buenas tardes'
        else:
            moment = 'Buenas noches'
            
        return render(request, "home.html", {
            'projects': projects, 
            'user': user,
            'user_id': user_id,
            'time': time,
            'tasks': tasks,
            'moment': moment,
            })


"""
Función para registrar usuarios.
Si la solicitud es un GET, se renderiza la página de registro con el formulario vacío.
Si la solicitud es un POST, se verifica que las contraseñas ingresadas coincidan.
Si coinciden, intenta registrar al usuario con los datos proporcionados y realiza el inicio de sesión.
Si hay un error de integridad (usuario ya existente), se renderiza nuevamente el formulario con un mensaje de error.
Si las contraseñas no coinciden, se renderiza nuevamente el formulario con un mensaje de error.
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
                    username = request.POST["username"],
                    password = request.POST["password1"],
                    first_name = request.POST["firstname"],
                    last_name = request.POST["lastname"]
                )
                # Se guarda en la base de datos
                user.save()
                login(request, user)
                # Y se lo redirecciona a la pagina de los proyectos.
                return redirect("home")
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
Función para iniciar sesion.
Si la solicitud es un POST, se verifica si el usuario y la contraseña proporcionados coinciden con algún usuario en la base de datos.
Si la autenticación es exitosa, se realiza el inicio de sesión y se redirecciona al usuario a la página de proyectos.
Si la autenticación falla, se renderiza la página de inicio de sesión con un mensaje de error.
Si la solicitud no es un POST, simplemente renderiza la página de inicio de sesión.
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
Función para cerrar la sesion del usuario.
Utilizamos la función logout propia de django.
Al hacerlo, redireccionamos la vista del usuario al index.
"""
@login_required
def signout_user(request):
    # Función para cerrar sesión, al hacerlo nos redirigirá a nuestro index
    logout(request)
    return redirect("index")

"""
Función para crear los proyectos
Decoramos la función con @login_required, para proteger la ruta y asegurarnos que solo se pueda acceder a la misma con un usuario autenticado.
A partir de ahora todas las funciones siguientes también estarán protegidas de ésta manera.
Solicitud GET:
Si la solicitud es un GET, se renderiza la página create_project.html con el formulario vacío para crear proyectos y la lista de proyectos existentes.
Solicitud POST:
Si la solicitud es un POST, se intenta procesar el formulario CreateProject que contiene los datos del nuevo proyecto.
Si el formulario es válido, se crea un nuevo proyecto, se establece el usuario actual (request.user) como propietario del proyecto y se guarda en la base de datos.
Luego, se obtiene el ID del nuevo proyecto y se redirige al usuario a la página específica del proyecto recién creado.
Si hay un error (por ejemplo, si los datos ingresados no son válidos), se renderiza nuevamente la página create_project.html con un mensaje de error.
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
        try:
            form = CreateProject(request.POST)
            new_project = form.save(commit=False)
            new_project.user = request.user
            new_project.save()
            project_id = new_project.id
            redirect_url = f'/project/{project_id}'
            return redirect(redirect_url)
        except ValueError:
            return render(request, 'create_project.html', {
                'form': CreateProject,
                'error': 'Por favor ingrese informacion valida'
            })

"""
Función para crear las tareas.
Se obtienen todos los proyectos, usuarios, prioridades y condiciones disponibles desde la base de datos.
Solicitud GET:
Si la solicitud es un GET, se renderiza la página create_task.html con el formulario vacío para crear tareas y las listas de proyectos, usuarios, prioridades y condiciones disponibles.
Solicitud POST:
Si la solicitud es un POST, se intenta procesar el formulario CreateTask que contiene los datos de la nueva tarea.
Si el formulario es válido, se crea una nueva tarea con los datos proporcionados y se guarda en la base de datos. La tarea se asocia al proyecto seleccionado en el formulario.
Luego, se obtiene el ID del proyecto al que pertenece la tarea recién creada y se redirige al usuario a la página específica de ese proyecto.
Si hay un error (por ejemplo, si los datos ingresados no son válidos), se renderiza nuevamente la página create_task.html con un mensaje de error.
"""
@login_required
def create_task(request):
    
    projects = Project.objects.all()
    users = User.objects.all()
    priority = Priority.objects.all()
    condition = TaskCondition.objects.all()


    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': CreateTask,
            'users': users,
            'projects': projects,
            'prioritys': priority,
            'conditions': condition,
        })
    else:
        try:
            form = CreateTask(request.POST)
            new_task = form.save(commit=False)
            new_task.save()

            project_id = new_task.project.id
            redirect_url = f'/project/{project_id}/'
            return redirect(redirect_url)
        except ValueError:
            return render(request, 'create_task.html', {
                'form': CreateTask,
                'error': 'Por favor ingrese informacion valida'
            })

"""
Función para ver la vista detallada de cada proyecto.
Se obtienen todos los proyectos existentes y el proyecto específico con el project_id proporcionado desde la base de datos.
Se obtienen todas las tareas asociadas al proyecto identificado por project_id.
Si la solicitud es un GET, se renderiza la página main_section.html con la información del proyecto específico y las tareas asociadas.
La variable projects contiene la lista de todos los proyectos.
La variable project contiene los detalles del proyecto específico.
La variable tasks contiene la lista de tareas asociadas al proyecto específico.
"""
@login_required
def main_section(request, project_id):
    if request.method == 'GET':
        projects = Project.objects.all()
        project = get_object_or_404(Project, pk = project_id)
        tasks = Task.objects.filter(project_id = project_id)
        return render(request, "main_section.html", {
            'project': project,
            'projects': projects,
            'tasks': tasks,
        })

"""
Función modificar tareas.
Se obtienen todos los proyectos, usuarios, prioridades y condiciones disponibles desde la base de datos.
Solicitud GET:
Si la solicitud es un GET, se obtiene la tarea específica con el task_id proporcionado desde la base de datos usando get_object_or_404.
Se renderiza la página update_task.html con el formulario llenado con los detalles de la tarea existente y las listas de proyectos, usuarios, prioridades y condiciones disponibles.
Solicitud POST:
Si la solicitud es un POST, se intenta procesar el formulario CreateTask que contiene los datos actualizados de la tarea.
Si el formulario es válido, se actualiza la tarea con los nuevos datos y se guarda en la base de datos.
Luego, se obtiene el ID del proyecto al que pertenece la tarea y se redirige al usuario a la página específica de ese proyecto.
Si hay un error (por ejemplo, si los datos ingresados no son válidos), se renderiza nuevamente la página update_task.html con un mensaje de error.
"""
@login_required
def update_task(request, task_id):
    projects = Project.objects.all()
    users = User.objects.all()
    priority = Priority.objects.all()
    condition = TaskCondition.objects.all()
    if request.method == 'GET':
        task = get_object_or_404(Task, pk = task_id)
        projects = Project.objects.all()
        form = CreateTask(instance = task)
        return render(request, 'update_task.html', {
                'form': CreateTask,
                'projects': projects,
                'task': task,
                'users': users,
                'prioritys': priority,
                'conditions': condition,
            })
    else:
        try:
            task = get_object_or_404(Task, pk = task_id)
            form = CreateTask(request.POST, instance = task)
            form.save()
            project_id = task.project.id
            # Construir la URL de redirección
            redirect_url = f'/project/{project_id}/'
            # Redirigir a la URL del proyecto
            return redirect(redirect_url) 
        except ValueError:
            return render(request, 'update_task.html', {
                'task': task, 
                'form': form, 
                'error': "Error actualizando la tarea" 
            })


"""
Función para marcar tareas como completadas.
Se obtiene la tarea específica con el task_id proporcionado desde la base de datos utilizando get_object_or_404.
Si la solicitud es un GET, se marca la tarea como completada al actualizar su propiedad datecompleted con la fecha y hora actual (timezone.now()), establecer completed en True y cambiar la condición de la tarea a la condición correspondiente al estado completado (TaskCondition(4)).
Luego, se guarda la tarea actualizada en la base de datos.
Finalmente, se obtiene el ID del proyecto al que pertenece la tarea y se redirige al usuario a la página específica de ese proyecto, indicando que la tarea se ha completado.
"""
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    if request.method == 'GET':
        task.datecompleted = timezone.now()
        task.completed = True
        task.condition = TaskCondition(4)
        task.save()
        project_id = task.project.id
        redirect_url = f'/project/{project_id}/'
        return redirect(redirect_url)    


"""
Función para eliminar tareas.
Se obtiene la tarea específica con el task_id proporcionado desde la base de datos utilizando get_object_or_404.
Si la solicitud es un GET, se elimina la tarea de la base de datos utilizando el método delete() de Django.
Luego, se obtiene el ID del proyecto al que pertenecía la tarea y se redirige al usuario a la página específica de ese proyecto, indicando que la tarea ha sido eliminada.
"""
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    if request.method == 'GET':
        task.delete()
        project_id = task.project.id
        redirect_url = f'/project/{project_id}/'
        return redirect(redirect_url) 
    
"""
Función para eliminar proyectos y todas sus tareas.
Se obtiene el proyecto específico con el project_id proporcionado desde la base de datos utilizando get_object_or_404.
Si la solicitud es un GET, se elimina el proyecto de la base de datos utilizando el método delete() de Django.
Luego, se redirige al usuario a la página de inicio ('home'), indicando que el proyecto ha sido eliminado.
"""
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk = project_id)
    if request.method == 'GET':
        project.delete()
        return redirect('home')

"""
Función modificar perfil de usuario.
Se obtiene el usuario actual (request.user) y todos los proyectos existentes desde la base de datos.
Solicitud GET:
Si la solicitud es un GET, se crea un formulario UserChangeForm con el usuario actual como instancia y se renderiza la página user_profile.html.
El formulario se muestra prellenado con la información actual del usuario.
Solicitud POST:
Si la solicitud es un POST, se intenta procesar el formulario UserChangeForm que contiene los datos actualizados del usuario.
Si el formulario es válido, se guardan los cambios en el usuario y se redirige al usuario a la página de inicio ('home').
Si hay errores en el formulario, se renderiza nuevamente la página user_profile.html con un mensaje de error y el formulario prellenado con los datos ingresados.
"""
@login_required
def user_profile(request):
    user = request.user
    projects = Project.objects.all()

    if request.method == 'GET':
        form = UserChangeForm(instance=user)
        return render(request, 'user_profile.html', {
            'form': form,
            'user': user,
            'projects': projects,
        })
    elif request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, 'user_profile.html', {
                'form': form,
                'user': user,
                'projects': projects,
            })



# def user_profile(request):
#     user = request.user
#     projects = Project.objects.all()
#     if request.method == 'GET':
#         form = UserChangeForm(instance = user)
#         print(form)
#         return render(request, 'user_profile.html', {
#             'form': form,
#             'user': user,
#             'projects': projects,
#         })
#     elif request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             return render(request, 'user_profile.html', {
#                 'form': form,
#                 'user': user,
#                 'projects': projects,
#             })


# def user_profile(request):
#     user = request.user
#     projects = Project.objects.all()

#     if request.method == 'GET':
#         form = CustomUserChangeForm(instance=user)
#         return render(request, 'user_profile.html', {
#             'form': form,
#             'user': user,
#             'projects': projects,
#         })
#     elif request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect("home")
#         else:
#             return render(request, 'user_profile.html', {
#                 'form': form,
#                 'user': user,
#                 'projects': projects,
#             })