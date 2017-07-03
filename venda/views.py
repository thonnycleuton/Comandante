from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy

from venda.form import VendaForm
from .models import Venda


class VendaList(ListView):
    model = Venda
    queryset = Venda.objects.all()
    context_object_name = 'venda_list'


class VendaCreate(FormView):

    form_class = VendaForm
    template_name = 'venda/venda_form.html'
    success_url = reverse_lazy('vendas:list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(VendaCreate, self).form_valid(form)


class VendaUpdate(UpdateView):
    model = Venda
    success_url = reverse_lazy('venda_list')
    fields = ['cod_cliente', 'nome', 'email']


class VendaDelete(DeleteView):
    model = Venda
    success_url = reverse_lazy('venda_list')
