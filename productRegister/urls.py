from django.urls import path,include
from . import views


app_name = "productRegister"

urlpatterns = [
    path("",views.home_view,name="home"),
    path("product-registration/",views.productRegistration_view,name="productRegistration"),
    path("product-registration-edit/",views.productRegistrationEdit_view,name="productRegistrationEdit"),
    path("product-registration-delete/",views.productRegistrationDelete_view,name="productRegistrationDelete"), 
    path("product-registration-return/",views.productRegistrationReturn_view,name="productRegistrationReturn"), 
    path("delivered-products/",views.deliveredProducts,name="delivered-products"),
    path("return-products/",views.returnProducts ,name="return-products"),
    path("export-excel/",views.export_excel_view,name="export_excel"), 
    path("export-return-excel/",views.export_excel_return_view,name="export_return_excel"), 
    path("export-pdf/",views.export_pdf_view,name="export_pdf"),
    path("stop-page/",views.stop_view,name="stop"),
    path("check-password-edit/<int:id>/",views.check_password_edit_view,name="check_password_edit"),
    path("check-password-delete/<int:id>/",views.check_password_delete_view,name="check_password_delete"),  
    path("check-password-return/<int:id>/",views.check_password_return_view,name="check_password_return"),        
]