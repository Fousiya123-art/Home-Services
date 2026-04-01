from django import forms
from .models import Service, cart, profile, QuoteRequest, ContactMessage


class serviceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['us']
        # fields = ['name', 'description', 'price', 'category']


class editserviceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['us']
        # fields = ['name', 'description', 'price', 'cat']


class profileForm(forms.ModelForm):
    class Meta:
        model = profile
        exclude = ['us']

class cartForm(forms.ModelForm):
    class Meta:
        model = cart
        exclude = ['us']


class quoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone (Optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }