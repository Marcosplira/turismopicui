import logging

logger = logging.getLogger(__name__)

import qrcode
import csv
from io import BytesIO, StringIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Empreendimento, FotoEmpreendimento, Categoria, Depoimento
from .forms import EmpreendimentoForm


@require_GET
def android_assetlinks(request):
    fingerprints = [
        value.strip()
        for value in settings.ANDROID_SHA256_CERT_FINGERPRINT.split(",")
        if value.strip()
    ]
    if not fingerprints:
        return HttpResponse(status=404)

    return JsonResponse(
        [
            {
                "relation": ["delegate_permission/common.handle_all_urls"],
                "target": {
                    "namespace": "android_app",
                    "package_name": settings.ANDROID_PACKAGE_NAME,
                    "sha256_cert_fingerprints": fingerprints,
                },
            }
        ],
        safe=False,
    )


def _enviar_notificacoes_cadastro(request, empreendimento):
    admin_email = getattr(settings, "ADMIN_EMAIL", None) or settings.DEFAULT_FROM_EMAIL
    admin_url = request.build_absolute_uri("/admin/")

    admin_body = (
        "Novo cadastro de empreendimento — Turismo de Picuí\n\n"
        f"Empreendimento: {empreendimento.nome}\n"
        f"Responsável: {empreendimento.responsavel}\n"
        f"CPF: {empreendimento.cpf_responsavel}\n"
        f"Telefone: {empreendimento.telefone}\n"
        f"E-mail: {empreendimento.email or 'Não informado'}\n"
        f"Zona: {empreendimento.get_zona_display()}\n"
        f"Categorias: {', '.join(c.nome for c in empreendimento.categorias.all()) or 'Não informadas'}\n"
        f"Status: {empreendimento.get_status_display()}\n\n"
        "Um novo empreendimento foi cadastrado no sistema e aguarda análise administrativa.\n"
        f"Acesse a área administrativa: {admin_url}"
    )

    send_mail(
        subject="Novo cadastro de empreendimento — Turismo de Picuí",
        message=admin_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin_email],
        fail_silently=True,
    )

    if empreendimento.email:
        fornecedor_body = (
            "Cadastro recebido — Turismo de Picuí\n\n"
            f"Olá {empreendimento.responsavel},\n\n"
            "Seu empreendimento foi cadastrado com sucesso e está em análise pela equipe responsável.\n"
            "Você receberá novas informações após a revisão administrativa.\n\n"
            f"Empreendimento: {empreendimento.nome}\n"
            f"Status: {empreendimento.get_status_display()}\n"
            f"Acesse sua área: {request.build_absolute_uri('/cadastro/minha-area/')}"
        )
        send_mail(
            subject="Cadastro recebido — Turismo de Picuí",
            message=fornecedor_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[empreendimento.email],
            fail_silently=True,
        )


def home(request):
    destaques = Empreendimento.objects.filter(status="aprovado").order_by(
        "-data_cadastro"
    )[:6]
    total = Empreendimento.objects.filter(status="aprovado").count()
    depoimentos = Depoimento.objects.filter(ativo=True).order_by("ordem", "-data_criacao")
    return render(
        request,
        "cadastro/home.html",
        {
            "destaques": destaques,
            "total": total,
            "depoimentos": depoimentos,
        },
    )


