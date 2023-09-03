from home.models import Product

Compare_SESSION_ID = 'compare'


class Compare:
    def __init__(self, request):
        self.session = request.session
        compare = self.session.get(Compare_SESSION_ID)
        if not compare:
            compare = self.session[Compare_SESSION_ID] = {}
        self.compare = compare

    def __iter__(self):
        product_ids = self.compare.keys()
        products = Product.objects.filter(id__in=product_ids)
        compare = self.compare
        for product in products:
            compare[str(product.id)]['product'] = product
        for item in compare.values():
            yield item

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.compare:
            del self.compare[product_id]
            self.save()

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.compare:
            self.compare[product_id] = {'id': product_id}
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[Compare_SESSION_ID]
        self.save()
