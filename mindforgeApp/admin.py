from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mindforgeApp.models import *

# Configuración del modelo Alumno en el panel de administración
class AlumnoAdmin(UserAdmin):
    model = Alumno
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nombre', 'apellidos', 'email', 'fecha_nacimiento', 'foto', 'cursos')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nombre', 'apellidos', 'email', 'fecha_nacimiento', 'foto', 'cursos')}),
    )

# Configuración del modelo Profesor en el panel de administración
class ProfesorAdmin(UserAdmin):
    model = Profesor
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nombre', 'apellidos', 'email', 'fecha_nacimiento', 'foto', 'cursos')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nombre', 'apellidos', 'email', 'fecha_nacimiento', 'foto', 'cursos')}),
    )

# Register your models here.
admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Clase)
admin.site.register(Contenido)
admin.site.register(Tarea)
admin.site.register(Entrega)

