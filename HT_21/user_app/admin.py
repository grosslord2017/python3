from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'price', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active', 'category_fk')
    search_fields = ('name', 'author')
    actions = (
        'enable_products',
        'disable_products'
    )

    def disable_products(self, request, queryset):
        qty = queryset.update(is_active=False)
        self.message_user(request, f'{qty} products has been disabled!')

    def enable_products(self, request, queryset):
        qty = queryset.update(is_active=True)
        self.message_user(request, f'{qty} products has been enabled!')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
