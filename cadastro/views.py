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
from .models import Empreendimento, FotoEmpreendimento, Categoria
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
    return render(
        request, "cadastro/home.html", {"destaques": destaques, "total": total}
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
        .order_by("-data_cadastro")[:8]
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

    return render(
        request,
        "cadastro/dashboard_gerente.html",
        {
            "total": total,
            "aprovados": aprovados,
            "pendentes": pendentes,
            "reprovados": reprovados,
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


def cadastro_sucesso(request):
    return render(request, "cadastro/sucesso.html")


def sair(request):
    logout(request)
    messages.success(request, "Sessão encerrada com sucesso.")
    return redirect("home")


@staff_member_required
def exportar_csv(request):
    """
    Exporta todos os empreendimentos para CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="empreendimentos_turismo_picui.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Nome', 'Responsável', 'CPF', 'CNPJ', 'Status',
        'Zona', 'Endereço', 'Bairro/Comunidade', 'Telefone', 'WhatsApp',
        'E-mail', 'Instagram', 'Facebook', 'Categorias',
        'Descrição', 'Data de Cadastro', 'Data de Atualização'
    ])

    empreendimentos = Empreendimento.objects.all().prefetch_related('categorias').order_by('-data_cadastro')

    for emp in empreendimentos:
        categorias = ', '.join([cat.nome for cat in emp.categorias.all()])
        writer.writerow([
            emp.pk,
            emp.nome,
            emp.responsavel,
            emp.cpf_responsavel,
            emp.cnpj or '',
            emp.get_status_display(),
            emp.get_zona_display(),
            emp.endereco,
            emp.bairro_comunidade,
            emp.telefone,
            emp.whatsapp or '',
            emp.email or '',
            emp.instagram or '',
            emp.facebook or '',
            categorias,
            emp.descricao,
            emp.data_cadastro.strftime('%d/%m/%Y %H:%M') if emp.data_cadastro else '',
            emp.data_atualizacao.strftime('%d/%m/%Y %H:%M') if emp.data_atualizacao else ''
        ])

    return response


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
