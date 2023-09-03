from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from home.models import Variants
from .forms import CartAddForm
from django.http import JsonResponse
from django.views import View
from .compare import Compare
from home.models import Product


class CartDetail(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, 'cart/cart.html', {'cart': cart})


class CartAdd(View):
    def post(self, request, *args, **kwargs):
        variant_id = request.POST.get('test')
        variant = get_object_or_404(Variants, id=variant_id)
        cart = Cart(request)
        form = CartAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cart.add(variant=variant, quantity=data['quantity'])
        return redirect('cart:details')


class CartRemove(View):
    def get(self, request, *args, **kwargs):
        variant = get_object_or_404(Variants, id=self.kwargs['pk'])
        cart = Cart(request)
        cart.remove(variant=variant)
        return redirect('cart:details')


class CartShow(View):
    def get(self, request, *args, **kwargs):
        total, price, quantity, discount = 0, 0, 0, 0
        cart = Cart(request)
        for c in cart:
            total += int(c['variant'].total_price * c['quantity'])
            price += int(c['variant'].unit_price * c['quantity'])
            quantity += c['quantity']
            discount = price - total
        response = {'total': total, 'price': price, 'quantity': quantity, 'discount': discount}
        return JsonResponse(response)


class AddSingle(View):
    def get(self, request, *args, **kwargs):
        variant_id = request.GET.get('variant_id')
        variant = get_object_or_404(Variants, id=variant_id)
        cart = Cart(request)
        cart.add(variant=variant, quantity=1)
        cart.save()
        data = {'success': 'ok'}
        return JsonResponse(data)


class RemoveSingle(View):
    def get(self, request, *args, **kwargs):
        variant_id = request.GET.get('variant_id')
        variant = get_object_or_404(Variants, id=variant_id)
        cart = Cart(request)
        cart.add(variant=variant, quantity=-1)
        cart.save()
        data = {'success': 'ok'}
        return JsonResponse(data)


class CompareProduct(View):
    def get(self, request, *args, **kwargs):
        qs = Compare(request)
        return render(request, 'cart/compare.html', {'qs': qs})


class AddCompares(View):
    def get(self, request, *args, **kwargs):
        qs = Compare(request)
        product = get_object_or_404(Product, id=kwargs['pk'])
        qs.add(product=product)
        data = {"message": "Successfully"}
        return JsonResponse(data)


class RemoveCompares(View):
    def get(self, request, *args, **kwargs):
        qs = Compare(request)
        id1 = request.GET.get('id', None)
        product = get_object_or_404(Product, id=id1)
        qs.remove(product)
        data = {'deleted': True}
        return JsonResponse(data)
