from django.urls import path

from . import views


urlpatterns = [
    path(
        'guia/',
        views.catalogo,
        name='catalogo'
    ),

    path(
        'privacidade/',
        views.privacidade,
        name='privacidade'
    ),

    path(
        'qrcode/',
        views.qrcode_acesso,
        name='qrcode_acesso'
    ),

    path(
        '',
        views.cadastrar_empreendimento,
        name='cadastrar_empreendimento'
    ),

    path(
        'sucesso/',
        views.cadastro_sucesso,
        name='cadastro_sucesso'
    ),
]