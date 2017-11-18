# encoding=utf-8
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from cliente.models import Cliente
from fluxo.models import Movimentacao
from servico.models import Servico


class Venda(models.Model):
    cod_venda = models.CharField(max_length=11, blank=True, unique=True)
    cod_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ManyToManyField(Servico, through='ItensVenda', through_fields=('cod_venda', 'cod_servico'),
                                     blank=True)
    data_venda = models.DateTimeField(auto_now_add=True)
    data_pagamento = models.DateTimeField(auto_now=False, default=datetime.today(), blank=True)
    tipo = models.IntegerField(choices=((1, 'A vista'), (2, 'Prazo'), (3, 'Debito'), (4, 'Credito')), blank=True, null=True)
    valor_venda = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    comanda = models.BooleanField(default=True, verbose_name="Comanda")
    desconto = models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True)
    valor_final = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ('-data_venda',)
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'

    def __str__(self):
        return self.cod_venda

    def get_absolute_url(self):
        return "/editar/%s/" %self.pk

    def update_valores(self):
        valor_total = 0
        itens = ItensVenda.objects.filter(cod_venda=self.pk)
        for item in itens:
            valor_total += item.valor
        self.valor_venda = valor_total
        self.save()

    def get_total_vendas(self):

        total_vendas = 0
        for item in self.objects.all():
            total_vendas += item.valor_venda
        return total_vendas

    def save(self, *args, **kwargs):
        # 20177V0001
        if self.cod_venda is "":
            mes_em_curso = str(datetime.now().year) + str('%02d' % datetime.now().month)
            ultimo = '0000' if Venda.objects.last() is None else Venda.objects.order_by('pk').last().cod_venda[-4:]

            ultimo = str(int(ultimo) + 1)
            while len(str(ultimo)) < 4:
                ultimo = "0" + ultimo
            self.cod_venda = mes_em_curso + "V" + str(ultimo)

        self.valor_final = self.valor_venda - self.desconto

        # se venda for a vista, lanca-se uma entrada com os dados da venda
        if not self.comanda:
            if self.tipo == 1:
                movimentacao = Movimentacao.objects.get_or_create(fonte_destino=self.cod_venda)[0]
                movimentacao.valor = self.valor_final
                movimentacao.link = self.get_absolute_url()
                movimentacao.tipo_id = 4
                movimentacao.user_id = 1
                movimentacao.data = self.data_venda
                movimentacao.save()

            # se Pagamento for em Debito (3) ou Credito (4)
            if self.tipo == 3 or self.tipo == 4:

                movimentacao = Movimentacao.objects.get_or_create(fonte_destino=self.cod_venda)[0]
                movimentacao.valor = self.valor_final
                movimentacao.link = self.get_absolute_url()
                movimentacao.tipo_id = 3
                movimentacao.user_id = 1
                movimentacao.data = self.data_venda
                movimentacao.save()

        # self.data_pagamento = datetime.today() + timedelta(days=1)

        # se Pagamento nao for setado
        elif self.tipo == '':
            self.tipo = None

        return super(Venda, self).save(*args, **kwargs)


class ItensVenda(models.Model):

    cod_item = models.CharField(max_length=10, blank=True, )
    cod_venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    cod_servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    desconto = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'itens'

    def __str__(self):
        return self.cod_item

    def save(self, *args, **kwargs):
        # 178
        if self.cod_item is "":
            ultimo = '0000' if ItensVenda.objects.last() is None else ItensVenda.objects.last().cod_item[-4:]

            ultimo = str(int(ultimo) + 1)
            while len(str(ultimo)) < 4:
                ultimo = "0" + ultimo
            self.cod_item = "IV" + ultimo

        self.valor = Servico.objects.get(pk=self.cod_servico.id).valor
        self.valor -= self.desconto

        super(ItensVenda, self).save(*args, **kwargs)
        Venda.update_valores(Venda.objects.get(pk=self.cod_venda.pk))

    def delete(self, *args, **kwargs):
        super(ItensVenda, self).delete(*args, **kwargs)
        Venda.update_valores(Venda.objects.get(pk=self.cod_venda.pk))
