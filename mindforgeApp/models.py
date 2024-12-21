from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to='media/fotosParticipantes/', null=True, blank=True, default='fotosParticipantes/default.png')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Clase(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)  # Campo adicional opcional para identificar clases

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Alumno(models.Model):
    idAlumno = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cursos = models.ManyToManyField(Clase, related_name="estudiantes")

    def __str__(self):
        return f"{self.idAlumno.first_name} {self.idAlumno.last_name}"


class Profesor(models.Model):
    idProfe = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cursos = models.ManyToManyField(Clase, related_name="profesores")

    def __str__(self):
        return f"{self.idProfe.first_name} {self.idProfe.last_name}"


class Contenido(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    archivo = models.FileField(upload_to='media/contenidos/', null=True, blank=True)

    def __str__(self):
        return self.titulo


class Tarea(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()

    def __str__(self):
        return self.titulo


class Entrega(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='media/entregas/')
    fecha_entrega = models.DateField(auto_now_add=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Entrega de {self.alumno} para {self.tarea}"

    