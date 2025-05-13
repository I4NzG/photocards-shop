from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update/', views.user_update, name='update'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('complete_register/', views.complete_register, name='complete_register'),
    path('tienda/', views.main_store, name='tienda'),
    path('perfil/', views.user_profile, name='perfil'),
    path('carrito/', views.carrito, name='carrito'),
    path('', views.main_store, name='home'),
    path('add_card/', views.add_card, name='add_card'),
    path('edit_card/<int:card_id>/', views.edit_card, name='edit_card'),
    path('delete_card/<int:card_id>/', views.delete_card, name='delete_card'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
