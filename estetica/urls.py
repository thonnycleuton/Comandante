"""estetica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from accounts.views import autocomplete
from django.conf.urls import url, include
from django.contrib import admin

from atendimento.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('venda.url', namespace='vendas')),
    url(r'^painel/', home, name='painel'),
    url(r'^admin/', admin.site.urls),
    url(r'^search/', include('haystack.urls', namespace='search')),
    url(r'^autocomplete/', autocomplete, name='autocomplete'),
    url(r'^clientes/', include('cliente.url', namespace='clientes')),
    url(r'^servicos/', include('servico.url', namespace='servicos')),
    # item de vendas
    url(r'^detalhes/', include('venda.url', namespace='detalhes')),
    url(r'^contas/', include('accounts.url', namespace='contas')),
    url(r'^movimentacao/', include('fluxo.url', namespace='movimentacao')),
    url(r'^provisionado/', include('pendencias.url', namespace='provisionado')),
    # url(r'^fornecedores/', fornecedores, name='fornecedores'),
    # url(r'^produtos/', produtos, name='produtos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)