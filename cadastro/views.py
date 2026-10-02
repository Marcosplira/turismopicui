import qrcode
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Empreendimento, FotoEmpreendimento, Categoria
from .forms import EmpreendimentoForm


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

    empreendimentos = (
        Empreendimento.objects
        .filter(status="aprovado")
        .prefetch_related("fotos", "categorias")
    )

    if busca:
        empreendimentos = empreendimentos.filter(
            Q(nome__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(bairro_comunidade__icontains=busca)
        )

    if categoria_selecionada:
        empreendimentos = empreendimentos.filter(
            categorias__slug=categoria_selecionada
        )

    if zona_selecionada:
        empreendimentos = empreendimentos.filter(
            zona=zona_selecionada
        )

    empreendimentos = empreendimentos.distinct().order_by("nome")

    categorias = (
        Categoria.objects
        .all()
        .order_by("nome")
    )

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
        Categoria.objects.annotate(total=Count("empreendimentos"))
        .order_by("-total", "nome")[:6]
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
        alertas.append({
            "titulo": "Cadastros pendentes",
            "descricao": f"{pendentes} empreendimento(s) aguardando revisão da equipe.",
            "tipo": "warning",
        })

    sem_categoria = Empreendimento.objects.filter(categorias__isnull=True).distinct().count()
    if sem_categoria:
        alertas.append({
            "titulo": "Sem categoria",
            "descricao": f"{sem_categoria} empreendimento(s) ainda não foram classificados.",
            "tipo": "info",
        })

    sem_fotos = Empreendimento.objects.annotate(total_fotos=Count("fotos")).filter(total_fotos=0).count()
    if sem_fotos:
        alertas.append({
            "titulo": "Falta de fotos",
            "descricao": f"{sem_fotos} empreendimento(s) ainda não possuem imagens publicadas.",
            "tipo": "danger",
        })

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
    if request.user.is_authenticated:
        meus = Empreendimento.objects.filter(proprietario=request.user).order_by(
            "-data_cadastro"
        )
    else:
        ultimo_id = request.session.get("ultimo_empreendimento_id")
        if ultimo_id:
            meus = Empreendimento.objects.filter(pk=ultimo_id).order_by("-data_cadastro")
        else:
            meus = Empreendimento.objects.none()

    return render(request, "cadastro/minha_area.html", {"meus_empreendimentos": meus})


def _resposta_chatbot(mensagem):
    texto = (mensagem or "").strip().lower()
    if not texto:
        return "Olá! Posso te ajudar com cadastro, guia turístico, status de aprovação ou informações do município."

    if any(p in texto for p in ["como cadastrar", "cadastrar", "cadastro", "inscrever", "empree"]):
        return "Para cadastrar um empreendimento, acesse a página de cadastro no menu principal, preencha os dados do negócio e envie o formulário. Depois, o pedido entra em análise e você pode acompanhar o status na sua área pessoal."

    if any(p in texto for p in ["status", "aprovado", "pendente", "reprovado", "analise", "análise"]):
        return "O status aparece na sua área pessoal após o envio do cadastro. Se estiver pendente, a equipe está avaliando o empreendimento. Aprovados entram no guia turístico e reprovados podem receber observações para ajustes."

    if any(p in texto for p in ["guia", "catálogo", "buscar", "descobrir", "atração", "hotel", "restaurante"]):
        return "O guia turístico reúne hotéis, pousadas, restaurantes, atrativos culturais e serviços da cidade. Você pode navegar por categoria ou buscar por nome, bairro ou tipo de serviço."

    if any(p in texto for p in ["contato", "telefone", "whatsapp", "falar", "ajuda"]):
        return "Você pode usar o WhatsApp do empreendimento cadastrado ou entrar em contato com a administração do sistema para esclarecer dúvidas sobre aprovação ou revisão."

    if any(p in texto for p in ["cidade", "picuí", "pocui", "local", "municipio", "turismo"]):
        return "Pocuí? Picuí é um município com forte valor cultural, turístico e gastronômico; o guia tem como objetivo divulgar empreendimentos locais e atrativos da região."

    if any(p in texto for p in ["dúvida", "olá", "oi", "bom dia", "boa tarde", "boa noite"]):
        return "Olá! Sou o assistente do Turismo de Picuí. Posso responder sobre cadastro, guia turístico, status e apoio para empreendedores locais."

    return "Posso ajudar com cadastro, guia turístico, status de análise e informações do município. Tente perguntar: 'como cadastrar?', 'qual o status do meu empreendimento?' ou 'como funciona o guia?'."


def chatbot_assistente(request):
    if request.method == "POST":
        mensagem = request.POST.get("mensagem", "")
        resposta = _resposta_chatbot(mensagem)
        return JsonResponse({"resposta": resposta})

    return render(request, "cadastro/chatbot.html")


def privacidade(request):
    return render(request, "cadastro/privacidade.html")


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
    url_destino = request.build_absolute_uri("/")
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


def cadastrar_empreendimento(request):
    if request.method == "POST":
        form = EmpreendimentoForm(request.POST, request.FILES)

        if form.is_valid():
            empreendimento = form.save(commit=False)

            if request.user.is_authenticated:
                empreendimento.proprietario = request.user

            empreendimento.save()
            form.save_m2m()
            _enviar_notificacoes_cadastro(request, empreendimento)

            fotos = request.FILES.getlist("fotos")
            for foto in fotos:
                if foto.size > 5 * 1024 * 1024:
                    messages.error(
                        request, f"Foto {foto.name} muito grande (máx. 5 MB)."
                    )
                    continue
                if not foto.name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    messages.error(
                        request, f"Formato inválido em {foto.name}. Use JPG ou PNG."
                    )
                    continue

                FotoEmpreendimento.objects.create(
                    empreendimento=empreendimento,
                    imagem=foto,
                )

            request.session["ultimo_empreendimento_id"] = empreendimento.pk
            messages.success(
                request,
                "Cadastro do empreendimento realizado com sucesso! Aguarde a avaliação.",
            )
            return redirect("cadastro_sucesso")
        else:
            messages.error(
                request,
                "Existem erros no formulário. Verifique os campos marcados abaixo.",
            )
    else:
        form = EmpreendimentoForm()

    return render(request, "cadastro/cadastrar.html", {"form": form})
