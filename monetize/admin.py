from django.contrib import admin
from .models import DigitalProduct, Transaction

# =======================
# Digital Product Admin
# =======================
@admin.register(DigitalProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


# =======================
# Transaction Admin
# =======================
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('created_at',)
    search_fields = ('user__username', 'product__title')

# =======================
# Admin Panel Titles
# =======================
admin.site.index_title = "Monetize Admin"
admin.site.site_header = "Monetize Panel"
admin.site.site_title = "Monetize Panel"
