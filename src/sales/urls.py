from django.urls import path
from .views import (
    csv_upload_view,
    home_view,
    SaleListView,
    SaleDetailView,
    UploadTmplateView,
    csv_upload_view,
    
)


app_name = 'sales'
urlpatterns=[
    path('', home_view, name='home'),
    path('sales/', SaleListView.as_view(), name='list'),
    path('upload/', csv_upload_view, name='upload'),
    path('sales/<pk>/', SaleDetailView.as_view(), name='detail'),
    path('from_file/', UploadTmplateView.as_view(), name='from_file'),

]
