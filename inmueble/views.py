from django.shortcuts import render
from .models import (Inmueble, Barrio, Tipo_de_inmueble,
                     Tipo_de_oferta, Imagenes)
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


def home(request):
    """Función que llama la página de inicio"""

    return render(request, "inicio.html")

def ventas(request):
    """Función que llama la página de ventas"""

    return render(request, "paginas/ventas.html")

def nosotros(request):
    """Función que llama la página de nosotros"""

    return render(request, "paginas/nosotros.html")

class InmuebleCreate(CreateView):
    """Clase que crea la vista para registrar los inmuebles"""

    model = Inmueble
    template_name = 'inmueble/inmueble_form.html'
    fields = ('direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
                'alcoba','baño','parqueadero','disponible','imagen')

    def get_success_url(self):
        """Retorna a la página donde se listan los inmuebles"""

        return reverse('listar')

    def get_context_data(self,**kwargs):
        """Muestra los registros guardados de las tablas (Barrio, Tipo_de_oferta,
        Tipo_de_inmueble) en los campos de selección"""

        context = super(InmuebleCreate,self).get_context_data(**kwargs)
        context['IDBarrio'] = Barrio.objects.all()
        context['IDTipo_de_inmueble'] = Tipo_de_inmueble.objects.all()
        context['IDTipo_de_oferta'] = Tipo_de_oferta.objects.all()
        return context

@login_required()
def Guardar_inmueble(request):
    """Función que guarda registros de inmuebles con sus respectivas imágenes"""

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
                'alcoba','baño','parqueadero','disponible','imagen']

    def get_success_url(self):
        """Retorna a la página donde se listan los inmuebles"""

        return reverse('listar')

class InmuebleDelete(DeleteView):
    """Clase que elimina los inmuebles"""

    model = Inmueble

    def get_success_url(self):
        """Retorna a la página donde se listan los inmuebles"""

        return reverse('listar')

#Oferta de inmuebles
class ImageList(ListView):
    """Clase que muestra las imágenes"""

    template_name = 'paginas/arrendamientos.html'
    model = Inmueble
    context_object_name = 'inmuebles'

class InmuebleDetail(DetailView):
    """Clase que muestra los datos de la tabla Inmueble"""

    model = Inmueble
    template_name = 'inmueble/inmueble_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['imagenes'] = Imagenes.objects.filter(IDInmueble_id = self.get_object().id)
        return super(InmuebleDetail, self).get_context_data(**kwargs)
