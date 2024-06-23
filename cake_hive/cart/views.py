from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from cakes.models import Cake
from cart.models import Cart,Orders
from cakes.views import allcat
from django.conf import settings
import razorpay
from cart.forms import OrderForm
from django.contrib import messages
from razorpay.errors import BadRequestError
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



payment_method=''
payment_instance = client.order.create({
                        "amount": int(10 * 100),  # Amount in paise
                        "currency": "INR",
                        "payment_capture": "1"
                    })
@login_required
def cartview(request):
    u = request.user
    total = 0
    c = Cart.objects.filter(user=u)
    for i in c:
        total += i.quantity * i.cake.price

    return render(request, 'cart.html', {'c': c, 'total': total})


@login_required
def add_to_cart(request,p):
    if request.method == 'POST':
        v = Cake.objects.get(id=p)
        u = request.user
        entry_date = request.POST.get('user_entry_date')
        notes = request.POST.get('user_notes')

        try:
            cart = Cart.objects.get(user=u, cake=v)
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            Cart.objects.create(cake=v, user=u, quantity=1, user_entry_date=entry_date, user_notes=notes)

        return cartview(request)
    else:
        return allcat(request)

def remove(request, p):
        v = Cake.objects.get(id=p)
        u = request.user
        try:
            cart = Cart.objects.get(user=u, cake=v)
            if(cart.quantity>1):
                cart.quantity -= 1
                cart.save()

        except:
            pass
        return cartview(request)

def delete(request,p):
    v = Cake.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, cake=v)
        cart.delete()
        v.save()
    except:
        pass
    return cartview(request)
#

@login_required
def place_order(request):
    user = request.user

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            global shipping_add, phone, payment_instance  # Make these variables global
            shipping_address = str(form.cleaned_data['shipping_address'])
            phone = int(form.cleaned_data['phone'])
            payment_method = form.cleaned_data['payment_method']
            shipping_add=shipping_address
            cart_items = Cart.objects.filter(user=user)
            total_price = sum(item.cake.price * item.quantity for item in cart_items)

            if payment_method == 'Razorpay' and total_price < 1:
                messages.error(request, 'Order amount must be at least 1 INR for Razorpay.')
                return redirect('cart:cartview')

            if payment_method == 'Razorpay':
                    payment = client.order.create({
                        "amount": int(total_price * 100),  # Amount in paise
                        "currency": "INR",
                        "payment_capture": "1"
                    })
                    payment_instance['id']=payment['id']


                    return render(request, 'payment.html', {'payment': payment, 'order': Orders})

            else:
                # Create the order
                for item in cart_items:
                    Orders.objects.create(
                        user=user,
                        cake=item.cake,
                        no_of_items=item.quantity,
                        price=item.cake.price * item.quantity,
                        address=shipping_address,
                        phone=phone,
                        payment_method=payment_method,
                        notes=item.user_notes,
                        user_entry_date=item.user_entry_date,
                        order_status='created',
                        paid=True
                    )
                    item.delete()

                messages.success(request, 'Order placed successfully!')
                return redirect('cart:success_page')

    else:
        form = OrderForm()
    return render(request, 'placeorder.html', {'form': form})



@login_required
@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        data = request.POST
        try:
            order = Orders.objects.get(razorpay_payment_id=data['razorpay_payment_id'])
            order.payment_id = data['razorpay_payment_id']
            order.paid = True
            order.save()
        except Orders.DoesNotExist:
            return render(request, 'cart.html')

    return render(request, 'cart.html')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    return render(request, 'order_detail.html', {'order': order})


def orderview(request):
    u = request.user
    o = Orders.objects.filter(user=u)
    return render(request,'orderview.html',{'order':o,'u':u.username})

def success_page(request):
    return render(request, 'success_page.html')

def razorpay_success(request):
    global shipping_add, phone, payment_instance  # Make these variables global

    user = request.user
    cart_items = Cart.objects.filter(user=user)
    for item in cart_items:
        Orders.objects.create(
            user=user,
            cake=item.cake,
            no_of_items=item.quantity,
            price=item.cake.price * item.quantity,
            address=shipping_add,
            phone=phone,
            payment_method='razorpay',
            notes=item.user_notes,
            user_entry_date=item.user_entry_date,
            order_status='created',
            paid=True,
            razorpay_payment_id=payment_instance['id']
        )
        item.delete()
    return render(request,'razorpay_success.html')
