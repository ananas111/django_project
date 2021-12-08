from django.forms import ModelChoiceField
from django.contrib import admin

from .models import *


class SoftwareProductAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='software'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class GameAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='game'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Game, GameAdmin)
admin.site.register(Customer)
admin.site.register(SoftwareProduct, SoftwareProductAdmin)
