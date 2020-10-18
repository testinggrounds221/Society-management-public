from django.urls import path
from . import views

urlpatterns = [
	path("",views.user_page,name="User Page"),
	path("pay/<int:invoice_id>",views.payment_page,name="Payment Page"),
	path("pay/generate/<int:invoice_id>",views.generate_receipt,name="Generate Receipt"),
	path("pay/generate/<int:invoice_id>/paid",views.payment_success,name="Generate Receipt"),	
	path("pay/receipt/<int:receipt_id>/",views.receipt_page,name="Receipt Page"),
	path("pay/receipts",views.all_receipts,name="All Receipts"),
	
]