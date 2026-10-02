from django.urls import path
from . import views

urlpatterns = [
    # Sessão e área do usuário
    path("sair/", views.sair, name="sair"),
    path("minha-area/", views.minha_area, name="minha_area"),
    path("dashboard-gerente/", views.dashboard_gerente, name="dashboard_gerente"),
    path("chatbot/", views.chatbot_assistente, name="chatbot_assistente"),
    # Catálogo público
    path("guia/", views.catalogo, name="catalogo"),
    path("empreendimento/<int:pk>/", views.detalhe_empreendimento, name="detalhe_empreendimento"),
    path("empreendimento/<int:pk>/qrcode/", views.qrcode_empreendimento, name="qrcode_empreendimento"),
    # Privacidade e QR Code
    path("privacidade/", views.privacidade, name="privacidade"),
    path("qrcode/", views.qrcode_acesso, name="qrcode_acesso"),
    # Cadastro de empreendimentos
    path("", views.home, name="home"),  # ✅ agora a home é a raiz
    path("cadastro/", views.cadastrar_empreendimento, name="cadastrar_empreendimento"),
    path("sucesso/", views.cadastro_sucesso, name="cadastro_sucesso"),
]
