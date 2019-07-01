from django.shortcuts import render
from django.shortcuts import render, redirect
from producto.models import producto, categoria, stock
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from usuario.models import usuario, user_logs
from compras.models import compra

from django.dispatch import receiver
from defender import signals
# Create your views here.

def indexView(request, *args, **kwargs):
    if request.GET.get('id') == None:
        items = producto.objects.all()
    else:
        items = producto.objects.filter(categoria=request.GET.get('id'))



    categorias = categoria.objects.all()
    template = "index.html"
    context = {'productos': items, 'categorias': categorias}
    return render(request, template, context)

def adminUserView(request, *arg, **kwargs):
    users = usuario.objects.all()
    context = {'users': users}
    template = "admin_user.html"
    return render(request, template, context)
    

def loginView(request, *args, **kwargs):
    template = "login.html"
    return render(request,template)

def adminView(request, *args, **kwargs):
    template = "admin.html"
    return  render(request,template)


@receiver(signals.username_block)
def login (request, *args, **kwargs):
    context = RequestContext(request)
    if request.method == 'POST':
        email= request.POST['email']
        password = request.POST['password']
        user = authenticate(request= request,username=email, password=password)


        if user:
            if user.is_active:
                auth_login(request, user)

                if user.tipo.id == 2:
                    return HttpResponseRedirect('/administrador')
                else:
                       return HttpResponseRedirect ('/')
        else:
            return HttpResponseRedirect('/')

#Edit user
def saveuser(request, *arg, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        lastname = request.POST['userlastname']
        userwallet = request.POST['userwallet']

        try:
            userisactive = request.POST['user_is_active']
            if userisactive == "on":
                userisactive = True
        except:
            userisactive = False


        userid = request.POST['userid']
        user = usuario.objects.get(pk=userid)
        user.nombre = username
        user.apellido = lastname
        user.wallet = userwallet
        user.is_active = userisactive
        user.save()
        return HttpResponseRedirect('/administrador/users/')

def deleteuser(request, *arg, **kwargs):
    usuario.objects.filter(id=request.GET.get('id')).delete()
    return HttpResponseRedirect('/administrador/users/')


def logout(request, *args, **kwargs):
    auth_logout(request)
    return HttpResponseRedirect ('/')

def comprar(request, *arg, **kwargs):
  inventario = stock.objects.get(producto=request.POST['id'])
  if int(request.POST['cantidad']) <= inventario.cantidad and request.user.wallet >= (inventario.producto.precio * int(request.POST['cantidad'])):
    user = usuario.objects.get(id=request.user.id)
    user.wallet = user.wallet - inventario.producto.precio * int(request.POST['cantidad'])
    user.save()
    inventario.cantidad = inventario.cantidad - int(request.POST['cantidad'])
    inventario.save()

    compra.objects.create(user=user, product= inventario.producto, cantidad=int(request.POST['cantidad']), precio_total=int(request.POST['cantidad'])*inventario.producto.precio )
    user_logs.objects.create(usuario=user,acciones='C')

  return HttpResponseRedirect('/')

  #user_logs



