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
    # Récupération ou création du profil
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Récupération de la première adresse si elle existe
    address = request.user.addresses.first()

    if request.method == "POST":
        # Formulaire profil
        form = UserProfileForm(request.POST, instance=profile)

        # Champs adresse depuis POST
        country = request.POST.get('country')
        city = request.POST.get('city')
        addr_text = request.POST.get('address')

        if form.is_valid():
            form.save()

            # Sauvegarde ou création de l'adresse
            if address:
                address.country = country
                address.city = city
                address.address = addr_text
                address.save()
            else:
                Address.objects.create(
                    user=request.user,
                    country=country,
                    city=city,
                    address=addr_text
                )

            messages.success(request, "Profil et adresse mis à jour avec succès.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'user_address': address,  # utilisé pour pré-remplir les champs adresse
    }

    return render(request, 'users/profile.html', context)

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
