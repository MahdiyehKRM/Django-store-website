from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from cart.cart import Cart
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.utils.crypto import get_random_string
from .forms import CouponForm
from django.views import View
from suds import Client
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderDetail(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        products = ItemOrder.objects.filter(pk=kwargs['pk'])
        form = CouponForm()
        context = {'order': order, 'form': form, 'products': products}
        return render(request, 'order/orders.html', context)


class OrderInformation(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'order/order.html')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect('order:information')

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            code = get_random_string(length=8)
            order = Order.objects.create(user_id=request.user.id, email=data['email'], f_name=data['f_name'],
                                         l_name=data['l_name'], address=data['address'], code=code)
            cart = Cart(request)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, variant=c['variant'],
                                         quantity=c['quantity'])

            return redirect('order:order_detail', order.id)
        else:
            return redirect('order:information')


class CouponOrder(View):
    def post(self, request, *args, **kwargs):
        form = CouponForm(request.POST)
        order = get_object_or_404(Order, pk=kwargs['pk'])
        time = timezone.now()
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this code wrong', 'danger')
                return redirect('order:order_detail', self.kwargs['pk'])
            order.discount = coupon.discount
            order.save()
        return redirect('order:order_detail', self.kwargs['pk'])


MERCHANT = '?????'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/order/verify/'  # Important: need to edit for realy server.


class SendRequest(View):
    def get(self, request, *args, **kwargs):
        global o_id
        o_id = kwargs['pk']
        orders = get_object_or_404(Order, id=o_id)
        result = client.service.PaymentRequest(MERCHANT, orders.get_price(), description,
                                               request.user.email, mobile, CallbackURL)
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))


class Verify(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('Status') == 'OK':
            order = get_object_or_404(Order, id=o_id)
            result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], order.get_price())
            if result.Status == 100:
                order.paid = True
                order.save()
                return render(request, 'order/success.html', {'order': order})
            elif result.Status == 101:
                return render(request, 'order/error.html')
            else:
                return render(request, 'order/error.html')
        else:
            return render(request, 'order/error.html')
