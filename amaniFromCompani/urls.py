from django.urls import path
from . import views
app_name = "amaniFromCompani"
urlpatterns = [
    path("",views.amaniHome_view,name="amani_home"),
    path("product-registration/",views.amaniProductRegistration_view,name="productRegistration"),
    path("product-registration-edit/",views.amaniProductRegistrationEdit_view,name="productRegistrationEdit"),
    path("product-registration-delete/",views.amaniProductRegistrationDelete_view,name="productRegistrationDelete"), 
    path("delivered-products/",views.amaniDeliveredProducts,name="delivered-products"),
    path("export-excel/",views.amaniExport_excel_view,name="export_excel"), 
    path("export-pdf/",views.amaniExport_pdf_view,name="export_pdf"),
    path("stop-page/",views.amaniStop_view,name="stop"),
    path("check-password-edit/<int:id>/",views.amaniCheck_password_edit_view,name="check_password_edit"),
    path("check-password-delete/<int:id>/",views.amaniCheck_password_delete_view,name="check_password_delete"),  
      
]