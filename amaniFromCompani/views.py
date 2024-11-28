from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
import xlwt
from datetime import datetime, timezone
from jalali_date import datetime2jalali
from django.contrib.auth.hashers import check_password

from .models import amaniProductRegistrationModel
from .forms import amaniProductRegisterForm, amaniSearchBoxForm, amaniProductRegisterEditForm, amaniCheckPasswordForm

# Create your views here.

@login_required(login_url='/accounts/login/')
def amaniHome_view(request):
    return render(request,'amaniFromCompani/index.html')
    


#این برای ثبت محصولات است
@login_required(login_url='/accounts/login/')
def amaniProductRegistration_view(request):
    if request.user.is_superuser:
        if request.method=="POST":
            product_data = amaniProductRegisterForm(request.POST,request.FILES)
            
            if product_data.is_valid():
                data_clean = product_data.cleaned_data
                user = data_clean["user"]
                first_last_name_in = data_clean["first_last_name_in"]
                first_last_name_out = data_clean["first_last_name_out"]
                
                prudoct_name = data_clean["prudoct_name"]
                prudoct_code = data_clean["prudoct_code"]
            
                product_image = data_clean["product_image"]
            
                username = User.objects.get(username=user)

                if username:
                    amaniProductRegistrationModel.objects.create(user=username,first_last_name_in=first_last_name_in,first_last_name_out=first_last_name_out,prudoct_name=prudoct_name,prudoct_code=prudoct_code,product_image=product_image)
                    
                    return redirect("amaniFromCompani:delivered-products")
                else:
                    return HttpResponse("this user is not found")
            else:
                return HttpResponse("data is not valid.")

        return render(request,"amaniFromCompani/product-register.html",{})
        


            
    
    else:
        return redirect("amaniFromCompani:stop")




@login_required(login_url='/accounts/login/')
def amaniProductRegistrationEdit_view(request):
    if request.user.is_superuser:
        id = request.session.get('edit_prodoct_key_amani')
        product_edit = amaniProductRegistrationModel.objects.get(pk=id)
        first_last_name_in = product_edit.first_last_name_in
        first_last_name_out = product_edit.first_last_name_out
        product_name = product_edit.prudoct_name
        product_code = product_edit.prudoct_code
        
    
        if request.method == "POST":
            product_form_edit = amaniProductRegisterEditForm(request.POST,instance=product_edit)
            if product_form_edit.is_valid():
                product_form_edit.save()
                return redirect("amaniFromCompani:delivered-products")
            else:
                return HttpResponse("form is not valid")
        else:
            product_form_edit = amaniProductRegisterEditForm(instance=product_edit)
        context = {"product_form_edit":product_form_edit,"first_last_name_in":first_last_name_in,"first_last_name_out":first_last_name_out,"product_name":product_name,"product_code":product_code}
        return render(request,"amaniFromCompani/product-edit.html",context)
    else:
        return redirect("amaniFromCompani:stop")


def amaniProductRegistrationDelete_view(request):
    if request.user.is_superuser:
        
        id = request.session.get('delete_prodoct_key_amani')
        product_delete = amaniProductRegistrationModel.objects.get(pk=id)
        product_delete.delete()      
        return redirect("amaniFromCompani:delivered-products")
    else:
        return redirect("amaniFromCompani:stop")


#برای نمایش محصولات است
@login_required(login_url='/accounts/login/')
def amaniDeliveredProducts(request):
    if request.user.is_superuser:
        
        search_form_data = amaniSearchBoxForm(request.GET)
        
        if search_form_data.is_valid():

            search_text_form = search_form_data.cleaned_data["search_text"]
            
            
            data = amaniProductRegistrationModel.objects.filter(Q(user__username__contains=search_text_form) | Q(first_last_name_in__contains=search_text_form) | Q(first_last_name_out__contains=search_text_form) | Q(prudoct_name__contains=search_text_form) | Q(prudoct_code__contains=search_text_form))
        else:
            data = amaniProductRegistrationModel.objects.filter(status=False).order_by('-create')
        
        context = {"datas":data}
        return render(request,"amaniFromCompani/delivered-products.html",context)
    else:
        return redirect("amaniFromCompani:stop")




def amaniExport_excel_view(request):
    pass


def amaniExport_pdf_view(request):
    pass


def amaniStop_view(request):
    return render(request,"amaniFromCompani/super-user-control.html")



@login_required(login_url='/accounts/login/')
def amaniCheck_password_edit_view(request,id):
    if request.user.is_superuser:
        
        if request.method=="POST":
            form = amaniCheckPasswordForm(request.POST)
            
            if form.is_valid():
                input_password = form.cleaned_data["input_password"]
                
                #اینجا پسورد سوپر یوزر را درون دیتابیس به صورت هش میگیریم بعد چک میکنیم با هش پسورد وارد شده
                user = User.objects.get(pk=request.user.id)
                password_hash = user.password
                
                check_pass = check_password(input_password,password_hash)
                if check_pass:
                    #ای دی محصول را درون سکشن ذخیره میکنم که درون صفحه ادیت بگیریم
                    request.session['edit_prodoct_key_amani'] = id
                    print(id)
                    
                    return redirect("amaniFromCompani:productRegistrationEdit")
                else:
                    return redirect("amaniFromCompani:stop")
        else:
            form = amaniCheckPasswordForm()
        
        context = {"text":"check password for edite prodoct"}
        
        return render(request,'amaniFromCompani/check-password.html',context)
                         
        
    else:
        return redirect("amaniFromCompani:stop")


@login_required(login_url='/accounts/login/')
def amaniCheck_password_delete_view(request,id):
    if request.user.is_superuser:
        
        if request.method=="POST":
            form = amaniCheckPasswordForm(request.POST)
            
            if form.is_valid():
                input_password = form.cleaned_data["input_password"]
                
                #اینجا پسورد سوپر یوزر را درون دیتابیس به صورت هش میگیریم بعد چک میکنیم با هش پسورد وارد شده
                user = User.objects.get(pk=request.user.id)
                password_hash = user.password
                
                check_pass = check_password(input_password,password_hash)
                if check_pass:
                    #ای دی محصول را درون سکشن ذخیره میکنم که درون صفحه ادیت بگیریم
                    request.session['delete_prodoct_key_amani'] = id
                    
                    return redirect("amaniFromCompani:productRegistrationDelete")
                else:
                    return redirect("amaniFromCompani:stop")
        else:
            form = amaniCheckPasswordForm()
        
        context = {"text":"check password for delete prodoct"}
        
        return render(request,'amaniFromCompani/check-password.html',context)
                         
        
    else:
        return redirect("amaniFromCompani:stop")


      