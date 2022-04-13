from django import forms
from django.core.exceptions import ValidationError
from .models import *

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



class ImageForm(forms.ModelForm):

    class Meta:
        model = Plate
        fields = ['purpose','plate_img']
        widgets = {
            "plate_img": forms.ClearableFileInput(attrs={'class':'form-control'}),
            'purpose': forms.Select(attrs={'class':'form-select'})
        }