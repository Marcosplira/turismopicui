from io import BytesIO
from urllib.parse import quote_plus

import qrcode

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EmpreendimentoForm
from .models import Categoria, Empreendimento, FotoEmpreendimento

# ==========================================================
# E-MAILS DOS ADMINISTRADORES
# ==========================================================

EMAIL_ADMINISTRADORES = [
    "turismopicui@gmail.com",
    "turismo@picui.pb.gov.br",
    "marcosplira12@gmail.com",
]


# ==========================================================
# HOME
# ==========================================================


def home(request):

    return render(
        request,
        "cadastro/home.html",
    )


# ==========================================================
# PRIVACIDADE
# ==========================================================


def privacidade(request):

    return render(
        request,
        "cadastro/privacidade.html",
    )


# ==========================================================
# CATÁLOGO
# ==========================================================


def catalogo(request):

    empreendimentos = (
        Empreendimento.objects.filter(status="aprovado")
        .prefetch_related(
            "categorias",
            "fotos",
        )
        .order_by("nome")
    )

    busca = request.GET.get(
        "busca",
        "",
    ).strip()

    categoria = request.GET.get(
        "categoria",
        "",
    ).strip()

    zona = request.GET.get(
        "zona",
        "",
    ).strip()

    # ==========================================
    # BUSCA
    # ==========================================

    if busca:

        empreendimentos = empreendimentos.filter(
            Q(nome__icontains=busca)
            | Q(tipo_empreendimento__icontains=busca)
            | Q(outro_segmento__icontains=busca)
            | Q(bairro_comunidade__icontains=busca)
            | Q(descricao__icontains=busca)
        ).distinct()

    # ==========================================
    # CATEGORIA
    # ==========================================

    if categoria:

        empreendimentos = empreendimentos.filter(categorias__slug=categoria)

    # ==========================================
    # ZONA
    # ==========================================

    if zona:

        empreendimentos = empreendimentos.filter(zona=zona)

    # ==========================================
    # LINKS DE WHATSAPP E MAPA
    # ==========================================

    for empreendimento in empreendimentos:

        telefone = empreendimento.whatsapp or empreendimento.telefone

        numeros = "".join(char for char in telefone if char.isdigit())

        if numeros and not numeros.startswith("55"):

            numeros = f"55{numeros}"

        if numeros:

            empreendimento.whatsapp_url = f"https://wa.me/{numeros}"

        else:

            empreendimento.whatsapp_url = ""

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
            "https://www.google.com/maps/search/"
            "?api=1&query="
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


# ==========================================================
# QR CODE
# ==========================================================


def qrcode_acesso(request):

    destino = request.GET.get(
        "destino",
        "home",
    )

    # ==========================================
    # REVISTA
    # ==========================================

    if destino == "revista":

        url = "https://heyzine.com/" "flip-book/e975954570.html"

    # ==========================================
    # CADASTRO
    # ==========================================

    elif destino == "cadastro":

        url = "http://10.0.0.230:8001/"

    # ==========================================
    # HOME
    # ==========================================

    else:

        url = request.build_absolute_uri("/cadastro/")

    # ==========================================
    # GERA QR CODE
    # ==========================================

    imagem = qrcode.make(url)

    arquivo = BytesIO()

    imagem.save(
        arquivo,
        format="PNG",
    )

    return HttpResponse(
        arquivo.getvalue(),
        content_type="image/png",
    )


# ==========================================================
# CADASTRO DE EMPREENDIMENTO
# ==========================================================


