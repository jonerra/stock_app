from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from .models import *
from .forms import *

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class StockPost(CreateView):
    model = Stock
    template_name = "stock/stock_form.html"
    fields = ['symbol', 'company', 'description', 'post']
    success_url = reverse_lazy('stock_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(StockPost, self).form_valid(form)

class StockList(ListView):
    model = Stock
    template_name = "stock/stock_list.html"
    paginate_by = 5

class StockDetail(DetailView):
    model = Stock
    template_name = 'stock/stock_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StockDetail, self).get_context_data(**kwargs)
        stock = Stock.objects.get(id=self.kwargs['pk'])
        reviews = Review.objects.filter(stock=stock)
        context['reviews'] = reviews
        user_reviews = Review.objects.filter(stock=stock, user=self.request.user)
        context['user_reviews'] = user_reviews
        return context

class StockUpdate(UpdateView):
    model = Stock
    template_name = 'stock/stock_form.html'
    fields = ['symbol', 'company', 'description']

    def get_object(self, *args, **kwargs):
        object = super(StockUpdate, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class StockDelete(DeleteView):
    model = Stock
    template_name = 'stock/stock_delete_form.html'
    success_url = reverse_lazy('stock_list')

    def get_object(self, *args, **kwargs):
        object = super(StockDelete, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class CreateReview(CreateView):
    model = Review
    template_name = "review/review_form.html"
    fields = ['text', 'post']

    def get_success_url(self):
        return self.object.stock.get_absolute_url()

    def form_valid(self, form):
        stock = Stock.objects.get(id=self.kwargs['pk'])
        if Review.objects.filter(stock=stock, user=self.request.user).exists():
            raise PermissionDenied()
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

    def get_object(self, *args, **kwargs):
        object = super(UpdateReview, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class DeleteReview(DeleteView):
    model = Review
    pk_url_kwarg = 'review_pk'
    template_name = 'review/review_delete_form.html'

    def get_success_url(self):
        return self.object.stock.get_absolute_url()

    def get_object(self, *args, **kwargs):
        object = super(DeleteReview, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object

class VoteFormView(FormView):
    form_class = VoteForm

    def form_valid(self, form):
        user = self.request.user
        stock = Stock.objects.get(pk=form.data["stock"])
        try:
            review = Review.objects.get(pk=form.data["review"])
            prev_votes = Vote.objects.filter(user=user, review=review)
            has_voted = (prev_votes.count()>0)
            if not has_voted:
                Vote.objects.create(user=user, review=review)
            else:
                prev_votes[0].delete()
            return redirect(reverse('stock_detail', args=[form.data["stock"]]))
        except:
            prev_votes = Vote.objects.filter(user=user, stock=stock)
            has_voted = (prev_votes.count()>0)
            if not has_voted:
                Vote.objects.create(user=user, stock=stock)
            else:
                prev_votes[0].delete()
        return redirect('stock_list')

class UserDetail(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'user/user_detail.html'
    context_object_name = 'user_in_view'

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        user_in_view = User.objects.get(username=self.kwargs['slug'])
        stocks = Stock.objects.filter(user=user_in_view).exclude(post=1)
        context['stocks'] = stocks
        reviews = Review.objects.filter(user=user_in_view).exclude(post=1)
        context['reviews'] = reviews
        return context

class UserEdit(UpdateView):
    model = User
    slug_field = "username"
    template_name = "user/user_form.html"
    fields = ['email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('user_detail', args=[self.request.user.username])

    def get_object(self, *args, **kwargs):
        object = super(UserEdit, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

class DeleteUser(DeleteView):
    model = User
    slug_field = "username"
    template_name = 'user/user_delete_form.html'

    def get_success_url(self):
        return reverse_lazy('logout')

    def get_object(self, *args, **kwargs):
        object = super(DeleteUser, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

    def delete(self, request, *args, **kwargs):
        user = super(DeleteUser, self).get_object(*args)
        user.is_active = False
        user.save()
        return redirect(self.get_success_url())

class SearchStock(StockList):
    def get_queryset(self):
        incoming_query_string = self.request.GET.get('query','')
        return Stock.objects.filter(company__icontains=incoming_query_string)