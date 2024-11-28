from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from jalali_date import datetime2jalali

class amaniProductRegistrationModel(models.Model):
    #یوزرنیم کاربری که محصول را میبرد
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #نام و نام خانوادگی تحویل دهنده
    first_last_name_in = models.CharField(max_length=200)

        #نام و نام خانوادگی تحویل گیرنده
    first_last_name_out = models.CharField(max_length=200)

    #نام محصول
    prudoct_name = models.CharField(max_length=200)
    #کد محصول
    prudoct_code = models.CharField(max_length=200,blank=True,null=True)
    # چک میکنیم ببینیم محصول کد محصول داره یا نه اگه نداشت باید این تیک زده بشه
    #عکس محصول
    product_image = models.ImageField("company_product/",blank=True,null=True)
    
    create = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now_add=True)
    
    
    
    #برای اینکه تحویل داده یا نه
    status = models.BooleanField(default=False)
    
    def get_jalali_date_create(self):
        return datetime2jalali(self.create)
    
    def get_jalali_date_update(self):
        return datetime2jalali(self.update)
    
    
    def __str__(self):
        return "{}-{}".format(self.first_last_name_out,self.prudoct_name)