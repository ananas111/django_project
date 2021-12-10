from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import SoftwareProduct, Game, Category, LatestProducts, Cart, Customer
from .mixins import CategoryDetailMixin
from django.http import HttpResponseRedirect


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('Game', 'SoftwareProduct')
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'software': SoftwareProduct,
        'game': Game
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        print(kwargs.get('ct_model'))
        print(kwargs.get('slug'))
        return HttpResponseRedirect('/cart/')
