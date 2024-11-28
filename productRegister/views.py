from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import productRegisterForm,SearchBoxForm,productRegisterEditForm,checkPasswordForm
from .models import productRegistrationModel,productReturnModel
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
import xlwt
from datetime import datetime, timezone
from jalali_date import datetime2jalali
from django.contrib.auth.hashers import check_password

# Create your views here.




@login_required(login_url='/accounts/login/')
def home_view(request):
    return render(request,'productRegister/index.html')


#این برای ثبت محصولات است
@login_required(login_url='/accounts/login/')
def productRegistration_view(request):
    
    if request.method=="POST":
        product_data = productRegisterForm(request.POST,request.FILES)
        print(product_data)
        if product_data.is_valid():
            data_clean = product_data.cleaned_data
            print(data_clean)
            


            user = data_clean["user"]
            first_last_name = data_clean["first_last_name"]
            prudoct_name = data_clean["prudoct_name"]
            prudoct_code = data_clean["prudoct_code"]
            
            product_image = data_clean["product_image"]
            
            username = User.objects.get(username=user)
            
            if request.user.is_superuser:
                if username:
                    productRegistrationModel.objects.create(user=username,first_last_name=first_last_name,prudoct_name=prudoct_name,prudoct_code=prudoct_code,product_image=product_image)
                    
                    return redirect("productRegister:delivered-products")
                else:
                    return HttpResponse("this user is not found")
            else:
                return redirect("productRegister:stop")
        else:
            return HttpResponse("data is not valid")


    return render(request,"productRegister/product-register.html",{})



@login_required(login_url='/accounts/login/')
def productRegistrationEdit_view(request):
    if request.user.is_superuser:
        id = request.session.get('edit_prodoct_key')
        product_edit = productRegistrationModel.objects.get(pk=id)
        first_last_name = product_edit.first_last_name
        product_name = product_edit.prudoct_name
        product_code = product_edit.prudoct_code
        
    
        if request.method == "POST":
            product_form_edit = productRegisterEditForm(request.POST,instance=product_edit)
            if product_form_edit.is_valid():
                product_form_edit.save()
                return redirect("productRegister:delivered-products")
            else:
                return HttpResponse("form is not valid")
        else:
            product_form_edit = productRegisterEditForm(instance=product_edit)
        context = {"product_form_edit":product_form_edit,"first_last_name":first_last_name,"product_name":product_name,"product_code":product_code}
        return render(request,"productRegister/product-edit.html",context)
    else:
        return redirect("productRegister:stop")
        
    

def productRegistrationDelete_view(request):
    if request.user.is_superuser:
        
        id = request.session.get('delete_prodoct_key')
        product_delete = productRegistrationModel.objects.get(pk=id)
        product_delete.delete()      
        return redirect("productRegister:delivered-products")
    else:
        return redirect("productRegister:stop")
        

def productRegistrationReturn_view(request):
    if request.user.is_superuser:
        
        id = request.session.get('return_prodoct_key')
        print("id",id)
        product_return = productRegistrationModel.objects.get(pk=id)
        print(product_return.user)
        print(product_return.first_last_name)
        print(product_return.prudoct_name)
        print(product_return.prudoct_code)
        print(product_return.product_image)
        productReturnModel.objects.create(
            user = product_return.user,
            first_last_name = product_return.first_last_name,
            product_name = product_return.prudoct_name,
            product_code = product_return.prudoct_code,
            product_image = product_return.product_image
        )
        product_return.delete()      
        return redirect("productRegister:delivered-products")
    else:
        return redirect("productRegister:stop")


#برای نمایش محصولات است
@login_required(login_url='/accounts/login/')
def deliveredProducts(request):
    if request.user.is_superuser:
        
        search_form_data = SearchBoxForm(request.GET)
        
        if search_form_data.is_valid():

            search_text_form = search_form_data.cleaned_data["search_text"]
            
            
            data = productRegistrationModel.objects.filter(Q(user__username__contains=search_text_form) | Q(first_last_name__contains=search_text_form) | Q(prudoct_name__contains=search_text_form) | Q(prudoct_code__contains=search_text_form))
        else:
            data = productRegistrationModel.objects.filter(status=False).order_by('-create')
        
        context = {"datas":data}
        return render(request,"productRegister/delivered-products.html",context)
    else:
        return redirect("productRegister:stop")

# برای خروجی گرفتن اکسل
@login_required(login_url='/accounts/login/')   
def export_excel_view(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type = "application/ms-excel")
        response["content-Disposition"] ='attachment;filename=delivered-products-'+str(datetime2jalali(datetime.now())).split(".")[0]+'.xls'
        
        workBook = xlwt.Workbook(encoding="utf-8")
        workSheet = workBook.add_sheet("delivered-products")
        
        columns = ["Username", "Full name", "Prudoct Name", "Prudoct Code", "Date-Time",]
        rowNumber = 0
        
        for col in range(len(columns)):
            workSheet.write(rowNumber,col,columns[col])
        
        data_for_excel = productRegistrationModel.objects.filter(status=False).order_by('-create').values_list(
            "user",
            "first_last_name",
            "prudoct_name",
            "prudoct_code",
            "create")
        
        for data in data_for_excel:
            rowNumber += 1

            for col in range(len(data)):
                if col==0:
                    workSheet.write(rowNumber,col,User.objects.get(pk=data[col]).username)
                
                
                elif col ==4:
                    workSheet.write(rowNumber,col,str(datetime2jalali(data[col])).split(".")[0])
                else:
                    workSheet.write(rowNumber,col,data[col])
        workBook.save(response)
        return response
    else:
        return redirect("productRegister:stop") 
    


def export_pdf_view(request):
    pass




