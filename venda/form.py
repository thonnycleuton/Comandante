from django import forms

from servico.models import Servico
from venda.models import Venda, ItensVenda


class VendaGerenciaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user')
        super(VendaGerenciaForm, self).__init__(*args, **kwargs)
        print(self.user.groups.all())

        if self.user.groups.filter(name="Gerência"):
            servicos = Servico.objects.all()
        else:
            servicos = Servico.objects.filter(categoria__in=self.user.groups.all())

        self.fields['servico'].queryset = servicos

    class Meta:

        model = Venda
        fields = ['cod_cliente', 'servico', 'tipo', 'comanda']
        widgets = {
            'cod_cliente': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control select'}),
            'comanda': forms.CheckboxInput(attrs={'class': 'icheckbox'}),
            'servico': forms.CheckboxSelectMultiple(attrs={'class': 'icheckbox'})
        }