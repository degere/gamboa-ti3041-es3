from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto, ConsultaCliente


class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

        self.fields['username'].widget.attrs.update({'placeholder': 'Ej: juanperez'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mínimo 4 caracteres'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repite la contraseña'})


class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos desde el sitio."""

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'stock', 'imagen']
        labels = {
            'nombre': 'Nombre del producto',
            'categoria': 'Categoría',
            'precio': 'Precio (CLP)',
            'stock': 'Stock disponible',
            'imagen': 'Archivo de imagen',
        }
        help_texts = {
            'imagen': 'Nombre del archivo dentro de static/Ferreteria/img/ (ej: 1.jpg). Opcional.',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return precio


class ConsultaClienteForm(forms.ModelForm):
    """Formulario de contacto: valida y guarda una ConsultaCliente."""

    class Meta:
        model = ConsultaCliente
        fields = ['nombre', 'correo', 'mensaje', 'producto']
        labels = {
            'nombre': 'Nombre',
            'correo': 'Correo electrónico',
            'mensaje': 'Mensaje',
            'producto': 'Producto de interés (opcional)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Juan Pérez'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'tucorreo@ejemplo.cl'}),
            'mensaje': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Cuéntanos qué necesitas (mínimo 10 caracteres)'}),
        }
        error_messages = {
            'nombre': {'required': 'Ingresa tu nombre.'},
            'correo': {
                'required': 'Ingresa tu correo electrónico.',
                'invalid': 'Ingresa un correo válido, por ejemplo nombre@dominio.cl.',
            },
            'mensaje': {'required': 'Escribe tu mensaje.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.order_by('nombre')
        self.fields['producto'].empty_label = 'Ninguno en particular'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return nombre

    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje'].strip()
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
        return mensaje

