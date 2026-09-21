from django import forms

from .models import Empreendimento


class EmpreendimentoForm(forms.ModelForm):

    # ==========================================
    # CONSENTIMENTO
    # ==========================================

    consentimento = forms.BooleanField(
        required=True,
        label="Li e aceito o aviso de privacidade.",
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
            # CADASTUR
            # ==========================================
            "possui_cadastur": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "numero_cadastur": forms.TextInput(
                attrs={
                    "class": "field-input",
                    "placeholder": "Número do CADASTUR",
                }
            ),
            # ==========================================
            # SICAB / CAF
            # ==========================================
            "possui_sicab": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "possui_caf": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
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
            "quarto_acessibilidade": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "cafe_incluso": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "possui_garagem": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "valor_diarias": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": (
                        "Informe os valores das diárias " "por tipo de quarto."
                    ),
                }
            ),
            # ==========================================
            # DESCRIÇÃO
            # ==========================================
            "descricao": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 5,
                    "placeholder": (
                        "Descreva o empreendimento, os serviços "
                        "oferecidos e seus principais diferenciais."
                    ),
                }
            ),
            "historia": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 5,
                    "placeholder": ("Conte um pouco da história do empreendimento."),
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
            "atende_agendamento": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "possui_estacionamento": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            # ==========================================
            # CULTURA
            # ==========================================
            "valoriza_cultura_local": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "como_valoriza_cultura": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": (
                        "Explique como o empreendimento " "valoriza a cultura local."
                    ),
                }
            ),
            # ==========================================
            # SUSTENTABILIDADE
            # ==========================================
            "sustentabilidade": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": (
                        "Informe ações de sustentabilidade, "
                        "preservação ambiental ou uso consciente "
                        "dos recursos."
                    ),
                }
            ),
            "praticas_sustentabilidade": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": (
                        "Descreva práticas de sustentabilidade "
                        "e ESG realizadas pelo empreendimento."
                    ),
                }
            ),
            # ==========================================
            # ACESSIBILIDADE
            # ==========================================
            "acessibilidade": forms.Textarea(
                attrs={
                    "class": "field-input",
                    "rows": 4,
                    "placeholder": (
                        "Informe recursos ou condições de "
                        "acessibilidade disponíveis."
                    ),
                }
            ),
            # ==========================================
            # SELO MUNICIPAL
            # ==========================================
            "deseja_selo_turismo": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "autoriza_divulgacao": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
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
        # CAMPOS SIM / NÃO OBRIGATÓRIOS
        # ==========================================

        self.fields["possui_cadastur"].required = True
        self.fields["atende_agendamento"].required = True
        self.fields["valoriza_cultura_local"].required = True

        # ==========================================
        # EVITA MARCAR "NÃO" AUTOMATICAMENTE
        # ==========================================

        if not self.is_bound:

            self.fields["possui_cadastur"].initial = None

            self.fields["atende_agendamento"].initial = None

            self.fields["valoriza_cultura_local"].initial = None

        # ==========================================
        # LABELS
        # ==========================================

        self.fields["nome"].label = "Nome do empreendimento"

        self.fields["responsavel"].label = "Responsável"

        self.fields["categorias"].label = "Categoria(s)"

        self.fields["cpf_responsavel"].label = "CPF do responsável"

        self.fields["cnpj"].label = "CNPJ"

        self.fields["possui_cadastur"].label = "Possui CADASTUR?"

        self.fields["numero_cadastur"].label = "Número do CADASTUR"

        self.fields["possui_sicab"].label = "É cadastrado no SICAB?"

        self.fields["possui_caf"].label = "Possui CAF?"

        self.fields["zona"].label = "Localização"

        self.fields["endereco"].label = "Endereço"

        self.fields["bairro_comunidade"].label = "Bairro ou comunidade"

        self.fields["ponto_referencia"].label = "Ponto de referência"

        self.fields["numero"].label = "Número"

        self.fields["telefone"].label = "Telefone"

        self.fields["whatsapp"].label = "WhatsApp"

        self.fields["email"].label = "E-mail"

        self.fields["instagram"].label = "Instagram"

        self.fields["facebook"].label = "Facebook"

        self.fields["outras_redes"].label = "Outras redes sociais"

        self.fields["tipo_empreendimento"].label = "Tipo de empreendimento"

        self.fields["outro_segmento"].label = "Outro segmento"

        self.fields["numero_quartos"].label = "Número e tipos de quartos"

        self.fields["numero_leitos"].label = "Número de leitos"

        self.fields["quarto_acessibilidade"].label = "Quarto com acessibilidade?"

        self.fields["cafe_incluso"].label = "Café incluso?"

        self.fields["possui_garagem"].label = "Possui garagem?"

        self.fields["valor_diarias"].label = "Valor das diárias"

        self.fields["descricao"].label = "Descrição do empreendimento"

        self.fields["historia"].label = "História do empreendimento"

        self.fields["dias_funcionamento"].label = "Dias de funcionamento"

        self.fields["horario_funcionamento"].label = "Horário de funcionamento"

        self.fields["atende_agendamento"].label = "Atende mediante agendamento?"

        self.fields["possui_estacionamento"].label = "Possui estacionamento?"

        self.fields["valoriza_cultura_local"].label = "Valoriza a cultura local?"

        self.fields["como_valoriza_cultura"].label = "Como valoriza a cultura local?"

        self.fields["sustentabilidade"].label = "Sustentabilidade"

        self.fields["praticas_sustentabilidade"].label = (
            "Práticas de sustentabilidade e ESG"
        )

        self.fields["acessibilidade"].label = "Acessibilidade"

        self.fields["deseja_selo_turismo"].label = (
            "Deseja participar da avaliação para o " "Selo Municipal do Turismo?"
        )

        self.fields["autoriza_divulgacao"].label = (
            "Autoriza o uso das informações para " "divulgação institucional?"
        )

        self.fields["consentimento"].label = "Li e aceito o aviso de privacidade."
