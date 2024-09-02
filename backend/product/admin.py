from django.contrib import admin

from .models import Product

# Register your models here.
admin.site.site_header = "E-commerce"
admin.site.site_title = "fleurette shop"
admin.site.index_title = "Manageur"

class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'price',)
    search_fields = ('name',) 
    list_editable = ('price',)

admin.site.register(Product, AdminProduct)
