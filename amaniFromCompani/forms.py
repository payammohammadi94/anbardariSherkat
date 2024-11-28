from django import forms 
from .models import amaniProductRegistrationModel

class amaniProductRegisterForm(forms.Form):
    user = forms.CharField(max_length=200)

    first_last_name_in = forms.CharField(max_length=200)
    
    first_last_name_out = forms.CharField(max_length=200)
    
    prudoct_name = forms.CharField(max_length=200)
    
    prudoct_code = forms.CharField(max_length=200)
    
    product_image = forms.ImageField()




class amaniSearchBoxForm(forms.Form):
    search_text = forms.CharField(max_length=100)



class amaniProductRegisterEditForm(forms.ModelForm):
   
    class Meta:
        model = amaniProductRegistrationModel
        fields = ['first_last_name_in','first_last_name_out','prudoct_name','prudoct_code']
        
class amaniCheckPasswordForm(forms.Form):
    input_password = forms.CharField(max_length=100)