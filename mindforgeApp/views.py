from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.views.decorators.csrf import csrf_protect




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(f"Usuario autenticado: {user}")  # Agrega este print
            if user is not None:
                login(request, user)
                return redirect('home_view')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})  

def logout_view(request):
    logout(request)
    return redirect('login_view')  # Redirige a la página de login después del logout

@login_required
def home_view(request):
    usuario = Usuario.objects.get(id = request.user.id)
    cursos = None
    es_profesor = Profesor.objects.filter(idProfe=request.user.id).exists()

    if Alumno.objects.filter(idAlumno = usuario.id).exists():
        user = Alumno.objects.get(idAlumno = request.user.id)
        #cursos = user.cursos.all()
        cursos = user.cursos.prefetch_related('profesores')
    elif(Profesor.objects.filter(idProfe = usuario.id).exists()): 
        user = Profesor.objects.get(idProfe = request.user.id)
        #cursos = user.cursos.all()
        cursos = user.cursos.prefetch_related('profesores')
   
    context = {
        'usuario' : usuario, 
        'cursos' : cursos,
        'es_profesor' : es_profesor,
    }
    return render(request, 'index.html', context) 

@csrf_protect
def registroAlumno_view(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            user = form.save()
            Alumno.objects.create(idAlumno = user)
            login(request, user)
             # Redirigir a la página principal
            return redirect('home_view')
        else:
            print(form.errors)
    return render(request, 'registro.html')

@csrf_protect
def registroProfe_view(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profesor.objects.create(idProfe = user)
            login(request, user)
             # Redirigir a la página principal
            return redirect('home_view')
        else:
            print(form.errors)
    return render(request, 'registro.html')
    

@login_required
def clase_view(request, clase_id):
    #Obtener la clase específica
    #clase = get_object_or_404(Clase, id=request.clase.codigo)
    clase = get_object_or_404(Clase, id=clase_id)
    #Obtener los contenidos de la clase
    Contenidos = Contenido.objects.filter(clase=clase)
    tareas = Tarea.objects.filter(clase=clase)
    es_profesor = Profesor.objects.filter(idProfe=request.user.id).exists()
    return render(request, 'clase.html', {'clase': clase, 'Contenidos': Contenidos, 'tareas': tareas, 'es_profesor': es_profesor})

@login_required
def anyadir_alumno_view(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)  # Asegúrate de obtener la clase
    if not Profesor.objects.filter(idProfe=request.user.id).exists():
        return redirect('clase_view', clase_id=clase.id)
   
    if request.method == 'POST':
        form = anyadirAlumnoForm(request.POST)
        if form.is_valid():
            try:
                form.save(clase)
                return redirect('clase_view', clase_id=clase.id)
            except forms.ValidationError as e:
                form.add_error('username', e.message)
    else:
        form = anyadirAlumnoForm()
    return render(request, 'clase.html', {'form': form, 'clase': clase})


@login_required
def participantes_view(request, clase_id):
    # Obtener la clase correspondiente
    clase = get_object_or_404(Clase, id=clase_id)

    # Obtener todos los alumnos y profesores de la clase
    alumnos = Alumno.objects.filter(cursos=clase)
    profesores = Profesor.objects.filter(cursos=clase)

    context = {
        'clase': clase,
        'alumnos': alumnos,
        'profesores': profesores,
    }

    return render(request, 'participantes.html', context)

@login_required
def tarea_view(request):
    return render(request, 'tarea.html')

@login_required
def perfil_view(request, id):
    usuario = Usuario.objects.get(id=id)
    return render(request, 'perfil.html', {'usuario' : usuario})

@login_required
def crear_clase_view(request):
    if request.method == 'POST':
        form = ClaseForm(request.POST)
        if form.is_valid():
            clase = form.save(commit=True)
            profesor = get_object_or_404(Profesor, idProfe_id=request.user.id)
            profesor.cursos.add(clase)
            clase.save()
            messages.success(request, 'Clase creada con éxito')  
            return redirect('clase_view', clase_id = clase.id)  # Redirige al índice o a otra página
        else:
            print(form.errors)
    else:
        form = ClaseForm()
    return render(request, 'crear_clase.html', {'form': form})

@login_required
def contenidos_view(request, clase_id):
    # Obtener la clase específica
    clase = get_object_or_404(Clase, id=clase_id)
    # Obtener todos los contenidos relacionados con la clase
    contenidos = Contenido.objects.filter(clase=clase)
    es_profesor = Profesor.objects.filter(idProfe=request.user.id).exists()

    context = {
        'clase': clase,
        'contenidos': contenidos,
        'es_profesor': es_profesor
    }
    return render(request, 'contenidos.html', context)

def anyadir_contenido_view(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    if request.method == 'POST':
        form = ContenidoForm(request.POST, request.FILES)
        if form.is_valid():
            contenido = form.save(commit=False)
            contenido.clase = clase
            contenido.save()
            return redirect('contenidos_view', clase_id=clase.id)
    else:
        print("formulario error")
        form = ContenidoForm()
    return render(request, 'clase.html', {'form': form, 'clase': clase})

@login_required
def tareas_view(request, clase_id):
    # Obtener la clase correspondiente
    clase = get_object_or_404(Clase, id=clase_id)
    es_profesor = Profesor.objects.filter(idProfe=request.user.id).exists()
    es_alumno = Alumno.objects.filter(idAlumno=request.user.id).exists()
    
    # Obtener todas las tareas de esa clase
    tareas = Tarea.objects.filter(clase=clase)
    
    context = {
        'clase': clase,
        'tareas': tareas,
        'es_profesor': es_profesor,
        'es_alumno': es_alumno,
    }
    
    return render(request, 'tarea.html', context)

def anyadir_tarea_view(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    alumnos = Alumno.objects.filter(cursos=clase)  # Obtener alumnos de la clase
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.clase = clase
            tarea.save()
            for alumno in alumnos:
                Entrega.objects.create(
                    tarea=tarea,
                    alumno=alumno,
                    archivo=None,  # Archivo vacío al inicio
                )
            messages.success(request, "Tarea y entregas asociadas creadas con éxito.")
            return redirect('tareas_view', clase_id=clase.id)
    else:
        form = TareaForm()
    return render(request, 'clase.html', {'form': form, 'clase': clase})

def entregas_view(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    entregas = Entrega.objects.filter(tarea=tarea)
    return render(request, 'entregas.html', {'tarea': tarea, 'entregas': entregas})

@login_required
def entrega_view(request, tarea_id, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    tarea = get_object_or_404(Tarea, id=tarea_id)
    alumno = get_object_or_404(Alumno, idAlumno=request.user.id)

    if request.method == 'POST':
        form = EntregaForm(request.POST, request.FILES)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.tarea = tarea
            entrega.alumno = alumno
            entrega.save()
            return redirect('tarea_view', tarea_id=tarea.id)  # Ajusta según corresponda
    else:
        form = EntregaForm()

    return render(request, 'entregas.html', {'form': form, 'tarea': tarea, 'clase': clase})


@login_required
def anyadir_entrega_view(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    # Verificar si el usuario actual es un alumno
    try:
        alumno = Alumno.objects.get(idAlumno=request.user.id)
    except Alumno.DoesNotExist:
        messages.error(request, "Solo los alumnos pueden subir entregas.")
        return redirect('home_view')

    if request.method == 'POST':
        form = EntregaForm(request.POST, request.FILES)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.tarea = tarea
            entrega.alumno = alumno
            entrega.save()
            messages.success(request, "Entrega subida exitosamente.")
            return redirect('tarea_view', tarea_id=tarea.id)
        else:
            messages.error(request, "Por favor, corrige los errores del formulario.")
    else:
        form = EntregaForm()

    return render(request, 'clase.html', {'form': form, 'tarea': tarea})

@login_required
def subir_entrega_view(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    alumno = get_object_or_404(Alumno, idAlumno=request.user.id)

    if request.method == 'POST':
        archivo = request.FILES.get('archivo')

        if archivo:
            entrega, created = Entrega.objects.get_or_create(tarea=tarea, alumno=alumno)
            entrega.archivo = archivo
            entrega.save()
            messages.success(request, "Entrega subida correctamente.")
        else:
            messages.error(request, "Por favor, selecciona un archivo.")
    return redirect('tareas_view', clase_id=tarea.clase.id)

@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        usuario = request.user

        # Actualizar solo los campos que se hayan enviado
        usuario.first_name = request.POST.get('first-name', usuario.first_name)
        usuario.last_name = request.POST.get('last-name', usuario.last_name)
        usuario.email = request.POST.get('email', usuario.email)

        # Manejar la foto de perfil si se envía una nueva
        if 'foto' in request.FILES:
            usuario.foto = request.FILES['foto']

        # Manejar la contraseña (si se proporciona)
        nueva_password = request.POST.get('password')
        if nueva_password:
            usuario.set_password(nueva_password)

        usuario.save()

        # Redirigir al perfil del usuario con su ID
        return redirect('perfil_view', id=usuario.id) 

    return render(request, 'perfil.html', {'usuario': request.user})