from stock.models import Company
from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render,get_object_or_404
import FinanceDataReader as fdr
from .models import Company
import pandas as pd


# Create your views here.
def index(request):
    
    # company_list = fdr.StockListing("NYSE")[:50]
    # company_list = pd.concat(company_list, ignore_index=True)
    print(company_list)
    context = {'company_list':company_list}
    return render(request,'stock/company_list.html',context)

