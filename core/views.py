from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import *

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class StockPost(CreateView):
    model = Stock
    template_name = "stock/stock_form.html"
    fields = ['symbol', 'company', 'description']
    success_url = reverse_lazy('stock_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(StockPost, self).form_valid(form)

class StockList(ListView):
    model = Stock
    template_name = "stock/stock_list.html"

class StockDetail(DetailView):
    model = Stock
    template_name = 'stock/stock_detail.html'

class StockUpdate(UpdateView):
    model = Stock
    template_name = 'stock/stock_form.html'
    fields = ['symbol', 'company', 'description']
    
class StockDelete(DeleteView):
    model = Stock
    template_name = 'stock/stock_delete_form.html'
    success_url = reverse_lazy('stock_list')