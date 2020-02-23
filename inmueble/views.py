from django.shortcuts import render
from .models import Inmueble

#ListView
from django.views.generic.list import ListView

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
