from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model



def redirect_to_form_if_needed(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and is_new:
        # Redirige al formulario personalizado con el email como parámetro
        return redirect(reverse('complete_register') + f'?email={user.email}')




def prevent_duplicate_user(strategy, details, backend, user=None, *args, **kwargs):
    User = get_user_model()
    email = details.get('email')
    if email and not user:
        existing = User.objects.filter(email=email).first()
        if existing:
            return {'user': existing}
        

def associate_by_email(strategy, details, user=None, *args, **kwargs):
    if user:
        return

    email = details.get('email')
    if not email:
        return

    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        return {'user': user}
    except User.DoesNotExist:
        return