from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import Product
from .models import Product
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import CartItem
from django.contrib import messages


def home(request):
    return render(request, 'store/home.html')


def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'store/product_list.html', {
        'products': products
    })

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     cart = request.session.get('cart', {})
#     cart[str(product_id)] = cart.get(str(product_id), 0) + 1
#     request.session['cart'] = cart
#     return redirect('store:product_list')

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Ensure user is logged in

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('store:product_list')

def view_cart(request):
    cart_items = CartItem.objects.all()  # Filter by user or session if needed
    total = sum(item.total() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


def checkout(request):
    request.session['cart'] = {}
    return render(request, 'store/checkout.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

    messages.success(request, 'Thanks for contacting us! We’ll get back to you soon.')
    return render(request, 'store/contact.html')

def about_view(request):
    return render(request, 'store/about.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('store:login') 
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('store:view_cart')



def billing_view(request):
    cart_items = CartItem.objects.all()  # Filter by user/session if needed
    total = sum(item.total() for item in cart_items)  # Use the total() method in your model

    return render(request, 'store/billing.html', {
        'cart_items': cart_items,
        'total': total
    })

def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('store:view_cart')  # or wherever your cart page is

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()  # remove item if quantity drops to 0
    return redirect('store:view_cart')


for item in CartItem.objects.all():  # ✅ Proper queryse
    item.subtotal = item.product.price * item.quantity






# Create your views here.
