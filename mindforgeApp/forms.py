from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'})
        )
                                                 
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
        )

    
    
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre', 'codigo']

    def save(self, commit=True):
        clase = super(ClaseForm, self).save(commit=False)
        if commit:
            clase.save()
        return clase
    
class anyadirAlumnoForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nombre de Usuario")

    def save(self, clase):
        username = self.cleaned_data['username']

        # Busca el usuario por su nombre de usuario
        try:
            usuario = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            raise forms.ValidationError(f"No se encontró un usuario con el nombre de usuario '{username}'.")

        # Verifica si el usuario ya es alumno
        alumno, created = Alumno.objects.get_or_create(idAlumno=usuario)

        # Asocia el alumno con la clase
        alumno.cursos.add(clase)
        alumno.save()

        return alumno
    
class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'descripcion', 'archivo']

    def save(self, commit=True):
        contenido = super(ContenidoForm, self).save(commit=False)
        if commit:
            contenido.save()
        return contenido
    

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_entrega']

    def save(self, commit=True, clase=None):
        tarea = super(TareaForm, self).save(commit=False)
        if clase:
            tarea.clase = clase
        if commit:
            tarea.save()
        return tarea
    

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['archivo', 'comentarios']  # Los campos que el alumno debe completar
        widgets = {
            'comentarios': forms.Textarea(attrs={'placeholder': 'Añade algún comentario (opcional)', 'rows': 4}),
        }

    def save(self, commit=True, tarea=None, alumno=None):
        """Permite asociar la tarea y el alumno a la entrega antes de guardarla."""
        entrega = super().save(commit=False)
        if tarea:
            entrega.tarea = tarea
        if alumno:
            entrega.alumno = alumno
        if commit:
            entrega.save()
        return entrega
