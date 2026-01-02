from django import forms
from .models import Delivery,Order,Payment

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['name', 'description', 'price', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'address',
            'delivery',
        ]
        widgets = {
            'address': forms.Select(attrs={'class': 'form-select'}),
            'delivery': forms.Select(attrs={'class': 'form-select'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method']
        widgets = {
            'method': forms.Select(
                choices=[
                    ('cash', 'Paiement à la livraison'),
                    ('mobile_money', 'Mobile Money'),
                    ('card', 'Carte bancaire'),
                ],
                attrs={'class': 'form-select'}
            )
        }
