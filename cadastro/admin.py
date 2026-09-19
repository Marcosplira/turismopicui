from django.contrib import admin
from .models import Empreendimento, FotoEmpreendimento, Categoria


class FotoEmpreendimentoInline(admin.TabularInline):
    model = FotoEmpreendimento
    extra = 1
    max_num = 4


@admin.register(Empreendimento)
class EmpreendimentoAdmin(admin.ModelAdmin):

    list_display = (
        'nome',
        'mostrar_categorias',
        'zona',
        'responsavel',
        'status',
        'data_cadastro',
    )

    list_filter = (
        'categorias',
        'zona',
        'status',
        'possui_cadastur',
        'valoriza_cultura_local',
    )

    search_fields = (
        'nome',
        'responsavel',
        'proprietario__email',
        'cpf_responsavel',
        'cnpj',
        'bairro_comunidade',
        'telefone',
        'email',
    )

    list_per_page = 20

    date_hierarchy = 'data_cadastro'
    readonly_fields = ('data_cadastro', 'data_atualizacao')
    actions = ('marcar_aprovados', 'marcar_reprovados')

    fieldsets = (
        ('Identificação', {
            'fields': (
                'nome', 'responsavel', 'proprietario', 'categorias',
                'cpf_responsavel', 'cnpj'
            ),
        }),
        ('Localização e contato', {
            'fields': (
                'zona', 'endereco', 'numero', 'bairro_comunidade',
                'ponto_referencia',
                'telefone', 'whatsapp', 'email'
            ),
        }),
        ('Informações turísticas', {
            'fields': (
                'tipo_empreendimento', 'descricao', 'historia',
                'numero_quartos', 'numero_leitos', 'quarto_acessibilidade',
                'cafe_incluso', 'possui_garagem', 'valor_diarias',
                'dias_funcionamento',
                'horario_funcionamento', 'possui_cadastur', 'numero_cadastur'
            ),
        }),
        ('Cultura e acessibilidade', {
            'fields': (
                'possui_sicab', 'possui_caf', 'possui_estacionamento',
                'atende_agendamento', 'valoriza_cultura_local',
                'como_valoriza_cultura', 'sustentabilidade', 'acessibilidade',
                'praticas_sustentabilidade',
            ),
        }),
        ('Moderação', {
            'fields': (
                'deseja_selo_turismo', 'autoriza_divulgacao', 'status',
                'observacoes', 'data_cadastro', 'data_atualizacao'
            ),
        }),
    )

    inlines = [
        FotoEmpreendimentoInline,
    ]

    def mostrar_categorias(self, obj):
        return ", ".join(
            categoria.nome
            for categoria in obj.categorias.all()
        )

    mostrar_categorias.short_description = 'Categorias'

    @admin.action(description='Aprovar empreendimentos selecionados')
    def marcar_aprovados(self, request, queryset):
        queryset.update(status='aprovado')

    @admin.action(description='Reprovar empreendimentos selecionados')
    def marcar_reprovados(self, request, queryset):
        queryset.update(status='reprovado')


@admin.register(FotoEmpreendimento)
class FotoEmpreendimentoAdmin(admin.ModelAdmin):

    list_display = (
        'empreendimento',
        'descricao',
        'data_upload',
    )

    search_fields = (
        'empreendimento__nome',
        'descricao',
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = (
        'nome',
        'slug',
    )

    search_fields = (
        'nome',
    )