def stop_view(request):
    return render(request,"productRegister/super-user-control.html")



#این ویو برای این نوشته شده که وقتی ادمین میخواد محصولی را ادیت یا حذف کند پسورد ادمین را باید وارد کند اگر درست بود اجازه حذف یا ادیت را میدیم.
@login_required(login_url='/accounts/login/')
def check_password_edit_view(request,id):
    if request.user.is_superuser:
        
        if request.method=="POST":
            form = checkPasswordForm(request.POST)
            
            if form.is_valid():
                input_password = form.cleaned_data["input_password"]
                
                #اینجا پسورد سوپر یوزر را درون دیتابیس به صورت هش میگیریم بعد چک میکنیم با هش پسورد وارد شده
                user = User.objects.get(pk=request.user.id)
                password_hash = user.password
                
                check_pass = check_password(input_password,password_hash)
                if check_pass:
                    #ای دی محصول را درون سکشن ذخیره میکنم که درون صفحه ادیت بگیریم
                    request.session['edit_prodoct_key'] = id
                    
                    return redirect("productRegister:productRegistrationEdit")
                else:
                    return redirect("productRegister:stop")
        else:
            form = checkPasswordForm()
        
        context = {"text":"check password for edite prodoct"}
        
        return render(request,'productRegister/check-password.html',context)
                         
        
    else:
        return redirect("productRegister:stop")




#این ویو برای این نوشته شده که وقتی ادمین میخواد محصولی را ادیت یا حذف کند پسورد ادمین را باید وارد کند اگر درست بود اجازه حذف یا ادیت را میدیم.
@login_required(login_url='/accounts/login/')
def check_password_delete_view(request,id):
    if request.user.is_superuser:
        
        if request.method=="POST":
            form = checkPasswordForm(request.POST)
            
            if form.is_valid():
                input_password = form.cleaned_data["input_password"]
                
                #اینجا پسورد سوپر یوزر را درون دیتابیس به صورت هش میگیریم بعد چک میکنیم با هش پسورد وارد شده
                user = User.objects.get(pk=request.user.id)
                password_hash = user.password
                
                check_pass = check_password(input_password,password_hash)
                if check_pass:
                    #ای دی محصول را درون سکشن ذخیره میکنم که درون صفحه ادیت بگیریم
                    request.session['delete_prodoct_key'] = id
                    
                    return redirect("productRegister:productRegistrationDelete")
                else:
                    return redirect("productRegister:stop")
        else:
            form = checkPasswordForm()
        
        context = {"text":"check password for delete prodoct"}
        
        return render(request,'productRegister/check-password.html',context)
                         
        
    else:
        return redirect("productRegister:stop")



@login_required(login_url='/accounts/login/')
def check_password_return_view(request,id):
    if request.user.is_superuser:
        
        if request.method=="POST":
            form = checkPasswordForm(request.POST)
            
            if form.is_valid():
                input_password = form.cleaned_data["input_password"]
                
                #اینجا پسورد سوپر یوزر را درون دیتابیس به صورت هش میگیریم بعد چک میکنیم با هش پسورد وارد شده
                user = User.objects.get(pk=request.user.id)
                password_hash = user.password
                
                check_pass = check_password(input_password,password_hash)
                if check_pass:
                    #ای دی محصول را درون سکشن ذخیره میکنم که درون صفحه ادیت بگیریم
                    request.session['return_prodoct_key'] = id
                    
                    return redirect("productRegister:productRegistrationReturn")
                else:
                    return redirect("productRegister:stop")
        else:
            form = checkPasswordForm()
        
        context = {"text":"check password for return prodoct"}
        
        return render(request,'productRegister/check-password.html',context)
                         
        
    else:
        return redirect("productRegister:stop")



#برای نمایش محصولات است
@login_required(login_url='/accounts/login/')
def returnProducts(request):
    if request.user.is_superuser:
        
        search_form_data = SearchBoxForm(request.GET)
        
        if search_form_data.is_valid():

            search_text_form = search_form_data.cleaned_data["search_text"]
            
            
            data = productReturnModel.objects.filter(Q(user__username__contains=search_text_form) | Q(first_last_name__contains=search_text_form) | Q(product_name__contains=search_text_form) | Q(product_name__contains=search_text_form))
        else:
            data = productReturnModel.objects.all().order_by('-create')
        
        context = {"datas":data}
        return render(request,"productRegister/return-product.html",context)
    else:
        return redirect("productRegister:stop")




# برای خروجی گرفتن اکسل
@login_required(login_url='/accounts/login/')   
def export_excel_return_view(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type = "application/ms-excel")
        response["content-Disposition"] ='attachment;filename=return-products-'+str(datetime2jalali(datetime.now())).split(".")[0]+'.xls'
        
        workBook = xlwt.Workbook(encoding="utf-8")
        workSheet = workBook.add_sheet("return-products")
        
        columns = ["Username", "Full name", "Product Name", "Product Code", "Date-Time",]
        rowNumber = 0
        
        for col in range(len(columns)):
            workSheet.write(rowNumber,col,columns[col])
        
        data_for_excel = productReturnModel.objects.all().order_by('-create').values_list(
            "user",
            "first_last_name",
            "product_name",
            "product_code",
            "create")
        
        for data in data_for_excel:
            rowNumber += 1

            for col in range(len(data)):
                if col==0:
                    workSheet.write(rowNumber,col,User.objects.get(pk=data[col]).username)
                
                
                elif col ==4:
                    workSheet.write(rowNumber,col,str(datetime2jalali(data[col])).split(".")[0])
                else:
                    workSheet.write(rowNumber,col,data[col])
        workBook.save(response)
        return response
    else:
        return redirect("productRegister:stop") 