from home.models import Variants

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variant, quantity):
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0, 'price': str(variant.total_price)}
        self.cart[variant_id]['quantity'] += quantity
        self.save()

    def remove(self, variant):
        variant_id = str(variant.id)
        del self.cart[variant_id]
        self.save()

    def remove_all(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def total_price(self):
        return sum(int(x['price']) * x['quantity'] for x in self.cart.values())

    def __iter__(self):
        variant_ids = self.cart.keys()
        products = Variants.objects.filter(id__in=variant_ids)
        for variant in products:
            self.cart[str(variant.id)]['variant'] = variant

        for data in self.cart.values():
            data['total_price'] = int(data['price']) * data['quantity']
            yield data

    def save(self):
        self.session.modified = True
