from django.shortcuts import render
from .models import Inmueble, Barrio, Tipo_de_inmueble, Tipo_de_oferta
from django.urls import reverse_lazy, reverse

#ListView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

# Create your views here.

# funciones que llaman las páginas
def home(request):
    return render(request, "inicio.html")

def ventas(request):
    return render(request, "paginas/ventas.html")

def arrendamientos(request):
    return render(request, "paginas/arrendamientos.html")

# Clase que lista los registros de los inmuebles
class InmuebleView(ListView):
    model = Inmueble
    context_object_name = 'inmueble'

# Clase que registra los inmuebles
class InmuebleCreate(CreateView):
    model = Inmueble
    template_name = 'inmueble/inmueble_form.html'
    fields = (['direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
                'alcoba','baño','parqueadero','disponible'])

    def get_success_url(self):
        return reverse('listar')

    def get_context_data(self,**kwargs):
        context = super(InmuebleCreate,self).get_context_data(**kwargs)
        context['IDBarrio'] = Barrio.objects.all()
        context['IDTipo_de_inmueble'] = Tipo_de_inmueble.objects.all()
        context['IDTipo_de_oferta'] = Tipo_de_oferta.objects.all()
        return context
