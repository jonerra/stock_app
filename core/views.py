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

    def get_context_data(self, **kwargs):
        context = super(StockDetail, self).get_context_data(**kwargs)
        stock = Stock.objects.get(id=self.kwargs['pk'])
        reviews = Review.objects.filter(stock=stock)
        context['reviews'] = reviews
        return context

class StockUpdate(UpdateView):
    model = Stock
    template_name = 'stock/stock_form.html'
    fields = ['symbol', 'company', 'description']

class StockDelete(DeleteView):
    model = Stock
    template_name = 'stock/stock_delete_form.html'
    success_url = reverse_lazy('stock_list')

class CreateReview(CreateView):
    model = Review
    template_name = "review/review_form.html"
    fields = ['text']

    def get_success_url(self):
        return self.object.stock.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.stock = Stock.objects.get(id=self.kwargs['pk'])
        return super(CreateReview, self).form_valid(form)

class UpdateReview(UpdateView):
    model = Review
    pk_url_kwarg = 'review_pk'
    template_name = 'review/review_form.html'
    fields = ['text']

    def get_success_url(self):
        return self.object.stock.get_absolute_url()

class DeleteReview(DeleteView):
    model = Review
    pk_url_kwarg = 'review_pk'
    template_name = 'review/review_delete_form.html'

    def get_success_url(self):
        return self.object.stock.get_absolute_url()