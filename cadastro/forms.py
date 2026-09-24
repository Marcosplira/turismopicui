from django import forms
from .models import Empreendimento

SIM_NAO_CHOICES = [
    (True, "Sim"),
    (False, "Não"),
]

class EmpreendimentoForm(forms.ModelForm):

    # ==========================================
    # CONSENTIMENTO
    # ==========================================
    consentimento = forms.BooleanField(
        required=True,
        label="Li e aceito o aviso de privacidade.",
    )

    # ==========================================
    # CAMPOS BOOLEANOS (SIM / NÃO)
    # Convertidos para TypedChoiceField para aceitarem False corretamente
    # ==========================================
    possui_cadastur = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Possui CADASTUR?",
    )
    possui_sicab = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="É cadastrado no SICAB?",
    )
    possui_caf = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Possui CAF?",
    )
    quarto_acessibilidade = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Quarto com acessibilidade?",
    )
    cafe_incluso = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Café incluso?",
    )
    possui_garagem = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Possui garagem?",
    )
    atende_agendamento = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Atende mediante agendamento?",
    )
    possui_estacionamento = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Possui estacionamento?",
    )
    valoriza_cultura_local = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Valoriza a cultura local?",
    )
    deseja_selo_turismo = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Deseja participar da avaliação para o Selo Municipal do Turismo?",
    )
    autoriza_divulgacao = forms.TypedChoiceField(
        coerce=lambda x: str(x).lower() in ['true', '1'],
        choices=SIM_NAO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label="Autoriza o uso das informações para divulgação institucional?",
    )

    class Meta:
        model = Empreendimento

        fields = [
            "nome",
            "responsavel",
            "categorias",
            "cpf_responsavel",
            "cnpj",
            "possui_cadastur",
            "numero_cadastur",
            "possui_sicab",
            "possui_caf",
            "zona",
            "endereco",
            "bairro_comunidade",
            "ponto_referencia",
            "numero",
            "telefone",
            "whatsapp",
            "email",
            "instagram",
            "facebook",
            "outras_redes",
            "tipo_empreendimento",
            "outro_segmento",
            "numero_quartos",
            "numero_leitos",
            "quarto_acessibilidade",
            "cafe_incluso",
            "possui_garagem",
            "valor_diarias",
            "descricao",
            "historia",
            "dias_funcionamento",
            "horario_funcionamento",
            "atende_agendamento",
            "possui_estacionamento",
            "valoriza_cultura_local",
            "como_valoriza_cultura",
            "sustentabilidade",
            "acessibilidade",
            "praticas_sustentabilidade",
            "deseja_selo_turismo",
            "autoriza_divulgacao",
        ]

        widgets = {
            # ==========================================
            # IDENTIFICAÇÃO
            # ==========================================
            "nome": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Nome do empreendimento",
                }
            ),
            "responsavel": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Nome completo do responsável",
                }
            ),
            "categorias": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "categoria-checkbox",
                }
            ),
            "cpf_responsavel": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "000.000.000-00",
                    "maxlength": "14",
                }
            ),
            "cnpj": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "00.000.000/0000-00",
                    "maxlength": "18",
                }
            ),
            # ==========================================
            # CADASTUR & OUTROS
            # ==========================================
            "numero_cadastur": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Número do CADASTUR",
                }
            ),
            # ==========================================
            # LOCALIZAÇÃO
            # ==========================================
            "zona": forms.Select(
                attrs={
                    "class": "field-input bg-white",
                }
            ),
            "endereco": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Rua, sítio, estrada ou localização",
                }
            ),
            "bairro_comunidade": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Bairro ou comunidade rural",
                }
            ),
            "ponto_referencia": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Ex.: próximo à igreja, praça, escola...",
                }
            ),
            "numero": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Número",
                }
            ),
            # ==========================================
            # CONTATO
            # ==========================================
            "telefone": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "(83) 99999-9999",
                }
            ),
            "whatsapp": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "(83) 99999-9999",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "exemplo@email.com",
                }
            ),
            "instagram": forms.URLInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "https://instagram.com/...",
                }
            ),
            "facebook": forms.URLInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "https://facebook.com/...",
                }
            ),
            "outras_redes": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "TikTok, YouTube, site ou outra rede",
                }
            ),
            # ==========================================
            # TIPO DE EMPREENDIMENTO
            # ==========================================
            "tipo_empreendimento": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Ex.: restaurante, pousada, artesanato...",
                }
            ),
            "outro_segmento": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Informe qual é o outro segmento",
                }
            ),
            # ==========================================
            # HOSPEDAGEM
            # ==========================================
            "numero_quartos": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Ex.: 5 quartos, sendo 3 duplos e 2 triplos",
                }
            ),
            "numero_leitos": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Ex.: 15 leitos",
                }
            ),
            "valor_diarias": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": "Informe os valores das diárias por tipo de quarto.",
                }
            ),
            # ==========================================
            # DESCRIÇÃO
            # ==========================================
            "descricao": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 5,
                    "placeholder": "Descreva o empreendimento, os serviços oferecidos e seus principais diferenciais.",
                }
            ),
            "historia": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 5,
                    "placeholder": "Conte um pouco da história do empreendimento.",
                }
            ),
            # ==========================================
            # FUNCIONAMENTO
            # ==========================================
            "dias_funcionamento": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Ex.: Segunda a sábado",
                }
            ),
            "horario_funcionamento": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Ex.: 08h às 18h",
                }
            ),
            # ==========================================
            # CULTURA, SUSTENTABILIDADE E ACESSIBILIDADE
            # ==========================================
            "como_valoriza_cultura": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": "Explique como o empreendimento valoriza a cultura local.",
                }
            ),
            "sustentabilidade": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": "Informe ações de sustentabilidade, preservação ambiental ou uso consciente dos recursos.",
                }
            ),
            "praticas_sustentabilidade": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": "Descreva práticas de sustentabilidade e ESG realizadas pelo empreendimento.",
                }
            ),
            "acessibilidade": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": "Informe recursos ou condições de acessibilidade disponíveis.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ==========================================
        # IDENTIFICA A CATEGORIA "OUTRO"
        # ==========================================
        self.outro_categoria_id = (
            self.fields["categorias"]
            .queryset.filter(slug="outro")
            .values_list("id", flat=True)
            .first()
        )

        # ==========================================
        # ZONA
        # ==========================================
        self.fields["zona"].choices = [("", "Selecione a zona")] + list(
            self.fields["zona"].choices
        )

        # ==========================================
        # EVITA MARCAR "NÃO" AUTOMATICAMENTE QUANDO NOVO FORMULÁRIO
        # ==========================================
        if not self.is_bound:
            self.fields["possui_cadastur"].initial = None
            self.fields["atende_agendamento"].initial = None
            self.fields["valoriza_cultura_local"].initial = None