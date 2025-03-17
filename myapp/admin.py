from django.contrib import admin
from .models import CustomUser, Product, Category, Order, Cart

# Registering the CustomUser, Product, and Category models
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Category)

# Inline admin to display Cart items inside the Order admin
class CartInline(admin.TabularInline):
    model = Order.items.through  # Many-to-many relationship table
    extra = 1  # Show 1 empty form initially
    verbose_name = 'Item'
    verbose_name_plural = 'Items'

# Admin class for the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'get_status_display', 'total_amount')  # Display useful columns
    list_filter = ('status', 'created_at', 'user', 'items__product__category')  # Filter by status, date, user, and product category
    search_fields = ('user__email', 'full_name', 'id')  # Search by user email, full name, or order ID
    inlines = [CartInline]  # Add Cart items inline in the Order admin form

    def total_amount(self, obj):
        return sum(item.total_price() for item in obj.items.all())  # Calculate total order amount

    total_amount.short_description = 'Total Amount'

# Check if the model is already registered before registering it
if not admin.site.is_registered(Order):
    admin.site.register(Order, OrderAdmin)
