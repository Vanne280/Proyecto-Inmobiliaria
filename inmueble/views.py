from django.shortcuts import render
from .models import Inmueble, Barrio, Tipo_de_inmueble, Tipo_de_oferta, Imagenes
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import InmuebleForm

# Librería Decoradores (permisos)
from django.contrib.auth.decorators import login_required

# Librería ListView
from django.views.generic.list import ListView

# Librerías CreateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Librería DetailView
from django.views.generic.detail import DetailView

# Funciones que llaman las páginas
def home(request):
    return render(request, "inicio.html")

def ventas(request):
    return render(request, "paginas/ventas.html")

def nosotros(request):
    return render(request, "paginas/nosotros.html")

class InmuebleCreate(CreateView):
    """Clase que registra los inmuebles"""

    model = Inmueble
    template_name = 'inmueble/inmueble_form.html'
    fields = ('direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
                'alcoba','baño','parqueadero','disponible')

    def get_success_url(self):
        return reverse('listar')

    def get_context_data(self,**kwargs):
        context = super(InmuebleCreate,self).get_context_data(**kwargs)
        context['IDBarrio'] = Barrio.objects.all()
        context['IDTipo_de_inmueble'] = Tipo_de_inmueble.objects.all()
        context['IDTipo_de_oferta'] = Tipo_de_oferta.objects.all()
        return context

# Guardar inmueble
@login_required()
def Guardar_inmueble(request):
    if request.method == 'POST':
        is_file = request.POST.get('imagenes', True)
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save()
            for field in request.FILES.keys():
                if is_file == True:
                    for formfile in request.FILES.getlist(field):
                        img = Imagenes(ruta = formfile, IDInmueble_id = inmueble.pk)
                        img.save()

        return HttpResponseRedirect(reverse('listar'))

class InmuebleView(ListView):
    """Clase que lista los registros de los inmuebles"""

    model = Inmueble
    context_object_name = 'inmueble'

class InmuebleUpdate(UpdateView):
    """Clase que edita los inmuebles"""

    model = Inmueble
    fields = ['direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
                'alcoba','baño','parqueadero','disponible']

    def get_success_url(self):
        return reverse('listar')

class InmuebleDelete(DeleteView):
    """Clase que edita los inmuebles"""

    model = Inmueble

    def get_success_url(self):
        return reverse('listar')

class ImageList(ListView):
    """Clase que muestra las imágenes"""

    template_name = 'paginas/arrendamientos.html'
    model = Imagenes
    context_object_name = 'imagenes'

class InmuebleDetail(DetailView):
    """Clase que muestra los datos de la tabla Inmueble"""

    model = Inmueble
    template_name = 'inmueble/inmueble_detail.html'
