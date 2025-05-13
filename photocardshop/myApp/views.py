from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import logout
from .models import Card
from .forms import AddCardForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Registro de usuario
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'user_register.html', {'form': form})

def complete_register(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            user = User.objects.get(email=email)
            user.username = username
            user.password = make_password(password) 
            user.save()
            messages.success(request, 'Registro completado. Ya puedes iniciar sesión.')
            return redirect('login')

    return render(request, 'complete_register.html', {'email': email})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}")
            return redirect('tienda')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, 'user_login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def user_update(request):
    print(f"Username: {request.user.username}, First Name: {request.user.first_name}, Last Name: {request.user.last_name}, Email: {request.user.email}")
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado!")
            return redirect('tienda')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'user_update.html', {'form': form})


@login_required
def main_store(request):
    featured_cards = Card.objects.filter(is_featured=True)[:8]
    new_arrivals = Card.objects.order_by('-created_at')[:8]
    cart_item_count = request.session.get('cart_item_count', 0)

    context = {
        'featured_cards': featured_cards,
        'new_arrivals': new_arrivals,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'main_store.html', context)

@login_required
def user_profile(request):
    return render(request, 'user_profile.html', {'user': request.user})


def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def add_card(request):
    if request.method == 'POST':
        form = AddCardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tienda')
    else:
        form = AddCardForm()
    return render(request, 'add_card.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'POST':
        form = AddCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('tienda')
    else:
        form = AddCardForm(instance=card)
    return render(request, 'edit_card.html', {'form': form, 'card': card})

@login_required
@user_passes_test(is_admin)
def delete_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'POST':
        card.delete()
        return redirect('tienda')
    return render(request, 'delete_card_confirm.html', {'card': card})


@login_required
def add_to_cart(request, card_id):
    cart = request.session.get('cart', {})


    if isinstance(cart, list):
        cart = {str(cid): 1 for cid in cart}

    card_id_str = str(card_id)

    if card_id_str in cart:
        cart[card_id_str] += 1
    else:
        cart[card_id_str] = 1

    request.session['cart'] = cart
    request.session['cart_item_count'] = sum(cart.values())

    messages.success(request, "Carta agregada al carrito exitosamente.")
    return redirect('tienda')




@login_required
def carrito(request):
    cart = request.session.get('cart', {})

    # Si por alguna razón sigue siendo lista, convierte a dict
    if isinstance(cart, list):
        cart = {str(cid): 1 for cid in cart}

    cart_items = []
    total = 0
    for card_id, quantity in cart.items():
        card = get_object_or_404(Card, pk=card_id)
        subtotal = card.price * quantity
        total += subtotal
        cart_items.append({
            'id': card.id,
            'name': card.name,
            'rarity': card.rarity,
            'price': card.price,
            'quantity': quantity,
            'total_price': subtotal,
            'image': card.image,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'carrito.html', context)