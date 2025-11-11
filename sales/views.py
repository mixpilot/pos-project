from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, SaleTransaction, SaleItem
from django.utils import timezone
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        # Validation to ensure values are not empty
        if not price or not stock:
            return render(request, 'sales/add_product.html', {
                'error': 'please fill in all fields'
            })

        price = float(price)
        stock = int(stock)

        Product.objects.create(
            name=name,
            category=category,
            price=price,
            stock=stock,
        )
        return redirect('product_list')

    return render(request, 'sales/add_product.html')


@login_required
def record_sale(request):
    products = Product.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        product = Product.objects.get(id=product_id)

        transaction = SaleTransaction.objects.create(timestamp=timezone.now())

        SaleItem.objects.create(
            transaction=transaction,
            product=product,
            quantity=quantity,
            subtotal=product.price * quantity
        )

        product.stock -= quantity
        product.save()

        return redirect('record-sale')
    return render(request, 'sales/record_sale.html', {'products': products})


@login_required
def sales_summary(request):
    transactions = SaleTransaction.objects.all().order_by('-timestamp')
    return render(request, 'sales/sales_summary.html', {'transactions': transactions})


@login_required
def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(SaleTransaction, id=transaction_id)
    items = SaleItem.objects.filter(transaction=transaction)
    return render(request, 'sales/transction_detail.html', {
        'transaction': transaction,
        'items': items
    })





