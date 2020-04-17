from django.shortcuts import render
from django.contrib.auth.models import User
from .models import (Inmueble, Barrio, Tipo_de_inmueble,
                     Tipo_de_oferta, Imagenes, Propietarios_arrendatarios, Cita)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import InmuebleForm, ContactoForm

# Librería para enviar correos
from django.core.mail import EmailMessage

# Librería Decoradores (permisos)
from django.contrib.auth.decorators import login_required

# Librerías permisos requeridos para vistas basadas en clases
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Librería que permite cargar una plantilla html como variable
from django.template.loader import render_to_string

# Librería TemplateView
from django.views.generic import TemplateView

# Librería ListView
from django.views.generic.list import ListView

# Librerías CreateView, UpdateView, DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Librería DetailView
from django.views.generic.detail import DetailView

# Función que llama la página de inicio
def home(request):
    return render(request, "inicio.html")

# Función que llama la página de nosotros
def nosotros(request):
    return render(request, "paginas/nosotros.html")


class ContactoView(TemplateView):
    """ Clase que llama la página de contacto y envía un correo
        con información de un cliente """

    template_name = 'paginas/contacto.html'

    # Función que llama al formulario de contacto
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['contacto_form'] = ContactoForm()

        return context

    # Función que envía un correo con la información recibida del formulario de contacto
    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        body = render_to_string('email/email_contacto.html', {
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'email': email,
            'mensaje': mensaje,
        })

        msg = EmailMessage(
            subject = asunto,
            body = body,
            from_email = email,
            to = ['asesorinmobiliariainnova@gmail.com'],
        )
        msg.content_subtype = 'html'
        msg.send()

        return HttpResponseRedirect(reverse('contacto'))

class ContactoList(LoginRequiredMixin, ListView):
    """docstring for ContactoList."""

    template_name = 'asesor/mis_citas.html'
    model = ContactoForm
    context_object_name = 'contacto'


class InmuebleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Clase que crea la vista para registrar los inmuebles """

    permission_required = 'usuario.agregar_inmueble'
    model = Inmueble
    template_name = 'inmueble/inmueble_form.html'
    fields = ['direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
                'alcoba','baño','parqueadero','disponible','descripcion','imagen']

    # Retorna a la página donde se listan los inmuebles
    def get_success_url(self):
        return reverse('listar')

    # Muestra los registros guardados de las tablas (Barrio, Tipo_de_oferta,
    # Tipo_de_inmueble) en los campos de selección
    def get_context_data(self,**kwargs):
        context = super(InmuebleCreate,self).get_context_data(**kwargs)
        context['IDBarrio'] = Barrio.objects.all()
        context['IDTipo_de_inmueble'] = Tipo_de_inmueble.objects.all()
        context['IDTipo_de_oferta'] = Tipo_de_oferta.objects.all()
        return context

@login_required()
# Función que guarda registros de inmuebles con sus respectivas imágenes
def Guardar_inmueble(request):
    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        IDBarrio = request.POST.get('IDBarrio')
        IDTipo_de_inmueble = request.POST.get('IDTipo_de_inmueble')
        IDTipo_de_oferta = request.POST.get('IDTipo_de_oferta')
        precio = request.POST.get('precio')
        alcoba = request.POST.get('alcoba')
        baño = request.POST.get('baño')
        parqueadero = request.POST.get('parqueadero')
        disponible = request.POST.get('disponible')
        descripcion = request.POST.get('descripcion')
        imagen = request.POST.get('imagen', True)
        is_file = request.POST.get('imagenes', True)

        print(direccion)
        print(IDBarrio)
        print(IDTipo_de_inmueble)
        print(IDTipo_de_oferta)
        print(precio)
        print(alcoba)
        print(baño)
        print(parqueadero)
        print(disponible)
        print(descripcion)
        print(imagen)
        print(is_file)

        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save()
            for field in request.FILES.keys():
                if is_file == True:
                    for formfile in request.FILES.getlist(field):
                        img = Imagenes(ruta = formfile, IDInmueble_id = inmueble.pk)
                        img.save()

        return HttpResponseRedirect(reverse('listar'))

class InmuebleView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Clase que lista los registros de los inmuebles """

    permission_required = 'usuario.listar_inmueble'
    model = Inmueble
    context_object_name = 'inmueble'

class InmuebleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Clase que edita los inmuebles """

    permission_required = 'usuario.eliminar_inmueble'
    model = Inmueble
    fields = ['direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
                'alcoba','baño','parqueadero','disponible','descripcion','imagen']

    # Retorna a la página donde se listan los inmuebles
    def get_success_url(self):
        return reverse('listar')

class InmuebleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Clase que elimina los inmuebles """

    permission_required = 'usuario.editar_inmueble'
    model = Inmueble
    context_object_name = 'inmueble'

    # Retorna a la página donde se listan los inmuebles
    def get_success_url(self):
        return reverse('listar')


class AlquilerList(ListView):
    """ Clase que muestra las ofertas de inmuebles en arrendamiento """

    template_name = 'paginas/arrendamientos.html'
    model = Inmueble
    context_object_name = 'inmuebles'

class VentaList(ListView):
    """ Clase que muestra las ofertas de inmuebles en venta """

    template_name = 'paginas/ventas.html'
    model = Inmueble
    context_object_name = 'inmuebles'

class InmuebleDetail(DetailView):
    """ Clase que muestra los datos de la tabla Inmueble """

    model = Inmueble
    template_name = 'inmueble/inmueble_detail.html'

    # Muestra las imágenes del respectivo inmueble de la tabla Imagenes
    def get_context_data(self, **kwargs):
        kwargs['imagenes'] = Imagenes.objects.filter(IDInmueble_id = self.get_object().id)
        return super(InmuebleDetail, self).get_context_data(**kwargs)

class GestionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Clase que registra los datos de la tabla Propietarios_arrendatarios """

    permission_required = 'usuario.gestionar_inmueble_propietario'
    model = Propietarios_arrendatarios
    template_name = 'asesor/gestion_inmueble.html'
    fields = ['usuario','inmueble','tipo_cliente']

    # Retorna a la página donde se listan los inmuebles y sus propietarios
    def get_success_url(self):
        return reverse('listado')

    # Muestra los registros guardados de las tablas (User, Inmuebles) en los campos de selección
    def get_context_data(self,**kwargs):
        context = super(GestionCreate,self).get_context_data(**kwargs)
        context['usuario'] = User.objects.all()
        context['inmueble'] = Inmueble.objects.all()
        return context

class GestionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Clase que lista los inmuebles y sus propietarios """

    permission_required = 'usuario.listar_propiedad_cliente'
    template_name = 'asesor/inmuebles.html'
    model = Propietarios_arrendatarios
    context_object_name = 'gestion'

class MisinmueblesList(LoginRequiredMixin, ListView):
    """docstring for MisinmueblesList."""

    template_name = 'cliente/mis_inmuebles.html'
    model = Propietarios_arrendatarios
    context_object_name = 'inmuebles'
