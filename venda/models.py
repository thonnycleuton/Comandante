from __future__ import unicode_literals

from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from cliente.models import Cliente
from servico.models import Servico


class Venda(models.Model):
    cod_venda = models.CharField(max_length=10, blank=True)
    cod_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    servico = models.ManyToManyField(Servico, through='ItensVenda', through_fields=('cod_venda', 'cod_servico'), )
    data_venda = models.DateTimeField(auto_now=True)
    tipo = models.IntegerField(choices=((1, 'A vista'), (2, 'Prazo')))
    valor_venda = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'

    def __unicode__(self):
        return self.cod_venda

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


class ItensVenda(models.Model):
    cod_item = models.CharField(max_length=10, blank=True)
    cod_venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    cod_servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'itens'

    def __unicode__(self):
        return self.cod_item

    def save(self, *args, **kwargs):
        self.valor = Servico.objects.get(pk=self.cod_servico.id).valor
        super(ItensVenda, self).save(*args, **kwargs)
        Venda.update_valores(Venda.objects.get(pk=self.cod_venda.pk))

    def delete(self, *args, **kwargs):
        super(ItensVenda, self).delete(*args, **kwargs)
        Venda.update_valores(Venda.objects.get(pk=self.cod_venda.pk))