from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import auth
import datetime
from django.http import HttpResponse
from django.http import JsonResponse
import json
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cart=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    items = Item.objects.all()
    Staff = staff.objects.all() 
    return render(request, 'index.html',  {'items': items, 'staff': Staff,'cartItems':cartItems})
def menu(request):
    items = Item.objects.all()
    return render(request, 'menu.html', {'items': items})
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cart=order.orderitem_set.all()
    else:
        items=[]
        cart=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
    return render(request, 'cart.html',{'cart':cart,'order':order})
def my_table(request):
    pass
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cart=order.orderitem_set.all()
    else:

        cart=[]
        order={'get_cart_total':0,'get_cart_items':0}
    #context={'cart'=items}
    return render(request, 'checkout.html',{'cart':cart,'order':order,'shipping':False})
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action:',action)
    print('productId:',productId)
    customer=request.user.customer
    product=Item.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action =='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                pincode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in.')
    return JsonResponse({'message': 'Payment complete'}, safe=False)
def contact(request):
    return render(request, 'contact.html')
def service(request):
    return render(request, 'service.html')
def testimonial(request):
    return render(request, 'testimonial.html')
def about(request):
    return render(request, 'about.html')
def booking(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    return render(request, 'booking.html',{'cartItems':cartItems})
def team(request):
    return render(request, 'team.html')
@login_required
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.email = request.user.email
            booking.save()
            return redirect('success')  # Ensure you have a 'success' URL defined
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})
def success(request):
    return render(request, 'success.html')
@login_required
def my_table(request):
    tables = Booking.objects.filter(user=request.user)
    return render(request, 'my_table.html', {'tables': tables})
