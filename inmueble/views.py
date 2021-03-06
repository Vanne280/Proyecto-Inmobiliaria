from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import (Inmueble, Barrio, Tipo_de_inmueble,
                     Tipo_de_oferta, Imagenes, Propietarios_arrendatarios, cita)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import InmuebleForm, ContactoForm
from django.contrib import messages

# Librería para paginación
from django.core.paginator import Paginator

# Librería para enviar correos
from django.core.mail import EmailMessage

# Librería Decoradores (permisos)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

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

# librería para filtrar en varios registros
from django.db.models import Q

# Función que llama la página de inicio
def home(request):
    return render(request, "inicio.html")

def Busqueda(request):
    queryset = request.GET.get("buscar")
    b = Inmueble.objects.filter(disponible=True)
    if queryset:
        b = Inmueble.objects.filter(
            Q(IDBarrio__nombre__icontains = queryset) |
            Q(IDTipo_de_inmueble__nombre__icontains = queryset) |
            Q(IDTipo_de_oferta__nombre__icontains = queryset)
        )
    # if request.method == 'POST':
    #     barrio = request.POST['barrio']
    #     tipo_inmueble = request.POST['tipo_inmueble']
    #     tipo_oferta = request.POST['tipo_oferta']
    #
    #     b = Inmueble.objects.filter(disponible=True, IDBarrio__id = barrio)
    #
    return render(request, 'inmueble/inmueble_search.html', {'object_list':b, 'buscar':queryset})


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


# Función que guarda registros de inmuebles con sus respectivas imágenes
@login_required()
@permission_required('usuario.agregar_inmueble')
def Guardar_inmueble(request):
    template_name = 'inmueble/inmueble_form.html'
    form = InmuebleForm()

    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            is_file = request.POST.get('imagenppal', True)
            inmueble = form.save(commit = False)
            if is_file == True:
                 inmueble.imagenppal = request.FILES['imagenppal']
            inmueble.save()
            for field in request.FILES.keys():
                    for formfile in request.FILES.getlist(field):
                        img = Imagenes(ruta = formfile, IDInmueble_id = inmueble.pk)
                        img.save()
                        messages.success(request, 'Se guardó el inmueble correctamente')
            return HttpResponseRedirect(reverse('listar'))
        else:
            messages.warning(request, 'Por favor, ingrese los datos otra vez.')
            return render(request, template_name, {'form':form})
    else:
        form = InmuebleForm()

    return render(request, template_name, {'form':form})

# Función que edita registros de inmuebles
@permission_required('usuario.editar_inmueble')
@login_required()
def Editar_inmueble(request, pk):
    inmueble = Inmueble.objects.get(pk=pk)
    if request.method == 'GET':
        form = InmuebleForm(instance=inmueble)
    else:
        form = InmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            is_file = request.POST.get('imagenppal', True)
            inmueble = form.save(commit = False)
            if is_file == True:
                 inmueble.imagenppal = request.FILES['imagenppal']
            inmueble.save()
            for field in request.FILES.keys():
                    for formfile in request.FILES.getlist(field):
                        img = Imagenes(ruta = formfile, IDInmueble_id = inmueble.pk)
                        img.save()
                        # messages.success(request, 'Se guardó el inmueble correctamente')
        return redirect('listar')

    return render(request, 'inmueble/inmueble_form.html', {'form':form})

# Función que lista los inmuebles
@permission_required('usuario.listar_inmueble')
@login_required()
def Listar_inmueble(request):
    inmueble = Inmueble.objects.all()
    if request.POST.get('codigo'):
        codigo = (request.POST.get('codigo'))
        inmueble = Inmueble.objects.filter(codigo__icontains = codigo)
    elif request.POST.get('tipo_oferta'):
        tipo_oferta = (request.POST.get('tipo_oferta'))
        inmueble = Inmueble.objects.filter(IDTipo_de_oferta__nombre__icontains = tipo_oferta)
    elif request.POST.get('tipo_inmueble'):
        tipo_inmueble = (request.POST.get('tipo_inmueble'))
        inmueble = Inmueble.objects.filter(IDTipo_de_inmueble__nombre__icontains = tipo_inmueble)
    elif request.POST.get('barrio'):
        barrio = (request.POST.get('barrio'))
        inmueble = Inmueble.objects.filter(IDBarrio__nombre__icontains = barrio)

    paginator = Paginator(inmueble, 7)
    page = request.GET.get('page')
    inmueble = paginator.get_page(page)

    return render(request, 'inmueble/inmueble_list.html', {'inmueble':inmueble})

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
        return reverse('listar_gestion')

    # Muestra los registros guardados de las tablas (User, Inmuebles) en los campos de selección
    def get_context_data(self,**kwargs):
        context = super(GestionCreate,self).get_context_data(**kwargs)
        context['usuario'] = User.objects.all()
        context['inmueble'] = Inmueble.objects.all()
        return context

class GestionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Clase que lista los propietarios y sus inmuebles """

    permission_required = 'usuario.listar_propiedad_cliente'
    template_name = 'asesor/inmuebles.html'
    model = Propietarios_arrendatarios
    context_object_name = 'gestion'

class MisinmueblesList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Clase que lista los inmuebles registrados en el perfil de los clientes """

    permission_required = 'usuario.ver_inmuebles'
    template_name = 'cliente/mis_inmuebles.html'
    model = Propietarios_arrendatarios
    context_object_name = 'inmuebles'

class Citas_inmuebles(CreateView):
    """ Clase que crea un formulario para mandar un mensaje al asesor """

    model = cita
    template_name = 'citas_inmuebles/cita_form.html'
    fields = ['inmueble','usuario','telefono','email','asunto','mensaje']

    # Retorna a la página donde se listan los inmuebles
    def get_success_url(self):
        return reverse('cita')

class CitaList(LoginRequiredMixin, ListView):
    """ Clase que muestra los mensajes al asesor """

    template_name = 'asesor/mis_citas.html'
    model = cita
    context_object_name = 'cita'

class CitaDelete(LoginRequiredMixin, DeleteView):
    """ Clase que borra la cita """

    model = cita
    template_name = 'citas_inmuebles/cita_delete.html'
    context_object_name = 'cita'

    # Retorna a la página donde se muestran las citas
    def get_success_url(self):
        return reverse('mis_citas')
