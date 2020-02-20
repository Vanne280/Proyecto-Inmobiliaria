from django.shortcuts import render

# Create your views here.

# funciones que llaman las páginas
def home(request):
    return render(request, 'base/base.html')

def ventas(request):
    return render(request, "paginas/ventas.html")

def arrendamientos(request):
    return render(request, "paginas/arrendamientos.html")
