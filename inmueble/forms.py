from django import forms
from .models import Inmueble

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ('direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
                  'alcoba','baño','parqueadero','disponible','descripcion')
        exclude = ['usuario',]

        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'validate', 'required': True}),
            'precio':forms.NumberInput(attrs={'class': 'validate', 'required': True}),
            'alcoba':forms.NumberInput(attrs={'class': 'validate', 'required': True}),
            'baño':forms.NumberInput(attrs={'class': 'validate', 'required': True}),
            'parqueadero':forms.CheckboxInput(attrs={'class': 'filled-in'}),
            'disponible':forms.CheckboxInput(attrs={'class': 'filled-in'}),
            'descripcion':forms.Textarea(attrs={'class': 'materialize-textarea'})
        }


class ContactoForm(forms.Form):
    """Clase del formulario Contacto"""

    nombre = forms.CharField(label='Nombre',)
    apellido = forms.CharField(label='Apellido',)
    telefono = forms.IntegerField(label='Teléfono',)
    email = forms.EmailField(label='Correo Electrónico',)
    asunto = forms.CharField(label='Asunto',)
    mensaje = forms.CharField(label='Mensaje', widget=forms.Textarea,)
