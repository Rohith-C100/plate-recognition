from random import choices
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User

class sign_up_form(forms.Form):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),strip=True,min_length=2,required=True)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),strip=True,min_length=2,required=True)
    email_id=forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    re_enter_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get("password")
        re_entered_password=cleaned_data.get("re_enter_password")

        if(password!=re_entered_password):
            raise ValidationError(
                "Enter the correct password for both the fields."
            )
        # else:
        #     return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
                User.objects.get(username=username)
        except User.DoesNotExist:
                return username
        raise forms.ValidationError("Username already taken.")


class ImageForm(forms.ModelForm):

    class Meta:
        model = Plate
        fields = ['purpose','plate_img']
        widgets = {
            "plate_img": forms.ClearableFileInput(attrs={'class':'form-control'}),
            'purpose': forms.Select(attrs={'class':'form-select'})
        }

class FineForm(forms.ModelForm):

    class Meta:
        model = Fine
        fields = ['img','reason','amount','date','details']
        widgets = {
            'img': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'reason':forms.TextInput(attrs={'class':'form-control'}),
            'date': AdminDateWidget(attrs={'class':'form-control','placeholder': 'yyyy-mm-dd'}),
            'details': forms.Textarea(attrs={'class':'form-control'}),
            'amount': forms.Select(attrs={'class':'form-select'}),
        }

class ComplainForm(forms.ModelForm):

    class Meta:
        model = Complain
        fields = ['severity','date_of_incident','details']
        widgets = {
            'date_of_incident': forms.DateInput(attrs={'class':'form-control','placeholder': 'yyyy-mm-dd'}),
            'severity': forms.Select(attrs={'class':'form-select'}),
            'details': forms.Textarea(attrs={'class':'form-control'}),
        }

class SearchForm(forms.Form):
    plate_number=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),strip=True,required=True)

class HistoryForm(forms.Form):
    CHOICES=[
        ("complain","complain"),
        ("fine","fine"),
    ]
    plate_number=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),strip=True,min_length=5,required=True)
    type=forms.ChoiceField(widget=forms.Select(attrs={'class':'form-select'}),choices=CHOICES)