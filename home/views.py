from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import *
from .forms import SearchForm
from django.db.models import Q
from .filters import ProductFilter
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(ListView):
    model = Product
    template_name = 'home/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['category'] = Category.objects.filter(sub_cat=False)
        return context


class AllProduct(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('id')
        filter = ProductFilter(request.GET, queryset=products)
        products = filter.qs
        paginator = Paginator(products, 2)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        search_form = SearchForm()
        if 'search' in request.GET:
            self.kwargs['pk'] = None
            self.kwargs['slug'] = None
            search_form = SearchForm(request.GET)
            if search_form.is_valid():
                info = search_form.cleaned_data['search']
                products = products.filter(Q(name__icontains=info)).order_by('-id')
                filter = ProductFilter(request.GET, queryset=products)
                products = filter.qs
                paginator = Paginator(products, 2)
                page_num = request.GET.get('page')
                page_obj = paginator.get_page(page_num)
        if self.kwargs['pk'] and self.kwargs['slug']:
            data = get_object_or_404(Category, slug=self.kwargs['slug'], id=self.kwargs['pk'])
            products = Product.objects.filter(category=data).order_by('-id')
            filter = ProductFilter(request.GET, queryset=products, )
            products = filter.qs
            paginator = Paginator(products, 2)
            page_num = request.GET.get('page')
            page_obj = paginator.get_page(page_num)
        context = {'products': page_obj, 'filter': filter, 'search_form': search_form}
        return render(request, 'home/products.html', context)


class ProductDetails(View):
    def setup(self, request, *args, **kwargs):
        self.products = get_object_or_404(Product, id=kwargs['pk'])
        self.related_products = self.products.tags.similar_objects()[:4]
        self.comments = Comment.objects.filter(is_reply=False, product_id=kwargs['pk'])
        self.change = Chart.objects.filter(product_id=kwargs['pk'])
        try:
            self.wishlist = UserWishlist.objects.get(user_id=request.user.id)
        except:
            self.wishlist = AnonymousUser()
        self.variant = Variants.objects.filter(available=True, product_id=kwargs['pk'], )
        return super().setup(request,*args,**kwargs)

    def get(self, request, *args, **kwargs):
        variants = get_object_or_404(Variants, id=self.variant[0].id)
        size = Variants.objects.raw('SELECT * FROM home_variants WHERE product_id=%s GROUP BY size_id',
                                    [self.kwargs['pk']])
        # size = Variants.objects.filter(available=True, product_id=self.kwargs['pk']).distinct('size_id')
        colors = Variants.objects.filter(available=True, product_id=self.kwargs['pk'], size_id=self.variant[0].size_id)
        context = (
            {'products': self.products, 'related_products': self.related_products,
             'variant': self.variant, 'variants': variants, 'colors': colors, 'size': size,
             'comments': self.comments, 'change': self.change, 'wishlist': self.wishlist})
        return render(request, 'home/details.html', context)

    def post(self, request, *args, **kwargs):
        var_id = self.request.POST.get('select')
        variants = get_object_or_404(Variants, available=True, id=var_id)
        size = Variants.objects.raw(
            'SELECT * FROM home_variants WHERE product_id=%s GROUP BY size_id', [self.kwargs['pk']])
        colors = Variants.objects.filter(available=True, product_id=self.kwargs['pk'], size_id=variants.size_id)
        # size = Variants.objects.filter(available=True, product_id=self.kwargs['pk']).distinct('size_id')
        context = ({'products': self.products, 'related_products': self.related_products, 'variant': self.variant,
                    'variants': variants, 'colors': colors, 'size': size, 'comments': self.comments,
                    'change': self.change, 'wishlist': self.wishlist})
        return render(request, 'home/details.html', context)


class CommentProduct(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment', 'rate']
    template_name = 'home/details.html'

    def form_valid(self, form):
        form.instance.product_id = self.kwargs['pk']
        form.instance.user_id = self.request.user.id
        return super(CommentProduct, self).form_valid(form)

    def get_success_url(self):
        return reverse('home:details', args=[self.kwargs['pk']])


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ('comment',)
    template_name = 'home/details.html'

    def form_valid(self, form):
        form.instance.product_id = self.kwargs['pk']
        form.instance.reply_id = self.kwargs['comment_id']
        form.instance.is_reply = True
        form.instance.user_id = self.request.user.id
        return super(ReplyCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home:details', args=[self.kwargs['pk']])


class FavouriteCreateView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product,id=kwargs['pk'])
        obj = UserWishlist.objects.get(user_id=request.user.id)
        if product in obj.products.all():
            obj.products.remove(product)
        else:
            obj.products.add(product)
        data = {'success': 'ok'}
        return JsonResponse(data)
