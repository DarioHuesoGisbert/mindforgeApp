# mindforgeApp/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login_view'), 
    path('logout/', views.logout_view, name='logout'),  # Ruta para la página principal (login)
    path('', views.home_view, name='home_view'), # Ruta para la vista principal
    path('registroAlumno/', views.registroAlumno_view, name='registroAlumno_view'),  # Ruta para la vista de registro
    path('registroProfe/', views.registroProfe_view, name='registroProfe_view'),  # Ruta para la vista de registro
    path('clase/<int:clase_id>/', views.clase_view, name='clase_view'),  # Ruta para las clases
    path('participantes/<int:clase_id>/', views.participantes_view, name='participantes_view'),# Ruta para la vista de participantes
    path('tarea/', views.tarea_view, name='tarea_view'),  # Ruta para la vista de tarea
    path('perfil/<int:id>/', views.perfil_view, name='perfil_view'),  # Ruta para la vista del perfil
    path('crear_clase/', views.crear_clase_view, name='crear_clase_view'),  # Ruta para la vista de creación de clase
    path('anyadir-alumno/<int:clase_id>/', views.anyadir_alumno_view, name='anyadir_alumno_view'),
    path('clase/<int:clase_id>/contenidos/', views.contenidos_view, name='contenidos_view'),
    path('clase/<int:clase_id>/contenido/nuevo/', views.anyadir_contenido_view, name='anyadir_contenido_view'),
    path('tarea/<int:tarea_id>/entregar/', views.anyadir_entrega_view, name='anyadir_entrega_view'),
    path('clase/<int:clase_id>/tareas/nueva/', views.anyadir_tarea_view, name='anyadir_tarea_view'),
    path('clase/<int:clase_id>/tareas/', views.tareas_view, name='tareas_view'),
    path('clase/<int:clase_id>/tarea/<int:tarea_id>/entregar/', views.entrega_view, name='entrega_view'),
    path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
    path('tarea/<int:tarea_id>/entregas/', views.entregas_view, name='entregas_view'),
    path('tarea/<int:tarea_id>/subir/', views.subir_entrega_view, name='subir_entrega_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
