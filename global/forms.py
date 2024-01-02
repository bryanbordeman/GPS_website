from .models import *
from django.forms import ModelForm
from django import forms

class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name','class' : 'form-control'})
        self.fields['first_name'].label = False
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name','class' : 'form-control'})
        self.fields['last_name'].label = False
        self.fields['email'].widget.attrs.update({'placeholder': 'Email','class' : 'form-control'})
        self.fields['email'].label = False
        self.fields['phone'].widget.attrs.update({'placeholder': 'Phone Numbers','class' : 'form-control'})
        self.fields['phone'].label = False
        self.fields['company_name'].widget.attrs.update({'placeholder': 'Company Name','class' : 'form-control'})
        self.fields['company_name'].label = False
        # self.fields['address1'].label = False
        # self.fields['address1'].widget.attrs.update({'placeholder': 'Address','class' : 'form-control'})
        # self.fields['address2'].label = False
        # self.fields['address2'].widget.attrs.update({'placeholder': 'Address','class' : 'form-control'})
        # self.fields['city'].label = False
        # self.fields['city'].widget.attrs.update({'placeholder': 'City','class' : 'form-control', })
        # self.fields['state'].label = False
        # self.fields['state'].widget.attrs.update({'placeholder': 'State','class' : 'form-control'})
        # self.fields['zip_code'].label = False
        # self.fields['zip_code'].widget.attrs.update({'placeholder': 'Zip','class' : 'form-control'})
        # self.fields['country'].widget.attrs.update({'class' : 'form-control'})
        # # self.fields['country'].empty_label = 'Select Country'
        # self.fields['country'].label = 'Select Country'
        self.fields['description'].widget.attrs.update({'placeholder': 'Give us a bit of detail on your project.','class' : 'form-control', 'id': 'description'})
        self.fields['description'].label = False
        
        
class windowForm(forms.Form): 
    width = forms.FloatField(max_value=200, min_value=12)  
    max_height = forms.CharField(max_length=50)  
  



   
# class AddressForm(ModelForm):
#     class Meta:
#         model = Address
#         fields = '__all__'
#         widgets = {
#             'address1': forms.TextInput(attrs={'placeholder': 'Address Line 1', 'class': 'form-control'}),
#             'address2': forms.TextInput(attrs={'placeholder': 'Address Line 2', 'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
#             'state': forms.Select(attrs={'placeholder': 'State', 'class': 'form-control',}),
#             'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
#             'country': forms.Select(attrs={'placeholder': 'Country', 'class': 'form-control'}),

#         }
#     def __init__(self, *args, **kwargs):
#         super(AddressForm, self).__init__(*args, **kwargs)
#         self.fields['address1'].label = False
#         self.fields['address2'].label = False
#         self.fields['city'].label = False
#         self.fields['zip_code'].label = False

