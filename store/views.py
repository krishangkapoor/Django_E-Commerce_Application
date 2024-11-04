from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.urls import reverse_lazy
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageForm
from .cart import Cart
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# Create product (admin only)
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('image') 
        for image in images:
            ProductImage.objects.create(product=self.object, image=image)
        return response


# Update product (admin only)
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('image')  
        for image in images:
            ProductImage.objects.create(product=self.object, image=image)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_images'] = ProductImage.objects.filter(product=self.object)
        return context

# Delete product (admin only)
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product_images = ProductImage.objects.filter(product=product)
        for image in product_images:
            image.delete()
        return super().delete(request, *args, **kwargs)


def delete_product_image(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)
    product_id = image.product.id
    image.delete()
    return redirect('product_update', pk=product_id)

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product)
    
    if request.user.is_authenticated:
        product_image_url = request.build_absolute_uri(product.image.url)
        context = {
            'product': product,
            'product_image_url': product_image_url,
            'user': request.user,
        }
        html_message = render_to_string('store/add_to_cart_email.html', context)
        send_mail(
            subject='Item Added to Your Cart',
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=False,
            html_message=html_message,
        )
    return redirect('product_list')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    total_price = cart.get_total_price()
    return render(request, 'store/cart_detail.html', {'cart': cart, 'total_price': total_price})

def buy_now(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.clear()  
    cart.add(product, quantity=1, update_quantity=True)  
    total_price = product.price  
    return redirect('checkout')  

def buy_all(request):
    cart = Cart(request)
    return redirect('checkout')  

def checkout(request):
    cart = Cart(request)
    total_price = cart.get_total_price()

    if request.method == 'POST':
        if request.user.is_authenticated:
            product_details = []
            for item in cart:
                product_details.append({
                    'name': item['product'].name,
                    'quantity': item['quantity'],
                    'image_url': request.build_absolute_uri(item['product'].image.url)
                })

            context = {
                'user': request.user,
                'product_details': product_details,
                'total_price': total_price
            }
            html_message = render_to_string('store/purchase_confirmation_email.html', context)

            send_mail(
                subject='Purchase Confirmation',
                message='',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
                fail_silently=False,
                html_message=html_message,
            )
        cart.clear()
        return redirect('payment_form')
    return render(request, 'store/checkout.html', {'total_price': total_price})

class PaymentForm(forms.Form):
    name = forms.CharField(label="Name on Card", max_length=100)
    card_number = forms.CharField(label="Card Number", max_length=19)
    expiry = forms.CharField(label="Expiry Date (MM/YY)", max_length=5)
    cvv = forms.CharField(label="CVV", max_length=3)

class PaymentFormView(FormView):
    template_name = 'store/payment_form.html'
    form_class = PaymentForm
    success_url = reverse_lazy('thank_you') 

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            cart = Cart(self.request)
            total_price = cart.get_total_price()
            product_details = []
            for item in cart:
                product_details.append({
                    'name': item['product'].name,
                    'quantity': item['quantity'],
                    'image_url': self.request.build_absolute_uri(item['product'].image.url)
                })
            context = {
                'user': self.request.user,
                'product_details': product_details,
                'total_price': total_price
            }
            html_message = render_to_string('store/purchase_confirmation_email.html', context)

            send_mail(
                subject='Purchase Confirmation',
                message='',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.request.user.email],
                fail_silently=False,
                html_message=html_message,
            )
        return super().form_valid(form)

class ThankYouView(TemplateView):
    template_name = 'store/thank_you.html'

class PaymentProcessView(FormView):
    template_name = 'store/payment_form.html'
    form_class = PaymentForm
    success_url = reverse_lazy('thank_you')

    def form_valid(self, form):
        return super().form_valid(form)