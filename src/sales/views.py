from django.shortcuts import render

# Create your views here.

def home_view(request):
    hello = "fuck the world i (view) am coming home"
    return render(request, 'sales/main.html', {'h':hello})