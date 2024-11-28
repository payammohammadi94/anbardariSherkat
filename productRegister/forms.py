from django import forms 
from .models import productRegistrationModel

class productRegisterForm(forms.Form):
    user = forms.CharField(max_length=200)
    first_last_name = forms.CharField(max_length=200)
    prudoct_name = forms.CharField(max_length=200)
    prudoct_code = forms.CharField(max_length=200)
    
    product_image = forms.ImageField()




class SearchBoxForm(forms.Form):
    search_text = forms.CharField(max_length=100)



class productRegisterEditForm(forms.ModelForm):
   
    class Meta:
        model = productRegistrationModel
        fields = ['first_last_name','prudoct_name','prudoct_code']
        
class checkPasswordForm(forms.Form):
    input_password = forms.CharField(max_length=100)