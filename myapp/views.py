from django.shortcuts import render, redirect

from django.contrib import messages


# Create your views here.
def index(request):
    return render (request,'index.html')
def home(request):
    return render (request,'home.html')


def about(request):
    return render (request,'about.html')

def login1(request):
    return render (request,'login.html')

def signup_view(request):
    return render (request,'signup.html')




# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import make_password
from .models import CustomUser  # Adjust the import according to your project structure

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Basic validations
        if not username or not name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html', {'request': request})

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', {'request': request})

        # Check for existing username and email using CustomUser
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html', {'request': request})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return render(request, 'signup.html', {'request': request})

        # Create user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # Hash the password
            name=name  # Assuming CustomUser has a name field
        )

        # Log the user in immediately after signup
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('login1')  # Redirect to a desired page after signup

    return render(request, 'signup.html', {'request': request})


from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

def login2(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate directly with email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # User is authenticated, log them in
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")
            
            # Check if the user is a staff member (admin)
            if user.is_staff:
                return redirect('/admin/')  # Redirect to the admin page for staff users
            
            # Redirect to home view after successful login for non-staff users
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'login.html')




# views.py
from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.contrib.auth.decorators import login_required

def product_listing(request):
    category_id = request.GET.get('category')  # Get category ID from the URL query parameters
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()  # If no category is selected, show all products
    
    categories = Category.objects.all()  # Fetch all categories to display in the filter

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'product_listing.html', context)
from .models import Cart, Product




def product_listing1(request):
    category_id = request.GET.get('category')  # Get category ID from the URL query parameters
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()  # If no category is selected, show all products
    
    categories = Category.objects.all()  # Fetch all categories to display in the filter

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'product_listing1.html', context)
from .models import Cart, Product


from django.shortcuts import render
from .models import Cart

def cart_view(request):
    # Get all cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate total cart price
    cart_total = sum(item.total_price() for item in cart_items)

    # Add available stock for each cart item to the context
    for item in cart_items:
        item.available_stock = item.product.stock  # Add the available stock information for validation in the template

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'cart.html', context)


# Add Product to Cart
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        # If item already in cart, increase quantity by 1
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')  # Redirect to cart view


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Product
from django.urls import reverse
from django.http import HttpResponseRedirect
# Remove Product from Cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return HttpResponseRedirect(reverse('cart_view'))  # Redirect back to cart page


def custom_logout(request):
    logout(request)  # Logs out the user
    messages.success(request, "You have been logged out successfully.")  # Add a success message
    return redirect('login1') 


from django.shortcuts import render
from django.http import HttpResponse

def forgot_password(request):
    return render(request, 'forgot_password.html')

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

def otp_verification(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_sent = request.session.get('otp')  # Retrieve the OTP from the session

        if str(otp_entered) == str(otp_sent):
            # OTP is correct
            messages.success(request, 'OTP verified successfully! You can now reset your password.')
            return redirect('reset_password')  # Redirect to password reset page
        else:
            # OTP is incorrect
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'otp_verification.html')

from django.core.mail import send_mail
import random

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = random.randint(100000, 999999)
        
        request.session['otp'] = otp
        request.session['email'] = email
        
        try:
            send_mail(
                subject='Your Password Reset OTP',
                message=f'Your OTP for password reset is {otp}.',
                from_email='your-email@example.com',
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent successfully. Please check your email.')
        except Exception as e:
            messages.error(request, f'Error sending email: {e}')
        
        return redirect('otp_verification')
    return render(request, 'forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'reset_password.html')

        email = request.session.get('email')  # Retrieve the email from the session
        if not email:
            messages.error(request, 'Session expired. Please start the process again.')
            return redirect('forgot_password')

        # Use get_user_model() to fetch the custom user model
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password reset successfully. You can now log in.')
            return redirect('login')  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
            return redirect('forgot_password')

    return render(request, 'reset_password.html')




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Order


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, Product
from django.contrib import messages

@login_required
def order_confirmation(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('cart_view')  # Redirect if the cart is empty

    cart_total = sum(item.total_price() for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone_number = request.POST.get('phone_number')

        # Validate input (optional)
        if not all([full_name, address, pincode, phone_number]):
            return render(request, 'order_confirmation.html', {
                'error': 'All fields are required.',
                'cart_items': cart_items,
                'cart_total': cart_total,
            })

        # Start a database transaction to ensure atomicity
        from django.db import transaction

        try:
            with transaction.atomic():
                # Save the order
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    address=address,
                    pincode=pincode,
                    phone_number=phone_number,
                    total_amount=cart_total,
                )
                # Link the cart items to the order
                order.items.set(cart_items)

                # Update the stock for each product
                for item in cart_items:
                    product = item.product
                    if product.stock >= item.quantity:
                        product.stock -= item.quantity  # Reduce the stock
                        product.save()
                    else:
                        # If not enough stock, cancel the order and raise an error
                        messages.error(request, f"Not enough stock for {product.name}.")
                        return redirect('cart_view')

                # Clear the cart after the order is successfully placed
                cart_items.delete()

                messages.success(request, "Order placed successfully!")
                return redirect('order_success')  # Redirect to a success page

        except Exception as e:
            messages.error(request, f"An error occurred while placing the order: {str(e)}")
            return redirect('cart_view')  # Redirect back to the cart view if something goes wrong

    return render(request, 'order_confirmation.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


from django.shortcuts import render

def order_success(request):
    return render(request, 'order.success.html')



from django.shortcuts import redirect, get_object_or_404
from .models import Cart
from django.contrib.auth.decorators import login_required

@login_required
def update_cart(request, cart_item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Get quantity from form, default to 1
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item if quantity is set to 0

    return redirect('cart_view') 


@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    return render(request, 'profile.html', {'user': user})



# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def edit_profile(request):
    user = request.user  # Get the logged-in user

    if request.method == 'POST':
        # Get new user data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Update the user object with new data
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        # Save the updated user object
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Redirect to the profile page after successful update

    return render(request, 'edit_profile.html', {'user': user})



def customer_orders(request, user_id):
    # Fetch the user based on the user_id in the URL
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Fetch orders placed by this specific user
    orders = Order.objects.filter(user=user).prefetch_related('items__product')

    return render(request, 'customer_orders.html', {'orders': orders, 'user': user})