def catalogo(request):
    busca = request.GET.get("busca", "").strip()
    categoria_selecionada = request.GET.get("categoria", "").strip()
    zona_selecionada = request.GET.get("zona", "").strip()

    empreendimentos = Empreendimento.objects.filter(status="aprovado").prefetch_related(
        "fotos", "categorias"
    )

    if busca:
        empreendimentos = empreendimentos.filter(
            Q(nome__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(bairro_comunidade__icontains=busca)
        )

    if categoria_selecionada:
        cat_lower = categoria_selecionada.lower()
        if cat_lower == "gastronomia":
            empreendimentos = empreendimentos.filter(
                Q(categorias__slug="gastronomia")
                | Q(categorias__slug__icontains="gastronomia")
                | Q(categorias__slug__icontains="restaurante")
                | Q(categorias__slug__icontains="bar")
                | Q(categorias__slug__icontains="lanchonete")
            )
        elif cat_lower == "hospedagem":
            empreendimentos = empreendimentos.filter(
                Q(categorias__slug="hospedagem")
                | Q(categorias__slug__icontains="hospedagem")
                | Q(categorias__slug__icontains="hotel")
                | Q(categorias__slug__icontains="pousada")
            )
        elif cat_lower in ("atrativo", "atrativos"):
            empreendimentos = empreendimentos.filter(
                Q(categorias__slug__icontains="atrativo")
                | Q(categorias__slug__icontains="turismo-de-aventura")
                | Q(categorias__slug__icontains="turismo-rural")
            )
        elif cat_lower in ("evento", "eventos"):
            empreendimentos = empreendimentos.filter(
                Q(categorias__slug__icontains="evento")
            )
        elif cat_lower == "artesanato":
            empreendimentos = empreendimentos.filter(
                Q(categorias__slug__icontains="artesanato")
            )
        else:
            empreendimentos = empreendimentos.filter(categorias__slug=categoria_selecionada)

    if zona_selecionada:
        empreendimentos = empreendimentos.filter(zona=zona_selecionada)

    empreendimentos = empreendimentos.distinct().order_by("nome")

    categorias = Categoria.objects.all().order_by("nome")

    return render(
        request,
        "cadastro/catalogo.html",
        {
            "empreendimentos": empreendimentos,
            "categorias": categorias,
            "busca": busca,
            "categoria_selecionada": categoria_selecionada,
            "zona_selecionada": zona_selecionada,
        },
    )


def detalhe_empreendimento(request, pk):
    """ESSA ERA A FUNÇÃO QUE FALTAVA"""
    empreendimento = get_object_or_404(Empreendimento, pk=pk)
    fotos = FotoEmpreendimento.objects.filter(empreendimento=empreendimento)

    # Se não for aprovado, só o dono ou admin pode ver
    if empreendimento.status != "aprovado":
        if (
            not request.user.is_authenticated
            or empreendimento.proprietario != request.user
        ):
            if not request.user.is_staff:
                # Se não for dono, mostra 404
                return get_object_or_404(Empreendimento, pk=pk, status="aprovado")

    relacionados = (
        Empreendimento.objects.filter(
            status="aprovado", categorias__in=empreendimento.categorias.all()
        )
        .exclude(pk=pk)
        .distinct()[:3]
    )

    return render(
        request,
        "cadastro/detalhe.html",
        {
            "empreendimento": empreendimento,
            "fotos": fotos,
            "relacionados": relacionados,
        },
    )


@staff_member_required
def dashboard_gerente(request):
    total = Empreendimento.objects.count()
    aprovados = Empreendimento.objects.filter(status="aprovado").count()
    pendentes = Empreendimento.objects.filter(status="pendente").count()
    reprovados = Empreendimento.objects.filter(status="reprovado").count()
    recentes = (
        Empreendimento.objects.select_related("proprietario")
        .prefetch_related("categorias")
        .order_by("-data_cadastro")[:50]
    )
    categoria_summary = list(
        Categoria.objects.annotate(total=Count("empreendimentos")).order_by(
            "-total", "nome"
        )[:6]
    )
    zona_summary = list(
        Empreendimento.objects.values("zona")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    for item in zona_summary:
        item["label"] = {
            "urbana": "Zona Urbana",
            "rural": "Comunidade Rural",
        }.get(item["zona"], item["zona"])

    alertas = []
    if pendentes:
        alertas.append(
            {
                "titulo": "Cadastros pendentes",
                "descricao": f"{pendentes} empreendimento(s) aguardando revisão da equipe.",
                "tipo": "warning",
            }
        )

    sem_categoria = (
        Empreendimento.objects.filter(categorias__isnull=True).distinct().count()
    )
    if sem_categoria:
        alertas.append(
            {
                "titulo": "Sem categoria",
                "descricao": f"{sem_categoria} empreendimento(s) ainda não foram classificados.",
                "tipo": "info",
            }
        )

    sem_fotos = (
        Empreendimento.objects.annotate(total_fotos=Count("fotos"))
        .filter(total_fotos=0)
        .count()
    )
    if sem_fotos:
        alertas.append(
            {
                "titulo": "Falta de fotos",
                "descricao": f"{sem_fotos} empreendimento(s) ainda não possuem imagens publicadas.",
                "tipo": "danger",
            }
        )

    taxa_aprovacao = round((aprovados / total * 100), 1) if total > 0 else 0
    com_cadastur = Empreendimento.objects.filter(possui_cadastur=True).count()

    return render(
        request,
        "cadastro/dashboard_gerente.html",
        {
            "total": total,
            "aprovados": aprovados,
            "pendentes": pendentes,
            "reprovados": reprovados,
            "taxa_aprovacao": taxa_aprovacao,
            "com_cadastur": com_cadastur,
            "recentes": recentes,
            "categoria_summary": categoria_summary,
            "zona_summary": zona_summary,
            "alertas": alertas,
        },
    )


def minha_area(request):
    ultimo_id = request.session.get("ultimo_empreendimento_id")

    if ultimo_id:
        meus = Empreendimento.objects.filter(pk=ultimo_id).order_by("-data_cadastro")
    elif request.user.is_authenticated:
        meus = Empreendimento.objects.filter(proprietario=request.user).order_by(
            "-data_cadastro"
        )
    else:
        meus = Empreendimento.objects.none()

    return render(
        request,
        "cadastro/minha_area.html",
        {"meus_empreendimentos": meus},
    )


def _resposta_chatbot(mensagem):
    texto = (mensagem or "").strip().lower()

    if not texto:
        return (
            "Olá! 👋 Sou o Assistente de Turismo de Picuí. "
            "Estou aqui para ajudar você a utilizar o aplicativo. "
            "O que você precisa saber?"
        )

    # ==========================================================
    # SAUDAÇÕES
    # ==========================================================
    if any(
        p in texto
        for p in [
            "bom dia",
            "boa tarde",
            "boa noite",
            "olá",
            "ola",
            "oi",
            "oie",
            "hey",
        ]
    ):
        if "bom dia" in texto:
            saudacao = "Bom dia! 🌞"
        elif "boa tarde" in texto:
            saudacao = "Boa tarde! 😊"
        elif "boa noite" in texto:
            saudacao = "Boa noite! 🌙"
        else:
            saudacao = "Olá! 👋"

        return (
            f"{saudacao} Seja bem-vindo ao Turismo de Picuí! "
            "Tudo bem com você? "
            "Sou o assistente virtual do aplicativo e posso ajudar com "
            "cadastro de empreendimentos, guia turístico, status do cadastro "
            "e informações sobre Picuí. "
            "O que você precisa saber sobre o aplicativo?"
        )

    # ==========================================================
    # TUDO BEM / COMO VOCÊ ESTÁ
    # ==========================================================
    if any(
        p in texto
        for p in [
            "tudo bem",
            "tudo bom",
            "como você está",
            "como vc está",
            "como vai",
        ]
    ):
        return (
            "Tudo bem por aqui! 😊 "
            "Estou pronto para ajudar você no Turismo de Picuí. "
            "Posso explicar como fazer um cadastro, consultar o status, "
            "usar o guia turístico ou conhecer melhor o município. "
            "O que você gostaria de saber?"
        )

    # ==========================================================
    # O QUE É O APLICATIVO / ASSISTENTE
    # ==========================================================
    if any(
        p in texto
        for p in [
            "o que é o aplicativo",
            "sobre o aplicativo",
            "o que você faz",
            "o que vc faz",
            "como funciona o aplicativo",
            "como funciona esse aplicativo",
            "o que posso fazer",
            "o que eu posso fazer",
        ]
    ):
        return (
            "O Turismo de Picuí é uma plataforma criada para facilitar o acesso "
            "às informações turísticas do município e ajudar na divulgação dos "
            "empreendimentos locais. 🗺️ "
            "Você pode consultar o guia turístico, conhecer estabelecimentos, "
            "cadastrar um empreendimento e acompanhar o status do cadastro."
        )

    # ==========================================================
    # CADASTRO
    # ==========================================================
    if any(
        p in texto
        for p in [
            "como cadastrar",
            "quero cadastrar",
            "fazer cadastro",
            "fazer meu cadastro",
            "cadastrar meu empreendimento",
            "cadastrar empreendimento",
            "cadastro de empreendimento",
            "inscrever",
        ]
    ):
        return (
            "Para cadastrar um empreendimento, acesse a opção "
            "\"Fazer cadastro\" no aplicativo. 📝 "
            "Preencha as informações solicitadas, envie o formulário e, "
            "se desejar, adicione as fotos do empreendimento. "
            "Depois do envio, o cadastro será analisado pela equipe responsável."
        )

    # ==========================================================
    # STATUS DO CADASTRO
    # ==========================================================
    if any(
        p in texto
        for p in [
            "status",
            "meu cadastro",
            "cadastro aprovado",
            "cadastro pendente",
            "cadastro reprovado",
            "acompanhar cadastro",
            "consultar cadastro",
        ]
    ):
        return (
            "Você pode acompanhar o status do seu cadastro na opção "
            "\"Meus dados\" ou \"Minha área\" do aplicativo. 📋 "
            "O cadastro pode aparecer como pendente, aprovado ou reprovado. "
            "Quando estiver pendente, significa que a equipe ainda está analisando."
        )

    # ==========================================================
    # GUIA TURÍSTICO
    # ==========================================================
    if any(
        p in texto
        for p in [
            "guia",
            "guia turístico",
            "guia turistico",
            "catálogo",
            "catalogo",
            "onde encontrar",
            "empreendimentos",
            "lugares",
            "estabelecimentos",
        ]
    ):
        return (
            "O Guia Turístico reúne informações dos empreendimentos "
            "cadastrados e aprovados em Picuí. 🗺️ "
            "Você pode pesquisar por nome, categoria ou zona e conhecer "
            "as opções disponíveis no município."
        )

    # ==========================================================
    # SOBRE PICUÍ
    # ==========================================================
    if any(
        p in texto
        for p in [
            "picuí",
            "picui",
            "sobre a cidade",
            "sobre o município",
            "sobre o municipio",
            "conhecer picuí",
            "conhecer picui",
            "turismo em picuí",
            "turismo em picui",
        ]
    ):
        return (
            "Picuí é um município paraibano com uma identidade cultural, "
            "histórica e gastronômica muito importante para a região. 🌵 "
            "O Turismo de Picuí busca valorizar os empreendedores locais, "
            "a cultura, os atrativos e as experiências que o município oferece."
        )

    # ==========================================================
    # GEODIVERSIDADE / GEOTURISMO / ATRATIVOS NATURAIS
    # ==========================================================
    if any(
        p in texto
        for p in [
            "geodiversidade",
            "geoturismo",
            "saco do inferninho",
            "serra do pedro",
            "cachoeira do pedro",
            "rochas",
            "vulcão",
            "vulcao",
            "basalto",
            "uepb",
            "geologia",
            "geossítio",
            "geossitio",
            "serra dos brandões",
            "trilha",
            "atrativo natural",
            "natureza",
        ]
    ):
        return (
            "Picuí possui uma geodiversidade raríssima no Brasil! 🌋⛰️ "
            "Pesquisas científicas da UEPB (V SGFNE) destacam que o município conta com os três tipos "
            "de rochas (magmáticas, metamórficas e sedimentares). "
            "Entre os principais geossítios estão:\n\n"
            "• Serra do Pedro / Cachoeira do Pedro: sítio arqueológico com pinturas rupestres, "
            "micaxistos da Formação Seridó e mirante panorâmico.\n"
            "• Saco do Inferninho: impressionante plug vulcânico de 150m de altura composto por fragmentos "
            "de basalto negro do antigo Magmatismo Macau.\n"
            "• Mirante da Serra dos Brandões: vista espetacular de 360° da caatinga e relevo do Seridó.\n\n"
            "Você pode explorar e traçar rotas para esses pontos no nosso Mapa Turístico!"
        )

    # ==========================================================
    # CONTATO / AJUDA
    # ==========================================================
    if any(
        p in texto
        for p in [
            "contato",
            "telefone",
            "whatsapp",
            "falar com alguém",
            "falar com alguem",
            "preciso de ajuda",
            "ajuda",
        ]
    ):
        return (
            "Claro! 😊 Posso ajudar você com informações sobre o aplicativo, "
            "cadastro, guia turístico e acompanhamento do cadastro. "
            "Se precisar falar diretamente com a equipe responsável, "
            "utilize os canais de contato disponibilizados no sistema."
        )

    # ==========================================================
    # AGRADECIMENTO
    # ==========================================================
    if any(
        p in texto
        for p in [
            "obrigado",
            "obrigada",
            "valeu",
            "agradeço",
            "agradecido",
        ]
    ):
        return (
            "Por nada! 😊 Fico feliz em ajudar. "
            "Se precisar de mais alguma informação sobre o Turismo de Picuí, "
            "é só perguntar."
        )

    # ==========================================================
    # DESPEDIDA
    # ==========================================================
    if any(
        p in texto
        for p in [
            "tchau",
            "até mais",
            "ate mais",
            "até logo",
            "ate logo",
            "falou",
        ]
    ):
        return (
            "Até mais! 👋 "
            "Obrigado por utilizar o Assistente de Turismo de Picuí. "
            "Quando precisar, estarei por aqui."
        )

    # ==========================================================
    # RESPOSTA PADRÃO
    # ==========================================================
    return (
        "Ainda estou aprendendo a responder essa pergunta. 😊 "
        "Mas posso ajudar você com:\n\n"
        "• Cadastro de empreendimento\n"
        "• Status do cadastro\n"
        "• Guia turístico\n"
        "• Informações sobre Picuí\n"
        "• Funcionamento do aplicativo\n\n"
        "Tente me perguntar, por exemplo: "
        "\"Como faço meu cadastro?\""
    )


def chatbot_assistente(request):
    if request.method == "POST":
        mensagem = request.POST.get("mensagem", "")
        resposta = _resposta_chatbot(mensagem)
        return JsonResponse({"resposta": resposta})

    return render(request, "cadastro/chatbot.html")


def privacidade(request):
    return render(request, "cadastro/privacidade.html")


def sobre(request):
    return render(request, "cadastro/sobre.html")


def mapa_turistico(request):
    """Página com mapa interativo de todos os empreendimentos e geossítios."""
    empreendimentos = Empreendimento.objects.filter(
        status="aprovado"
    ).prefetch_related("fotos", "categorias")

    # Coordenadas georreferenciadas e pontos científicos do V SGFNE / UEPB (2024)
    COORDENADAS_ESPECIFICAS = {
        "serra do pedro": (-6.54242, -36.39648, True, "Geossítio Arqueológico e Formação Seridó (Pesquisa UEPB)"),
        "cachoeira do pedro": (-6.54242, -36.39648, True, "Geossítio Arqueológico e Formação Seridó (Pesquisa UEPB)"),
        "saco do inferninho": (-6.36170, -36.31121, True, "Plug Vulcânico de Basalto - Magmatismo Macau (Pesquisa UEPB)"),
        "serra dos brandões": (-6.4715, -36.2980, True, "Mirante Panorâmico 360° e Ecoturismo"),
        "igreja matriz": (-6.5115, -36.3475, False, ""),
        "chero do sertão": (-6.5132, -36.3490, False, ""),
        "portal do seridó": (-6.5085, -36.3440, False, ""),
        "arte da terra": (-6.5100, -36.3460, False, ""),
        "recanto das serras": (-6.5350, -36.3200, False, ""),
        "bodega do seridó": (-6.5122, -36.3482, False, ""),
    }

    # Converter para JSON para usar no JavaScript com coordenadas geográficas de Picuí
    empreendimentos_data = []
    for emp in empreendimentos:
        nome_lower = emp.nome.lower()
        bairro_lower = emp.bairro_comunidade.lower()
        lat = None
        lng = None
        is_geossitio = False
        geologia_info = ""

        # Verificar se coincide com pontos georreferenciados específicos
        for chave, (c_lat, c_lng, c_geo, c_desc) in COORDENADAS_ESPECIFICAS.items():
            if chave in nome_lower or chave in bairro_lower:
                lat = c_lat
                lng = c_lng
                is_geossitio = c_geo
                geologia_info = c_desc
                break

        if lat is None or lng is None:
            # Deslocamento determinístico baseado na chave primária para dispersão dos pontos
            offset_lat = ((emp.pk * 7 + 3) % 17 - 8) * 0.0018
            offset_lng = ((emp.pk * 13 + 5) % 17 - 8) * 0.0018

            if emp.zona == "rural":
                base_lat = -6.4850
                base_lng = -36.3250
                lat = base_lat + offset_lat * 2.5
                lng = base_lng + offset_lng * 2.5
            else:
                base_lat = -6.5115
                base_lng = -36.3475
                lat = base_lat + offset_lat
                lng = base_lng + offset_lng

        primeira_foto = emp.fotos.first()
        foto_url = primeira_foto.imagem.url if primeira_foto else ""

        empreendimentos_data.append({
            'id': emp.pk,
            'nome': emp.nome,
            'descricao': emp.descricao[:200] if emp.descricao else '',
            'endereco': emp.endereco,
            'bairro': emp.bairro_comunidade,
            'zona': emp.get_zona_display(),
            'zona_raw': emp.zona,
            'telefone': emp.telefone,
            'whatsapp': emp.whatsapp_url,
            'categoria': emp.categorias.first().nome if emp.categorias.exists() else '',
            'foto_url': foto_url,
            'lat': round(lat, 5),
            'lng': round(lng, 5),
            'is_geossitio': is_geossitio,
            'geologia_info': geologia_info,
        })

    return render(
        request,
        "cadastro/mapa_turistico.html",
        {
            "empreendimentos": empreendimentos,
            "empreendimentos_json": empreendimentos_data,
        },
    )


def _gerar_qrcode_imagem(url_destino):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(url_destino)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def qrcode_acesso(request):
    """
    Gera a imagem do QR Code dinamicamente apontando para a home.
    """
    url_destino = "https://heyzine.com/flip-book/e975954570.html"
    return HttpResponse(_gerar_qrcode_imagem(url_destino), content_type="image/png")


def qrcode_empreendimento(request, pk):
    empreendimento = get_object_or_404(Empreendimento, pk=pk, status="aprovado")
    url_destino = request.build_absolute_uri(f"/empreendimento/{empreendimento.pk}/")
    return HttpResponse(_gerar_qrcode_imagem(url_destino), content_type="image/png")


def selo_display_balcao(request, pk):
    """
    Gera a placa de mesa / display de balcão oficial com QR Code
    e Selo de Homologação Turística da Prefeitura Municipal de Picuí.
    """
    empreendimento = get_object_or_404(Empreendimento, pk=pk)
    if empreendimento.status != "aprovado" and not request.user.is_staff:
        empreendimento = get_object_or_404(Empreendimento, pk=pk, status="aprovado")

    return render(
        request,
        "cadastro/selo_display.html",
        {"empreendimento": empreendimento},
    )


def cadastro_sucesso(request):
    return render(request, "cadastro/sucesso.html")


def sair(request):
    logout(request)
    messages.success(request, "Sessão encerrada com sucesso.")
    return redirect("home")


@staff_member_required
def exportar_csv(request):
    """
    Exporta todos os empreendimentos para CSV 100% compatível com Microsoft Excel (Windows)
    com codificação UTF-8 BOM e delimitador ponto-e-vírgula.
    """
    response = HttpResponse(content_type="text/csv; charset=utf-8-sig")
    response["Content-Disposition"] = 'attachment; filename="relatorio_turismo_picui.csv"'

    # Grava explicitamente o caractere BOM para o Excel abrir sem quebrar acentos
    response.write("\ufeff")

    writer = csv.writer(response, delimiter=";", dialect="excel")
    writer.writerow([
        "ID", "Nome do Empreendimento", "Responsável", "CPF", "CNPJ", "Status",
        "Zona", "Endereço", "Bairro / Comunidade", "Telefone", "WhatsApp",
        "E-mail", "Instagram", "Facebook", "Possui Cadastur", "Nº Cadastur",
        "Categorias", "Descrição", "Data de Cadastro", "Data de Atualização"
    ])

    empreendimentos = Empreendimento.objects.all().prefetch_related("categorias").order_by("-data_cadastro")

    for emp in empreendimentos:
        categorias = ", ".join([cat.nome for cat in emp.categorias.all()])
        desc = (emp.descricao or "").replace("\r\n", " ").replace("\n", " ").strip()
        writer.writerow([
            emp.pk,
            emp.nome,
            emp.responsavel,
            emp.cpf_responsavel,
            emp.cnpj or "",
            emp.get_status_display(),
            emp.get_zona_display(),
            emp.endereco,
            emp.bairro_comunidade,
            emp.telefone,
            emp.whatsapp or "",
            emp.email or "",
            emp.instagram or "",
            emp.facebook or "",
            "Sim" if emp.possui_cadastur else "Não",
            emp.numero_cadastur or "",
            categorias,
            desc,
            emp.data_cadastro.strftime("%d/%m/%Y %H:%M") if emp.data_cadastro else "",
            emp.data_atualizacao.strftime("%d/%m/%Y %H:%M") if emp.data_atualizacao else ""
        ])

    return response


@staff_member_required
def relatorio_executivo(request):
    """
    Relatório Executivo Oficial pronto para impressão e exportação em PDF,
    formatado com identidade institucional para apresentação ao Prefeito / Secretário.
    """
    total = Empreendimento.objects.count()
    aprovados = Empreendimento.objects.filter(status="aprovado").count()
    pendentes = Empreendimento.objects.filter(status="pendente").count()
    reprovados = Empreendimento.objects.filter(status="reprovado").count()
    com_cadastur = Empreendimento.objects.filter(possui_cadastur=True).count()
    taxa_aprovacao = round((aprovados / total * 100), 1) if total > 0 else 0

    categoria_summary = list(
        Categoria.objects.annotate(total=Count("empreendimentos")).order_by("-total", "nome")
    )
    zona_summary = list(
        Empreendimento.objects.values("zona").annotate(total=Count("id")).order_by("-total")
    )
    for item in zona_summary:
        item["label"] = {"urbana": "Zona Urbana", "rural": "Comunidade Rural"}.get(item["zona"], item["zona"])

    empreendimentos = Empreendimento.objects.prefetch_related("categorias").order_by("-data_cadastro")

    return render(
        request,
        "cadastro/relatorio_executivo.html",
        {
            "total": total,
            "aprovados": aprovados,
            "pendentes": pendentes,
            "reprovados": reprovados,
            "com_cadastur": com_cadastur,
            "taxa_aprovacao": taxa_aprovacao,
            "categoria_summary": categoria_summary,
            "zona_summary": zona_summary,
            "empreendimentos": empreendimentos,
        },
    )


@staff_member_required
def aprovar_empreendimento_rapido(request, pk):
    """Aprova diretamente um empreendimento a partir do Dashboard do Gerente."""
    emp = get_object_or_404(Empreendimento, pk=pk)
    emp.status = "aprovado"
    emp.save(update_fields=["status", "data_atualizacao"])
    msg = f"Empreendimento '{emp.nome}' aprovado com sucesso e publicado no Guia!"
    messages.success(request, msg)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("format") == "json":
        aprovados = Empreendimento.objects.filter(status="aprovado").count()
        pendentes = Empreendimento.objects.filter(status="pendente").count()
        reprovados = Empreendimento.objects.filter(status="reprovado").count()
        total = Empreendimento.objects.count()
        taxa = round((aprovados / total * 100), 1) if total > 0 else 0
        return JsonResponse({
            "status": "success",
            "message": msg,
            "novo_status": "aprovado",
            "emp_id": emp.pk,
            "emp_nome": emp.nome,
            "aprovados": aprovados,
            "pendentes": pendentes,
            "reprovados": reprovados,
            "total": total,
            "taxa_aprovacao": taxa,
        })
    return redirect("dashboard_gerente")


@staff_member_required
def reprovar_empreendimento_rapido(request, pk):
    """Reprova diretamente um empreendimento a partir do Dashboard do Gerente."""
    emp = get_object_or_404(Empreendimento, pk=pk)
    emp.status = "reprovado"
    emp.save(update_fields=["status", "data_atualizacao"])
    msg = f"Empreendimento '{emp.nome}' marcado como reprovado."
    messages.warning(request, msg)

    if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.GET.get("format") == "json":
        aprovados = Empreendimento.objects.filter(status="aprovado").count()
        pendentes = Empreendimento.objects.filter(status="pendente").count()
        reprovados = Empreendimento.objects.filter(status="reprovado").count()
        total = Empreendimento.objects.count()
        taxa = round((aprovados / total * 100), 1) if total > 0 else 0
        return JsonResponse({
            "status": "success",
            "message": msg,
            "novo_status": "reprovado",
            "emp_id": emp.pk,
            "emp_nome": emp.nome,
            "aprovados": aprovados,
            "pendentes": pendentes,
            "reprovados": reprovados,
            "total": total,
            "taxa_aprovacao": taxa,
        })
    return redirect("dashboard_gerente")


def cadastrar_empreendimento(request):
    if request.method == "POST":
        form = EmpreendimentoForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                logger.info("CADASTRO: formulário validado com sucesso.")

                empreendimento = form.save(commit=False)

                if request.user.is_authenticated:
                    empreendimento.proprietario = request.user

                logger.info("CADASTRO: salvando empreendimento no banco.")
                empreendimento.save()

                logger.info("CADASTRO: salvando categorias.")
                form.save_m2m()

                logger.info("CADASTRO: enviando notificações.")
                _enviar_notificacoes_cadastro(request, empreendimento)

                logger.info("CADASTRO: processando fotos.")
                fotos = request.FILES.getlist("fotos")

                for foto in fotos:
                    if foto.size > 5 * 1024 * 1024:
                        messages.error(
                            request,
                            f"Foto {foto.name} muito grande (máx. 5 MB).",
                        )
                        continue

                    if not foto.name.lower().endswith(
                        (".jpg", ".jpeg", ".png", ".webp")
                    ):
                        messages.error(
                            request,
                            f"Formato inválido em {foto.name}. Use JPG ou PNG.",
                        )
                        continue

                    FotoEmpreendimento.objects.create(
                        empreendimento=empreendimento,
                        imagem=foto,
                    )

                logger.info("CADASTRO: fotos processadas.")

                request.session["ultimo_empreendimento_id"] = empreendimento.pk

                messages.success(
                    request,
                    "Cadastro do empreendimento realizado com sucesso! Aguarde a avaliação.",
                )

                logger.info(
                    "CADASTRO: concluído com sucesso. ID=%s",
                    empreendimento.pk,
                )

                return redirect("cadastro_sucesso")

            except Exception:
                logger.exception("ERRO AO PROCESSAR CADASTRO DE EMPREENDIMENTO.")
                raise

        else:
            messages.error(
                request,
                "Existem erros no formulário. Verifique os campos marcados abaixo.",
            )

    else:
        form = EmpreendimentoForm()

    return render(
        request,
        "cadastro/cadastrar.html",
        {"form": form},
    )
