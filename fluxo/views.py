from datetime import datetime, timedelta

# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from fluxo.form import MovimentacaoForm
from fluxo.models import Movimentacao, Tipo
from venda.models import Venda


class ListReceber(ListView):
    model = Venda


class ListMovimentacao(ListView):
    model = Movimentacao

    def get_queryset(self):
        # data inicial e final sao parametros que vem do form.
        # Quando o filtro eh setado esse

        data_inicial = self.request.GET.get('data_inicial')
        data_final = self.request.GET.get('data_final')
        tipo = self.request.GET.get('tipo')

        if data_final or data_inicial:
            date = datetime.strptime(data_final, '%Y-%m-%d')
            date += timedelta(days=1)
            movimentacoes = Movimentacao.objects.filter(data__range=(data_inicial, date))
        else:
            movimentacoes = Movimentacao.objects.filter(data__month=datetime.today().month)

        if tipo:
            if tipo != '0':
                movimentacoes = movimentacoes.filter(tipo__tipo=int(tipo))

        return movimentacoes

    def get_context_data(self, **kwargs):

        context = super(ListMovimentacao, self).get_context_data()
        movimento_total = 0
        movimento_total_vista = 0
        movimento_total_cartao = 0
        movimento_total_fiado = 0

        for movimento in self.object_list.all():
            try:
                movimento_total += movimento.valor
                if movimento.tipo.pk == 4:
                    movimento_total_vista += movimento.valor
                elif movimento.tipo.pk == 3:
                    movimento_total_cartao += movimento.valor
                elif movimento.tipo.pk == 27:
                    movimento_total_fiado += movimento.valor

            except Exception as e:
                print(e, " - ", movimento)

        context['movimento_total'] = movimento_total
        context['movimento_total_vista'] = movimento_total_vista
        context['movimento_total_cartao'] = movimento_total_cartao
        context['movimento_total_fiado'] = movimento_total_fiado

        return context


class CreateMovimentacao(CreateView):
    model = Movimentacao
    form_class = MovimentacaoForm
    success_url = reverse_lazy('movimentacao:list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        f = form.save(commit=False)
        f.user = self.request.user
        f.valor = f.valor * (-1) if f.tipo.tipo == 2 else f.valor
        f.save()
        return super(CreateMovimentacao, self).form_valid(form)


class UpdateMovimentacao(UpdateView):
    model = Movimentacao
    form_class = MovimentacaoForm
    success_url = reverse_lazy('movimentacao:list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        f = form.save(commit=False)
        f.user = self.request.user
        f.valor = f.valor * (-1) if f.tipo.tipo == 2 else f.valor
        f.save()
        return super(UpdateMovimentacao, self).form_valid(form)


class ListMovimentacaoTipo(ListView):
    model = Tipo


class CreateMovimentacaoTipo(CreateView):
    model = Tipo
    fields = '__all__'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(CreateMovimentacaoTipo, self).form_valid(form)


def create_prazo(request, cod_venda):

    venda = Venda.objects.get(cod_venda=cod_venda)
    venda.pago = True
    venda.save()
    # Cria uma nova movimentacao
    Movimentacao.objects.create(valor=venda.valor_final, user=request.user, tipo_id=27,
                                fonte_destino=venda.cod_cliente.nome, link=venda.get_absolute_url())
    return redirect(reverse_lazy('movimentacao:list'))
