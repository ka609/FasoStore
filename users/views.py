from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from orders.models import Cart

from .models import UserProfile, Address, Notification
from .forms import UserProfileForm, AddressForm

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile,
    })

@login_required
def address_list_create(request):
    addresses = request.user.addresses.all()

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user

            # une seule adresse par défaut
            if address.is_default:
                Address.objects.filter(
                    user=request.user,
                    is_default=True
                ).update(is_default=False)

            address.save()
            messages.success(request, "Adresse ajoutée avec succès.")
            return redirect('addresses')
    else:
        form = AddressForm()

    return render(request, 'users/addresses.html', {
        'addresses': addresses,
        'form': form,
    })

@login_required
def address_update(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)

            if address.is_default:
                Address.objects.filter(
                    user=request.user,
                    is_default=True
                ).exclude(pk=address.pk).update(is_default=False)

            address.save()
            messages.success(request, "Adresse mise à jour.")
            return redirect('addresses')
    else:
        form = AddressForm(instance=address)

    return render(request, 'users/address_form.html', {
        'form': form,
        'address': address,
    })

@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, "Adresse supprimée.")
    return redirect('addresses')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # ✅ Profil utilisateur
            UserProfile.objects.create(user=user)

            # ✅ Panier utilisateur (items jamais NULL)
            Cart.objects.create(
                user=user,
                items={}
            )

            login(request, user)
            messages.success(request, "Compte créé avec succès.")
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {
        'form': form
    })


@login_required
def notifications_list(request):
    notifications = request.user.notifications.order_by('-created_at')

    return render(request, 'users/notifications.html', {
        'notifications': notifications
    })

@login_required
def notification_mark_read(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def notifications_mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    messages.success(request, "Toutes les notifications ont été marquées comme lues.")
    return redirect('notifications')
