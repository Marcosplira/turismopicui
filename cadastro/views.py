from io import BytesIO
from urllib.parse import quote_plus

import qrcode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import EmpreendimentoForm
from .models import Categoria, Empreendimento, FotoEmpreendimento


def home(request):
    return render(request, "cadastro/home.html")


def privacidade(request):
    return render(request, "cadastro/privacidade.html")


def catalogo(request):
    empreendimentos = (
        Empreendimento.objects.filter(status="aprovado")
        .prefetch_related("categorias", "fotos")
        .order_by("nome")
    )
    busca = request.GET.get("busca", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    zona = request.GET.get("zona", "").strip()

    if busca:
        empreendimentos = empreendimentos.filter(
            Q(nome__icontains=busca)
            | Q(tipo_empreendimento__icontains=busca)
            | Q(bairro_comunidade__icontains=busca)
            | Q(descricao__icontains=busca)
        ).distinct()
    if categoria:
        empreendimentos = empreendimentos.filter(categorias__slug=categoria)
    if zona:
        empreendimentos = empreendimentos.filter(zona=zona)

    for empreendimento in empreendimentos:
        telefone = empreendimento.whatsapp or empreendimento.telefone
        numeros = "".join(char for char in telefone if char.isdigit())
        if numeros and not numeros.startswith("55"):
            numeros = f"55{numeros}"
        empreendimento.whatsapp_url = (
            f"https://wa.me/{numeros}" if numeros else ""
        )
        endereco = ", ".join(
            part
            for part in (
                empreendimento.endereco,
                empreendimento.bairro_comunidade,
                "Picuí, PB",
            )
            if part
        )
        empreendimento.mapa_url = (
            "https://www.google.com/maps/search/?api=1&query="
            f"{quote_plus(endereco)}"
        )

    return render(
        request,
        "cadastro/catalogo.html",
        {
            "empreendimentos": empreendimentos,
            "categorias": Categoria.objects.order_by("nome"),
            "busca": busca,
            "categoria_selecionada": categoria,
            "zona_selecionada": zona,
        },
    )


def qrcode_acesso(request):
    destino = request.GET.get("destino", "home")
    caminho = "/cadastro/" if destino == "cadastro" else "/"
    url = request.build_absolute_uri(caminho)

    imagem = qrcode.make(url)
    arquivo = BytesIO()
    imagem.save(arquivo, format="PNG")

    return HttpResponse(arquivo.getvalue(), content_type="image/png")


def cadastrar_empreendimento(request):

    if request.method == "POST":

        form = EmpreendimentoForm(request.POST, request.FILES)

        # Pega todas as fotos enviadas
        fotos = request.FILES.getlist("fotos")

        # ==========================================
        # VALIDAÇÃO DAS FOTOS
        # ==========================================

        fotos_invalidas = [
            foto
            for foto in fotos
            if foto.content_type not in {"image/jpeg", "image/png"}
            or foto.size > 5 * 1024 * 1024
        ]

        if len(fotos) > 4:

            messages.error(request, "Você pode enviar no máximo 4 fotos.")

        elif fotos_invalidas:

            messages.error(
                request,
                "Cada foto deve ser JPG ou PNG e ter no máximo 5 MB.",
            )

        # ==========================================
        # VALIDAÇÃO DO FORMULÁRIO
        # ==========================================

        elif form.is_valid():

            try:

                email = form.cleaned_data["email"].lower()
                if User.objects.filter(username=email).exists():
                    form.add_error(
                        "email",
                        "Este e-mail já possui acesso. Use outro e-mail "
                        "ou entre no painel.",
                    )
                    raise ValueError("E-mail já cadastrado")

                with transaction.atomic():

                    usuario = User.objects.create_user(
                        username=email,
                        email=email,
                        password=form.cleaned_data["senha_acesso"],
                        first_name=form.cleaned_data["responsavel"],
                    )

                    # Salva o empreendimento
                    empreendimento = form.save()
                    empreendimento.proprietario = usuario
                    empreendimento.save(update_fields=["proprietario"])

                    # Salva cada foto
                    for foto in fotos:

                        FotoEmpreendimento.objects.create(
                            empreendimento=empreendimento, imagem=foto
                        )

                if empreendimento.email:
                    send_mail(
                        subject="Cadastro recebido - Turismo de Picuí",
                        message=(
                            f"Olá, {empreendimento.responsavel}.\n\n"
                            "Recebemos o cadastro do empreendimento "
                            f"{empreendimento.nome}. A equipe do Turismo de "
                            "Picuí "
                            "irá analisar as informações enviadas."
                        ),
                        from_email=None,
                        recipient_list=[empreendimento.email],
                        fail_silently=True,
                    )

                messages.success(
                    request,
                    "Cadastro enviado com sucesso! "
                    "A Prefeitura irá analisar as informações.",
                )

                return redirect("cadastro_sucesso")

            except ValueError:

                messages.error(request, "Confira o e-mail informado.")

            except Exception:

                messages.error(
                    request,
                    "Ocorreu um erro ao salvar o cadastro. Tente novamente.",
                )

        else:

            messages.error(
                request,
                "Corrija os erros indicados no formulário.",
            )

    else:

        form = EmpreendimentoForm()

    return render(
        request,
        "cadastro/cadastrar.html",
        {
            "form": form,
        },
    )


def cadastro_sucesso(request):

    return render(request, "cadastro/sucesso.html")


def entrar(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        senha = request.POST.get("senha", "")
        usuario = authenticate(request, username=email, password=senha)
        if usuario is not None:
            login(request, usuario)
            return redirect("minha_area")
        messages.error(request, "E-mail ou senha inválidos.")
    return render(request, "cadastro/entrar.html")


def sair(request):
    logout(request)
    return redirect("entrar")


@login_required
def minha_area(request):
    empreendimentos = request.user.empreendimentos.prefetch_related(
        "categorias", "fotos"
    )
    return render(
        request,
        "cadastro/minha_area.html",
        {"empreendimentos": empreendimentos},
    )
