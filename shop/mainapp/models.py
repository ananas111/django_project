from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class().base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):
    CATEGORY_NAME_COUNT_NAME = {
        'Game': 'game__count',
        'SoftwareProduct': 'softwareproduct__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('game', 'softwareproduct')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Category Name", unique=True)
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=255,verbose_name="Product Name")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Image")
    description = models.TextField(verbose_name="Description", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Price")

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class SoftwareProduct(Product):
    OS = models.CharField(max_length=255, verbose_name="OS Type")
    subscription_duration = models.CharField(max_length=255, verbose_name="Subscription Duration")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Game(Product):
    genre = models.CharField(max_length=255, verbose_name="Genre")
    release_date = models.DateField(verbose_name="Release Date")
    company = models.CharField(max_length=255, verbose_name="Company")
    age_restrictions = models.CharField(max_length=255, verbose_name="Age restrictions")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name="Customer", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Cart", on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveSmallIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Total Price")

    def __str__(self):
        return "Product: {} (for cart)" .format(self.content_object.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='User', on_delete=models.CASCADE, unique=True)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Total Price")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone number')
    address = models.CharField(max_length=255, verbose_name='Address')

    def __str__(self):
        return "Customer: {}, {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):
    pass

