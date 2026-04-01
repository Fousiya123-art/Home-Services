from django.shortcuts import render, redirect

from marketplace.models import Service
from urllib import request
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User, auth
from .forms import *
from django.contrib.auth.decorators import login_required
from .serializers import ServiceSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
import ollama


# Create your views here.
def homefn(request):
    return render(request,'home.html')


def aboutfn(request):
    return render(request,'about.html')


def contactfn(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {
                'form': ContactMessageForm(),
                'success': 'Your message has been sent successfully! We will contact you soon.'
            })
    else:
        form = ContactMessageForm()
    return render(request, 'contact.html', {'form': form})

def quotefn(request):
    if request.method == 'POST':
        form = quoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'quote.html', {
                'form': quoteRequestForm(),
                'success': 'Your quote request has been submitted. We will contact you soon.'
            })
    else:
        form = quoteRequestForm()
    return render(request, 'quote.html', {'form': form})



def servicefn(request):
    c = ServiceCategory.objects.all()
    s = Service.objects.all()
    recent_ids = request.session.get('recent_services', [])
    recent_services = Service.objects.filter(id__in=recent_ids)
    a = request.GET.get('q')
    if a:
        s = Service.objects.filter(title__icontains=a)
    
    print(f"DEBUG servicefn: Categories={c.count()}, Services={s.count()}")
    
    return render(request, 'services.html', {
        'category': c,
        'services': s,
        'recent_services': recent_services
    })


def viewservicefn(request, pid):
    service = Service.objects.get(id=pid)
    recent = request.session.get('recent_services', [])
    if pid not in recent:
        recent.append(pid)
    request.session['recent_services'] = recent[-5:]
    return render(request, 'serviceview.html', {'service': service})


def categoryviewfn(request, cid):
    x = Service.objects.filter(category=cid)
    return render(request, 'categoryview.html', {'data': x})

def register_fn(request):
    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'msg': 'user already exists'})
            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=fname,
                    last_name=lname
                )

                return redirect('home')
        else:
            return render(request, 'signup.html', {'msg': 'password not matching'})
    return render(request, 'signup.html')

def login_fn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'msg': 'invalid credentials'})
    return render(request, 'login.html')

def logout_fn(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='login')
def addservices_fn(request):
    if request.method == "POST":
        f = serviceForm(request.POST, request.FILES)
        if f.is_valid():
            x = f.save(commit=False)

            provider = ServiceProvider.objects.get(user=request.user)
            x.provider = provider

            x.save()
            return redirect('/services')
    else:
        f = serviceForm()

    return render(request, 'addservice.html', {'form': f})



@login_required(login_url='login')
def editservices_fn(request, pid):
    if request.method == "POST":
        x = Service.objects.get(id=pid)
        f = editserviceForm(request.POST, request.FILES, instance=x)
        if f.is_valid():
            x = f.save(commit=False)
            provider = ServiceProvider.objects.get(user=request.user)
            x.provider = provider
            x.save()
            return redirect('/services')
    else:
        x = Service.objects.get(id=pid)
        if request.user == x.us:
            f = editserviceForm(instance=x)
            return render(request, 'editservice.html', {'form': f})
        else:
            return HttpResponse("ERROR 404 NOT FOUND")

@login_required(login_url='/home/')
def delete_servicefn(request, pid):
    x = Service.objects.get(id=pid)
    x.delete()
    return redirect('/services')

@login_required(login_url='login')
def profilefn(request):
    if profile.objects.filter(us=request.user).exists():
        pro = Service.objects.filter(us=request.user)

        return render(request, 'profile.html', {'prod': pro})
    else:
        return redirect('/addprofile')
    

@login_required(login_url='login')
def addprofilefn(request):
    if request.method == "POST":
        f = profileForm(request.POST, request.FILES)
        if f.is_valid():
            x = f.save(commit=False)
            x.us = request.user
            x.save()
            return redirect('/profile')
    else:
        f = profileForm()
    return render(request, 'addprofile.html', {'form': f})

@login_required(login_url='login')
def add_to_cartfn(request, pid):
    serv = Service.objects.get(id=pid)
    print(serv)
    cart_item = cart.objects.filter(
        user=request.user,
        service=serv
    ).first()
     
    if cart_item:

        cart_item.quantity += 1
        cart_item.save()
    else:

        cart.objects.create(
            user=request.user,
            service=serv,
            quantity=1
        )

    return redirect('/view_cart/')

@login_required(login_url='login')
def view_cartfn(request):
    cart_items = cart.objects.filter(user=request.user)

    grand_total = 0
    for c in cart_items:
        c.item_total = c.service.price * c.quantity
        grand_total += c.item_total

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })

def delete_cart_itemfn(request, cid):
    cart_item = cart.objects.get(id=cid, user=request.user)
    cart_item.delete()
    return redirect('/view_cart/')

@login_required(login_url='login')
def update_cart_qty(request, cid):
    if request.method == "POST":
        qty = int(request.POST.get('quantity', 1))

        if qty < 1:
            return redirect('/view_cart/')

        cart_item = cart.objects.get(id=cid, user=request.user)
        cart_item.quantity = qty
        cart_item.save()

    return redirect('/view_cart/')

@api_view(['GET'])
def ourservapifn(request):
    x = Service.objects.all()
    y = ServiceSerializer(x, many=True)
    return Response(y.data)

@api_view(['GET'])
def viewservapifn(request, pid):
    x = Service.objects.get(id=pid)
    y = ServiceSerializer(x)
    return Response(y.data)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def addservapifn(request):
    x = ServiceSerializer(data=request.data)
    if x.is_valid():
        x.save()
        return Response(
            x.data, status=status.HTTP_201_CREATED
        )
    return Response(
        x.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def editservapifn(request, pid):
    a = Service.objects.get(id=pid)
    x = ServiceSerializer(data=request.data, instance=a)
    if x.is_valid():
        x.save()
        return Response(
            x.data,  status=status.HTTP_201_CREATED
        )
    
@api_view(['DELETE'])
def deleteservapifn(request, pid):
    a = Service.objects.get(id=pid)
    a.delete()
    return Response(
        {'msg': 'deleted successfully'}, status=status.HTTP_200_OK
    )


@login_required(login_url='login')
def buy_nowfn(request, cid):
    cart_item = cart.objects.get(id=cid, user=request.user)
    
    Booking.objects.create(
        user=request.user,
        service=cart_item.service,
        quantity=cart_item.quantity,
        price=cart_item.service.price
    )

    cart_item.delete()

    return HttpResponse("Order placed successfully")


def chatfn(request):
    if request.method == "POST":
        m = request.POST.get('xyz')
        res = ollama.chat(model='llama3.2:3b', messages=[
            {
                'role': 'user',
                'content': m
            }
        ])
        return render(request, 'chat.html', {'msg': res['message']['content']})
        # print(res)
        # return HttpResponse(res['message']['content'])
    return render(request, 'chat.html')

def searchfn(request):
    n = request.GET.get('q')
    x = Service.objects.filter(title__icontains=n)
    return render(request, 'search.html', {'prod': x})


