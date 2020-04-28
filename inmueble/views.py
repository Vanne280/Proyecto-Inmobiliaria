from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import (Inmueble, Barrio, Tipo_de_inmueble,
                     Tipo_de_oferta, Imagenes, Propietarios_arrendatarios, cita)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import InmuebleForm, ContactoForm, CitaForm
from django.contrib import messages

# Librería para enviar correos
from django.core.mail import EmailMessage

# Librería Decoradores (permisos)
from django.contrib.auth.decorators import login_required

# Librerías permisos requeridos para vistas basadas en clases
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

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
    barrios = Barrio.objects.all()
    tipo_inmueble = Tipo_de_inmueble.objects.all()
    tipo_oferta = Tipo_de_oferta.objects.all()
    return render(request, "inicio.html", {'barrios':barrios,
                                           'tipo_inmueble':tipo_inmueble,
                                           'tipo_oferta': tipo_oferta})

def is_valid_queryparam(param):
    return param != '' and param is not None

def Busqueda(request):
    qs = Inmueble.objects.all()
    barrios = Barrio.objects.all()
    tipo_inmuebles = Tipo_de_inmueble.objects.all()
    tipo_ofertas = Tipo_de_oferta.objects.all()

    barrio = request.GET.get('barrio')
    tipo_inmueble = request.GET.get('tipo_inmueble')
    tipo_oferta = request.GET.get('tipo_oferta')

    if is_valid_queryparam(barrio):
        qs = qs.filter(IDBarrio=barrio)
        print(qs)

    if is_valid_queryparam(tipo_inmueble):
        qs = qs.filter(IDTipo_de_inmueble__nombre=tipo_inmueble)

    if is_valid_queryparam(tipo_oferta):
        qs = qs.filter(IDTipo_de_oferta__nombre=tipo_oferta)



    context = {
        'queryset': qs
        # 'barrios': barrios,
        # 'tipo_inmuebles': tipo_inmuebles,
        # 'tipo_ofertas': tipo_ofertas
    }
    return render(request, 'inmueble/inmueble_search.html', context)

# def Buscarinmueble(request):
#     if request.method == 'POST':
#         pattern = request.POST['buscar']
#         inmuebles = Inmueble.objects.filter(disponible = True,
#                                             precio__contains = pattern)
#
#     return render(request, 'inmueble/inmueble_search.html', {'object_list':inmuebles, 'buscar':pattern})


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

# class InmuebleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     """ Clase que crea la vista para registrar los inmuebles """
#
#     permission_required = 'usuario.agregar_inmueble'
#     model = Inmueble
#     template_name = 'inmueble/inmueble_form.html'
#     fields = ['direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
#                 'alcoba','baño','parqueadero','disponible','descripcion','imagen']
#
#     # Retorna a la página donde se listan los inmuebles
#     def get_success_url(self):
#         return reverse('listar')
#
#     # Muestra los registros guardados de las tablas (Barrio, Tipo_de_oferta,
#     # Tipo_de_inmueble) en los campos de selección
#     def get_context_data(self,**kwargs):
#         context = super(InmuebleCreate,self).get_context_data(**kwargs)
#         context['IDBarrio'] = Barrio.objects.all()
#         context['IDTipo_de_inmueble'] = Tipo_de_inmueble.objects.all()
#         context['IDTipo_de_oferta'] = Tipo_de_oferta.objects.all()
#         return context

