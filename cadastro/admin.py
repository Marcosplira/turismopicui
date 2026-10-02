from django.conf import settings
from django.contrib import admin
from django.contrib.messages.api import MessageFailure
from django.core.mail import send_mail
from django.utils.html import format_html

from .models import Empreendimento, FotoEmpreendimento, Categoria


class FotoEmpreendimentoInline(admin.TabularInline):
    model = FotoEmpreendimento
    extra = 1
    max_num = 4
    readonly_fields = ("preview",)

    @admin.display(description="Prévia")
    def preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:4px;" />',
                obj.imagem.url,
            )
        return "—"


@admin.register(Empreendimento)
class EmpreendimentoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "mostrar_categorias",
        "zona",
        "responsavel",
        "status",
        "data_cadastro",
    )

    list_filter = (
        "categorias",
        "zona",
        "status",
        "possui_cadastur",
        "valoriza_cultura_local",
    )

    search_fields = (
        "nome",
        "responsavel",
        "proprietario__email",
        "cpf_responsavel",
        "cnpj",
        "bairro_comunidade",
        "telefone",
        "email",
    )

    list_per_page = 20
    date_hierarchy = "data_cadastro"

    readonly_fields = (
        "data_cadastro",
        "data_atualizacao",
    )

    actions = (
        "marcar_aprovados",
        "marcar_reprovados",
    )

    fieldsets = (
        (
            "Identificação",
            {
                "fields": (
                    "nome",
                    "responsavel",
                    "proprietario",
                    "categorias",
                    "cpf_responsavel",
                    "cnpj",
                ),
            },
        ),
        (
            "Localização e contato",
            {
                "fields": (
                    "zona",
                    "endereco",
                    "numero",
                    "bairro_comunidade",
                    "ponto_referencia",
                    "telefone",
                    "whatsapp",
                    "email",
                ),
            },
        ),
        (
            "Informações turísticas",
            {
                "fields": (
                    "tipo_empreendimento",
                    "descricao",
                    "historia",
                    "numero_quartos",
                    "numero_leitos",
                    "quarto_acessibilidade",
                    "cafe_incluso",
                    "possui_garagem",
                    "valor_diarias",
                    "dias_funcionamento",
                    "horario_funcionamento",
                    "possui_cadastur",
                    "numero_cadastur",
                ),
            },
        ),
        (
            "Cultura e acessibilidade",
            {
                "fields": (
                    "possui_sicab",
                    "possui_caf",
                    "possui_estacionamento",
                    "atende_agendamento",
                    "valoriza_cultura_local",
                    "como_valoriza_cultura",
                    "sustentabilidade",
                    "acessibilidade",
                    "praticas_sustentabilidade",
                ),
            },
        ),
        (
            "Moderação",
            {
                "fields": (
                    "deseja_selo_turismo",
                    "autoriza_divulgacao",
                    "status",
                    "observacoes",
                    "data_cadastro",
                    "data_atualizacao",
                ),
            },
        ),
    )

    inlines = [FotoEmpreendimentoInline]

    @admin.display(description="Categorias")
    def mostrar_categorias(self, obj):
        return ", ".join(categoria.nome for categoria in obj.categorias.all())

    def _atualizar_status(self, request, queryset, novo_status, texto_status):
        observacao = (request.POST.get("observacoes") or "").strip()
        count = 0

        for empreendimento in queryset:
            if observacao:
                base = (empreendimento.observacoes or "").strip()
                empreendimento.observacoes = (
                    f"{base}\n{observacao}" if base else observacao
                ).strip()

            empreendimento.status = novo_status
            empreendimento.save()
            count += 1

            if empreendimento.email:
                send_mail(
                    subject=f"Empreendimento {texto_status} — Turismo de Picuí",
                    message=(
                        f"Olá {empreendimento.responsavel},\n\n"
                        f"Seu empreendimento '{empreendimento.nome}' foi {texto_status.lower()} no sistema.\n"
                        f"Observações: {observacao or 'Nenhuma observação adicional.'}\n\n"
                        f"Acesse sua área para acompanhar: {request.build_absolute_uri('/cadastro/minha-area/')}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[empreendimento.email],
                    fail_silently=True,
                )

        try:
            self.message_user(
                request,
                f"{count} empreendimentos {texto_status.lower()} com sucesso.",
            )
        except MessageFailure:
            pass

    @admin.action(description="Aprovar empreendimentos selecionados")
    def marcar_aprovados(self, request, queryset):
        self._atualizar_status(request, queryset, "aprovado", "Aprovado")

    @admin.action(description="Reprovar empreendimentos selecionados")
    def marcar_reprovados(self, request, queryset):
        self._atualizar_status(request, queryset, "reprovado", "Reprovado")


@admin.register(FotoEmpreendimento)
class FotoEmpreendimentoAdmin(admin.ModelAdmin):
    list_display = (
        "empreendimento",
        "descricao",
        "data_upload",
    )

    search_fields = (
        "empreendimento__nome",
        "descricao",
    )

    ordering = ("-data_upload",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "slug",
    )

    search_fields = ("nome",)

    prepopulated_fields = {
        "slug": ("nome",),
    }

    ordering = ("nome",)
