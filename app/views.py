from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.views.generic import TemplateView
import os
import stripe
from .models import Item, Order


# sk_test_51Lg8iOJyWq7aphhoI01yNPw9yCKx4y7amUQXoX1eNv7L4i5nSArLE8ujMSTzQyWp3fOPBU1Bb5uUCgbqynsrMJXR00vO7KJEbJ
stripe.api_key = settings.STRIPE_SECRET_KEY

global id_ses
id_ses = 0

def main(request):
    return render(request, "main.html")

def about(request):
    return render(request, "about.html")

def success(request):
    return render(request, "success.html")

def cancel(request):
    return render(request, "cancel.html")

def api(request):
    items = Item.objects.order_by('-id')
    return render(request, "api.html", {'items':items})

def add_cart(request, id):
    item = Item.objects.get(id=id)     
    try:
        order = Order.objects.order_by('-id')[0]
        order.items.add(item)
        return HttpResponseRedirect("/items_show")
    except:
        order = Order(id=1)
        order.save()
        add_cart(request, id)
        return HttpResponseRedirect("/items_show")

def shopping_cart(request):
    order = Order.objects.order_by('-id')
    try:
        order_count= Order.objects.order_by('-id')[0]
        order_items = order_count.items
        count = order_items.count
    except:
        count = 0
    return render(request, "shopping_cart.html", {'order':order, 'count':count})

def shop_delete(request, id):
    try:
        order = Order.objects.get(id=id)
        order.delete()
        return HttpResponseRedirect("/shopping_cart")
    except order.DoesNotExist:
        return HttpResponseNotFound("<h2>Товар не найден</h2>")

def items_show(request):
    items = Item.objects.order_by('-id')
    try:
        order= Order.objects.order_by('-id')[0]
        order_items = order.items
        count = order_items.count
    except:
        count = 0
    return render(request, "items_show.html", {'items':items, 'count':count})

def item(request, id):
    global id_ses
    id_ses = id
    item = Item.objects.get(id=id)
    return render(request, "item.html", {"item": item})

def create(request):
    if request.method == "POST":
        item = Item()
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.save()
    return HttpResponseRedirect("/api")
 
def edit(request, id):
    try:
        item = Item.objects.get(id=id)
 
        if request.method == "POST":
            item.name = request.POST.get("name")
            item.price = request.POST.get("price")
            item.description = request.POST.get("description")
            item.save()
            return HttpResponseRedirect("/api")
        else:
            return render(request, "edit.html", {"item": item})
    except item.DoesNotExist:
        return HttpResponseNotFound("<h2>Товар не найден</h2>")
     
def delete(request, id):
    try:
        item = Item.objects.get(id=id)
        item.delete()
        return HttpResponseRedirect("/api")
    except item.DoesNotExist:
        return HttpResponseNotFound("<h2>Товар не найден</h2>")
        

class CreateCheckoutSessionView(View):
    global id_ses
    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=id_ses)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'RUB',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/success',
            cancel_url='http://127.0.0.1:8000/cancel',
        )
        return redirect(session.url, code=303)

class ShoppingCartCheckoutSession(View):   
    def post(self, request, *args, **kwargs):
        order = Order.objects.order_by('-id')[0]
        items=order.display_items()
        amount=order.total_amount()
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'RUB',
                    'product_data': {
                        'name': items,
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/success',
            cancel_url='http://127.0.0.1:8000/cancel',
        )
        return redirect(session.url, code=303)