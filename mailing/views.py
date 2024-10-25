from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import CreateView,DeleteView,UpdateView
from mailing.models import Recipient
from mailing.forms import RecipientForm

# Create your views here.

class IndexView(TemplateView):
    template_name = "mailing/index.html"


# CRUD для модели "Получатель рассылки"
class RecipientListView(ListView):
    model = Recipient


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipient_list")