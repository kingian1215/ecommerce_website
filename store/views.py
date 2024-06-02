from django.shortcuts import render
from .models import Product
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem,Order, OrderItem

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def about(request):
    return render(request, 'store/about.html')

@login_required(login_url='/admin/') #檢查是否登入,若已登入才會執行add_to_cart()
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1

    cart_item.save()
    return redirect('product_list')

@login_required(login_url='/admin/')
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    return render(request,'store/view_cart.html', {'cart':cart, 'total_price':total_price})

@login_required(login_url='/admin/')
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    if request.method == 'POST':
        # 模擬實際的付款流程，寫入資料庫
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.cartitem_set.all().delete()
        return redirect('order_success') # 導向訂單成功頁面
    return render(request,'store/checkout.html', {'cart':cart, 'total_price':total_price})

@login_required(login_url='/admin/')
def order_success(request):
    return render(request,'store/order_success.html')

