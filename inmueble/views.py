from django.shortcuts import render
from .models import Inmueble, Barrio, Tipo_de_inmueble, Tipo_de_oferta, Imagenes
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import InmuebleForm

#Decoradores
from django.contrib.auth.decorators import login_required

#ListView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Funciones que llaman las páginas
def home(request):
    return render(request, "inicio.html")

def ventas(request):
    return render(request, "paginas/ventas.html")

def arrendamientos(request):
    return render(request, "paginas/arrendamientos.html")

# Clase que registra los inmuebles
class InmuebleCreate(CreateView):
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

# Clase que lista los registros de los inmuebles
class InmuebleView(ListView):
    model = Inmueble
    context_object_name = 'inmueble'

# Clase que edita los inmuebles
class InmuebleUpdate(UpdateView):
    """docstring for InmuebleUpdate."""

    model = Inmueble
    fields = ['direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
                'alcoba','baño','parqueadero','disponible']

    def get_success_url(self):
        return reverse('listar')

# Clase que edita los inmuebles
class InmuebleDelete(DeleteView):
    """docstring for InmuebleDelete."""

    model = Inmueble

    def get_success_url(self):
        return reverse('listar')

# Clase que lista las imágenes
class ImageList(ListView):
    """docstring for ImageList."""

    template_name = 'inmueble/inmueble_list.html'
    model = Imagenes
