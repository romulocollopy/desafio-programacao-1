from django.contrib import admin
from core.models import Purchase, UploadAction


class PurchaseAdmin(admin.ModelAdmin):
    list_display = [
        'item_price', 'merchant_address', 'purchase_count',
        'item_description', 'purchaser_name', 'merchant_name']


class PurchaseInline(admin.TabularInline):
    model = Purchase


class UploadActionAdmin(admin.ModelAdmin):
    inlines = [PurchaseInline]

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(UploadAction, UploadActionAdmin)
