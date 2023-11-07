from django.db.utils import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TareaForm
from .models import Tarea
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm(),
                                                       'error': 'El usuario ya existe'})

        return render(request, 'signup.html', {'form': UserCreationForm(),
                                               'error': 'La contraseña no coincide'})


@login_required
def tareas(request):
    lista_tareas = Tarea.objects.filter(
        user=request.user, datecompleted__isnull=True)
    return render(request, 'tareas.html', {'tareas': lista_tareas})


@login_required
def tareas_completed(request):
    lista_tareas = Tarea.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tareas.html', {'tareas': lista_tareas})


@login_required
def created_tareas(request):
    if request.method == 'GET':
        return render(request, 'created_tareas.html', {'form': TareaForm()})
    else:
        try:
            form = TareaForm(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'created_tareas.html', {'form': TareaForm(),
                                                           'error': 'No se pudo guardar la tarea'})


@login_required
def tarea_detail(request, tarea_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user)
        form = TareaForm(instance=tarea)
        return render(request, 'tarea_detail.html', {'tarea': tarea, 'form': form})
    else:
        try:
            nueva_tarea = get_object_or_404(
                Tarea, pk=tarea_id, user=request.user)
            new_form = TareaForm(request.POST, instance=nueva_tarea)
            new_form.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'tarea_detail.html', {'tarea': tarea, 'form': form,
                                                         'error': 'Error al actualizar'})


@login_required
def complete_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.datecompleted = timezone.now()
        tarea.save()
        return redirect('tareas')


@login_required
def delete_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form': AuthenticationForm(),
                                                  'error': 'Usuario o contraseña incorrectos'})

        else:
            login(request, user)
            return redirect('tareas')
