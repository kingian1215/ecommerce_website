from django.shortcuts import render
from .models import Product
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem,Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def about(request):
    return render(request, 'store/about.html')

@login_required(login_url='/login/') #檢查是否登入,若已登入才會執行add_to_cart()
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1

    cart_item.save()
    return redirect('product_list')

@login_required(login_url='/login/')
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        if not cart_items.exists():
                message = "購物車現在是空的"
                total_price = 0
        else:
            total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
            message = ""
    
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total_price = 0
        message = "購物車現在是空的"

    return render(request,'store/view_cart.html', {'cart':cart, 'total_price':total_price, 'message': message} )

@login_required(login_url='/login/')
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        if not cart_items.exists():
                message = "購物車現在是空的"
                total_price = 0
        else:
            total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
            message = ""
            if request.method == 'POST':
                # 模擬實際的付款流程，寫入資料庫
                order = Order.objects.create(user=request.user, total_price=total_price)
                for item in cart.cartitem_set.all():
                    OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                cart.cartitem_set.all().delete()
                return redirect('order_success') # 導向訂單成功頁面

    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total_price = 0
        message = "購物車現在是空的"
    
    return render(request,'store/checkout.html', {'cart':cart, 'total_price':total_price, 'message': message})

@login_required(login_url='/login/')
def order_success(request):
    return render(request,'store/order_success.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')  # 註冊成功後導向商品列表頁面
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})