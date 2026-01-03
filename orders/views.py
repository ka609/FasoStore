from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from django.db.models import Q


from .models import Order, Payment, Cart,OrderItem
from shop.models import Article, Coupon
from users.models import Address

def calculate_cart_totals(cart_items):
    """
    cart_items = {
        "1": {"qty": 2, "price": "15000"},
        "5": {"qty": 1, "price": "8000"}
    }
    """
    subtotal = Decimal('0')
    for item in cart_items.values():
        subtotal += Decimal(item['price']) * item['qty']
    return subtotal


#def calculate_cart_totals(items):
   # subtotal = Decimal('0')
   # for item in items.values():
      #  subtotal += Decimal(item['price']) * int(item['quantity'])
    #return subtotal

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    addresses = request.user.addresses.all()

    if not cart.items:
        messages.warning(request, "Votre panier est vide.")
        return redirect('article_list')

    subtotal = calculate_cart_totals(cart.items)
    discount = Decimal('0')
    delivery_fee = Decimal('0')  # client ne choisit pas la livraison
    total = subtotal  # initial

    cart_items = []

    for article_id, item in cart.items.items():
        article = get_object_or_404(Article, id=article_id)

        quantity = int(item.get('qty', 1))
        price = Decimal(item['price'])

        cart_items.append({
            'id': article.id,
            'name': article.name,  # ou article.name selon ton modèle
            'price': price,
            'quantity': quantity,
            'total_price': price * quantity
        })

    if request.method == 'POST':
        address_id = request.POST.get('address')
        coupon_code = request.POST.get('coupon')

        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Gestion coupon
        if coupon_code:
            now = timezone.now()
            coupon_obj = Coupon.objects.filter(
                code=coupon_code,
                is_active=True
            ).filter(
                Q(valid_from__lte=now) | Q(valid_from__isnull=True),
                Q(valid_to__gte=now) | Q(valid_to__isnull=True),
            ).first()
            if coupon_obj:
                discount = coupon_obj.discount
            else:
                messages.error(request, "Coupon invalide")

        total = subtotal + delivery_fee - discount

        # Création commande
        order = Order.objects.create(
            user=request.user,
            address=address,
            delivery=None,  # gérant s’occupe de la livraison
            items=cart.items,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
            status='pending'
        )
        for article_id, item in cart.items.items():
            article = get_object_or_404(Article, id=article_id)

            OrderItem.objects.create(
                order=order,
                article=article,
                quantity=int(item.get('qty', 1)),
                price=Decimal(item['price'])
            )

        # Vider le panier
        cart.items = {}
        cart.save()

        messages.success(request, "Commande créée avec succès.")
        return redirect('payment', pk=order.pk)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'discount': discount,
        'total': total,
        'addresses': addresses,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def orders_list(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'orders/orders_list.html', {
        'orders': orders
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    articles = []
    for article_id, item in order.items.items():
        article = Article.objects.filter(id=article_id).first()
        if article:
            articles.append({
                'article': article,
                'qty': item['qty'],
                'price': item['price'],
            })

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'articles': articles,
    })

@login_required
def payment_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == 'POST':
        method = request.POST.get('method')

        payment = Payment.objects.create(
            order=order,
            method=method,
            amount=order.total,
            status='completed',  # simulation
            transaction_ref=f"TX-{timezone.now().timestamp()}"
        )

        order.status = 'processing'
        order.save()

        messages.success(request, "Paiement effectué avec succès.")
        return redirect('order_detail', pk=order.pk)

    return render(request, 'orders/payment.html', {
        'order': order
    })

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.status not in ['pending', 'processing']:
        messages.error(request, "Cette commande ne peut plus être annulée.")
        return redirect('order_detail', pk=pk)

    order.status = 'cancelled'
    order.save()

    messages.success(request, "Commande annulée.")
    return redirect('orders_list')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        defaults={'items': {}}
    )

    articles = []
    subtotal = Decimal('0')

    for article_id, item in cart.items.items():
        article = Article.objects.filter(id=article_id, is_active=True).first()
        if article:
            total_price = Decimal(item['price']) * item['qty']
            subtotal += total_price

            articles.append({
                'article': article,
                'qty': item['qty'],
                'price': Decimal(item['price']),
                'total': total_price,
            })

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'articles': articles,
        'subtotal': subtotal,
    })

@login_required
def add_to_cart(request, article_id):
    article = get_object_or_404(Article, id=article_id, is_active=True)

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        defaults={'items': {}}
    )

    items = cart.items or {}
    article_id = str(article.id)

    if article_id in items:
        items[article_id]['qty'] += 1
    else:
        items[article_id] = {
            'qty': 1,
            'price': str(article.price)
        }

    cart.items = items
    cart.save()

    messages.success(request, f"{article.name} ajouté au panier.")
    return redirect('cart')

@login_required
def remove_from_cart(request, article_id):
    cart = get_object_or_404(Cart, user=request.user)
    article_id = str(article_id)

    if article_id in cart.items:
        del cart.items[article_id]
        cart.save()
        messages.success(request, "Article retiré du panier.")

    return redirect('cart')

@login_required
def update_cart_qty(request, article_id):
    if request.method == 'POST':
        qty = int(request.POST.get('qty', 1))

        cart = get_object_or_404(Cart, user=request.user)
        article_id = str(article_id)

        if article_id in cart.items:
            if qty > 0:
                cart.items[article_id]['qty'] = qty
            else:
                del cart.items[article_id]

            cart.save()

    return redirect('cart')