def cadastrar_empreendimento(request):

    if request.method == "POST":

        form = EmpreendimentoForm(
            request.POST,
            request.FILES,
        )

        # ==========================================
        # FOTOS
        # ==========================================

        fotos = request.FILES.getlist("fotos")

        # ==========================================
        # VALIDA FOTOS
        # ==========================================

        fotos_invalidas = [
            foto
            for foto in fotos
            if (
                foto.content_type
                not in {
                    "image/jpeg",
                    "image/png",
                }
                or foto.size > 5 * 1024 * 1024
            )
        ]

        # ==========================================
        # MAIS DE 4 FOTOS
        # ==========================================

        if len(fotos) > 4:

            messages.error(
                request,
                "Você pode enviar no máximo 4 fotos.",
            )

        # ==========================================
        # FOTO INVÁLIDA
        # ==========================================

        elif fotos_invalidas:

            messages.error(
                request,
                ("Cada foto deve ser JPG ou PNG " "e ter no máximo 5 MB."),
            )

        # ==========================================
        # FORMULÁRIO
        # ==========================================

        elif form.is_valid():

            try:

                with transaction.atomic():

                    # ==================================
                    # SALVA EMPREENDIMENTO
                    # ==================================

                    empreendimento = form.save()

                    # ==================================
                    # SALVA FOTOS
                    # ==================================

                    for foto in fotos:

                        FotoEmpreendimento.objects.create(
                            empreendimento=empreendimento,
                            imagem=foto,
                        )

                # ======================================
                # E-MAIL PARA O RESPONSÁVEL
                # ======================================

                if empreendimento.email:

                    send_mail(
                        subject=("Cadastro recebido - " "Turismo de Picuí"),
                        message=(
                            f"Olá, "
                            f"{empreendimento.responsavel}.\n\n"
                            "Recebemos o cadastro do "
                            "empreendimento "
                            f"{empreendimento.nome}.\n\n"
                            "A equipe do Turismo de Picuí "
                            "irá analisar as informações "
                            "enviadas."
                        ),
                        from_email=None,
                        recipient_list=[empreendimento.email],
                        fail_silently=False,
                    )

                # ======================================
                # E-MAIL PARA OS ADMINISTRADORES
                # ======================================

                try:

                    # ----------------------------------
                    # CATEGORIAS
                    # ----------------------------------

                    categorias = empreendimento.categorias.all()

                    nomes_categorias = ", ".join(
                        categoria.nome for categoria in categorias
                    )

                    # ----------------------------------
                    # LINK PARA ÁREA ADMINISTRATIVA
                    # ----------------------------------

                    link_admin = request.build_absolute_uri(reverse("admin:index"))

                    # ----------------------------------
                    # MENSAGEM
                    # ----------------------------------

                    mensagem_admin = f"""
NOVO CADASTRO DE EMPREENDIMENTO
TURISMO DE PICUÍ

Um novo empreendimento foi cadastrado no sistema
e aguarda análise administrativa.

========================================
INFORMAÇÕES DO CADASTRO
========================================

Empreendimento:
{empreendimento.nome}

Responsável:
{empreendimento.responsavel}

Telefone:
{empreendimento.telefone}

WhatsApp:
{empreendimento.whatsapp or "Não informado"}

E-mail:
{empreendimento.email or "Não informado"}

Zona:
{empreendimento.get_zona_display()}

Endereço:
{empreendimento.endereco}

Bairro/Comunidade:
{empreendimento.bairro_comunidade}

Categorias:
{nomes_categorias or "Não informado"}

Status:
{empreendimento.get_status_display()}

Data do cadastro:
{empreendimento.data_cadastro.strftime("%d/%m/%Y %H:%M")}

========================================
ÁREA ADMINISTRATIVA
========================================

Acesse a área administrativa para visualizar
o cadastro completo:

{link_admin}


Turismo de Picuí
Prefeitura Municipal de Picuí
"""

                    # ----------------------------------
                    # ENVIA PARA OS 3 ADMINISTRADORES
                    # ----------------------------------

                    send_mail(
                        subject=(
                            "Novo cadastro de empreendimento " "- Turismo de Picuí"
                        ),
                        message=mensagem_admin,
                        from_email=None,
                        recipient_list=EMAIL_ADMINISTRADORES,
                        fail_silently=True,
                    )

                except Exception as erro_email_admin:

                    print(
                        "Erro ao enviar e-mail "
                        f"para administradores: {erro_email_admin}"
                    )

                # ======================================
                # MENSAGEM DE SUCESSO
                # ======================================

                messages.success(
                    request,
                    (
                        "Cadastro enviado com sucesso! "
                        "A Prefeitura irá analisar "
                        "as informações."
                    ),
                )

                # ======================================
                # GUARDA CADASTRO NA SESSÃO
                # ======================================

                request.session["empreendimento_id"] = empreendimento.id

                return redirect("cadastro_sucesso")

            except Exception:
                import traceback

                print("\n" + "=" * 70)
                print("ERRO AO SALVAR CADASTRO:")
                print(str(e))
                print("=" * 70)
                traceback.print_exc()
                print("=" * 70 + "\n")

                messages.error(
                    request,
                    (f"Erro ao salvar o cadastro: {e}"),
                )

        # ==========================================
        # ERROS DO FORMULÁRIO
        # ==========================================

        else:

            messages.error(
                request,
                ("Corrija os erros indicados " "no formulário."),
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


# ==========================================================
# SUCESSO
# ==========================================================


def cadastro_sucesso(request):

    return render(
        request,
        "cadastro/sucesso.html",
    )


# ==========================================================
# SAIR
# ==========================================================


def sair(request):

    request.session.pop(
        "empreendimento_id",
        None,
    )

    return redirect("home")


# ==========================================================
# MINHA ÁREA
# ==========================================================


def minha_area(request):

    empreendimento_id = request.session.get("empreendimento_id")

    empreendimentos = Empreendimento.objects.none()

    if empreendimento_id:

        empreendimentos = Empreendimento.objects.filter(id=empreendimento_id)

    return render(
        request,
        "cadastro/minha_area.html",
        {"empreendimentos": empreendimentos},
    )