# @login_required()
# Función que guarda registros de inmuebles con sus respectivas imágenes
# def Guardar_inmueble(request):
#     if request.method == 'POST':
#         direccion = request.POST.get('direccion')
#         IDBarrio = request.POST.get('IDBarrio')
#         IDTipo_de_inmueble = request.POST.get('IDTipo_de_inmueble')
#         IDTipo_de_oferta = request.POST.get('IDTipo_de_oferta')
#         precio = request.POST.get('precio')
#         alcoba = request.POST.get('alcoba')
#         baño = request.POST.get('baño')
#         parqueadero = request.POST.get('parqueadero')
#         disponible = request.POST.get('disponible')
#         descripcion = request.POST.get('descripcion')
#         imagen = request.POST.get('imagen', True)
#         is_file = request.POST.get('imagenes', True)
#
#         print(direccion)
#         print(IDBarrio)
#         print(IDTipo_de_inmueble)
#         print(IDTipo_de_oferta)
#         print(precio)
#         print(alcoba)
#         print(baño)
#         print(parqueadero)
#         print(disponible)
#         print(descripcion)
#         print(imagen)
#         print(is_file)
#
#         form = InmuebleForm(request.POST)
#         if form.is_valid():
#             inmueble = form.save()
#             for field in request.FILES.keys():
#                 if is_file == True:
#                     for formfile in request.FILES.getlist(field):
#                         img = Imagenes(ruta = formfile, IDInmueble_id = inmueble.pk)
#                         img.save()
#
#         return HttpResponseRedirect(reverse('listar'))

# Función que guarda registros de inmuebles con sus respectivas imágenes
@permission_required('usuario.agregar_inmueble')
@login_required()
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

class InmuebleView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Clase que lista los registros de los inmuebles """

    permission_required = 'usuario.listar_inmueble'
    model = Inmueble
    context_object_name = 'inmueble'

# class InmuebleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     """ Clase que edita los inmuebles """
#
#     permission_required = 'usuario.editar_inmueble'
#     model = Inmueble
#     fields = ['direccion','IDBarrio','precio','IDTipo_de_inmueble','IDTipo_de_oferta',
#                 'alcoba','baño','parqueadero','disponible','descripcion','imagenppal']
#
#     # Retorna a la página donde se listan los inmuebles
#     def get_success_url(self):
#         return reverse('listar')

class InmuebleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Clase que elimina los inmuebles """

    permission_required = 'usuario.eliminar_inmueble'
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
    """ Clase que lista los propietarios y sus inmuebles """

    permission_required = 'usuario.listar_propiedad_cliente'
    template_name = 'asesor/inmuebles.html'
    model = Propietarios_arrendatarios
    context_object_name = 'gestion'

class GestionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Clase que edita los propietarios y sus inmuebles """

    permission_required = 'usuario.editar_propiedad_cliente'
    model = Propietarios_arrendatarios
    fields = ['usuario','inmueble','tipo_cliente']

    # Retorna a la página donde se listan los propietarios y sus inmuebles
    def get_success_url(self):
        return reverse('listado')

class GestionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Clase que eliminar los propietarios y sus inmuebles """

    permission_required = 'usuario.eliminar_propiedad_cliente'
    model = Propietarios_arrendatarios
    context_object_name = 'gestion'

    # Retorna a la página donde se listan los propietarios y sus inmuebles
    def get_success_url(self):
        return reverse('listado')

class MisinmueblesList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Clase que lista los inmuebles registrados en el perfil de los clientes """

    permission_required = 'usuario.ver_inmuebles'
    template_name = 'cliente/mis_inmuebles.html'
    model = Propietarios_arrendatarios
    context_object_name = 'inmuebles'

class Citas_inmuebles(CreateView):
    """docstring for Citas_inmuebles."""

    model = cita
    template_name = 'citas_inmuebles/cita_form.html'
    fields = ['inmueble','usuario','telefono','email','asunto','mensaje']

    # Retorna a la página donde se listan los inmuebles
    def get_success_url(self):
        return reverse('cita')

# def Citas_inmuebles(request):
#     template_name = 'citas_inmuebles/cita_form.html'
#     form = CitaForm()
#
#     if request.method == 'POST':
#         form = CitaForm(request.POST)
#         if form.is_valid():
#
#             form.save()
#             messages.success(request, 'Se envió correctamente el mensaje')
#             return HttpResponseRedirect(reverse('cita'))
#         else:
#             messages.warning(request, 'Por favor, ingrese los datos otra vez.')
#             return render(request, template_name, {'form':form})
#     else:
#         form = CitaForm()
#
#     return render(request, template_name, {'form':form})


class CitaList(LoginRequiredMixin, ListView):
    """docstring for ContactoList."""

    template_name = 'asesor/mis_citas.html'
    model = cita
    context_object_name = 'cita'
