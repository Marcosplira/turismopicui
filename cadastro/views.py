from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from .models import Empreendimento, FotoEmpreendimento
from .forms import EmpreendimentoForm


def home(request):
    return render(request, "cadastro/home.html")


def catalogo(request):
    empreendimentos = Empreendimento.objects.filter(status="aprovado")
    return render(
        request,
        "cadastro/catalogo.html",
        {"empreendimentos": empreendimentos},
    )


def minha_area(request):
    return render(request, "cadastro/minha_area.html")


def privacidade(request):
    return render(request, "cadastro/privacidade.html")


def qrcode_acesso(request):
    return render(request, "cadastro/qrcode_acesso.html")


def cadastro_sucesso(request):
    return render(request, "cadastro/sucesso.html")


def sair(request):
    logout(request)
    messages.success(request, "Sessão encerrada com sucesso.")
    return redirect("cadastrar_empreendimento")


def cadastrar_empreendimento(request):
    if request.method == "POST":
        form = EmpreendimentoForm(request.POST)

        if form.is_valid():
            empreendimento = form.save(commit=False)

            if request.user.is_authenticated:
                empreendimento.proprietario = request.user

            empreendimento.save()
            form.save_m2m()

            fotos = request.FILES.getlist("fotos")
            for foto in fotos:
                FotoEmpreendimento.objects.create(
                    empreendimento=empreendimento,
                    imagem=foto,
                )

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

    return render(
        request,
        "cadastro/cadastrar.html",
        {"form": form},
    )
