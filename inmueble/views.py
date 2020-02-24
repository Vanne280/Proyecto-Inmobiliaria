from django.shortcuts import render
from .models import Inmueble

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

class InmuebleCreate(CreateView):
    model = Inmueble
    fields = '__all__'

    def get_success_url(self):
        return reverse('')
        
