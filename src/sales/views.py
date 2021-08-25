from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView,DetailView, TemplateView
from .models import Sale,Position,CSV
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from django.utils.dateparse import parse_date
import csv
from products.models import Product 
from .utils import get_customer_from_id,get_salesman_from_id,get_chart
from customer.models import Customer
from profiles.models import Profile 

# Create your views here.

def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    df =None
    chart = None
    no_data = None
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm
    if request.method == 'POST':
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        chart_type = request.POST.get("chart_type")
        results_by = request.POST.get("results_by")

        # print(date_from, date_to, chart_type)

        sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))

            sales_df.rename({'customer_id': 'customer', 'salesman_id':'salesman', 'id':'sales_id'}, axis=1,inplace=True)
            
            positions_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj ={
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity':pos.quantity,
                        'price':pos.price,
                        'sales_id': pos.get_sales_id(),                                                                 
                    }
                    positions_data.append(obj)
        
            positions_df = pd.DataFrame(positions_data)
            merged_df =pd.merge(sales_df,positions_df,on='sales_id')
            df = merged_df.groupby('transaction_id',as_index=False)['price'].agg('sum')
            
            chart = get_chart(chart_type, sales_df, results_by)
           
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df =merged_df.to_html()
            df = df.to_html()
            
        else:
            no_data = 'no data is available during this period of time'

       

    context = {
    
        'search_form':search_form,
        'no_data':no_data,
        'report_form' :report_form,
        'sales_df': sales_df,
        'positions_df':positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
    }
    return render(request, 'sales/home.html', context)
    

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model =Sale
    template_name = 'sales/detail.html'

class UploadTmplateView(TemplateView):
    template_name = 'sales/from_file.html'

def csv_upload_view(request):
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)
        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r')as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    data = "".join(row)
                    data = data.split(";")                
                    data.pop()
                

                    transaction_id = data[1]
                    product = data[2]
                    quantity = int(data[3])
                    customer = data[4]
                    date = parse_date(data[5])

                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None
                
                    if product_obj is not None:
                        customer_obj,_ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product_obj,quantity=quantity, created =date)

                        sale_obj,_ = Sale.objects.get_or_create(transaction_id=transaction_id,customer=customer_obj,salesman=salesman_obj,created=date)
                        sale_obj.positions.add(position_obj) 
                        sale_obj.save()
        
                return JsonResponse({'ex': False})
        else:
            return JsonResponse({'ex':True})
    return HttpResponse()