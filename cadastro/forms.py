from django import forms

from .models import Empreendimento


class EmpreendimentoForm(forms.ModelForm):

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
            "zona",
            "endereco",
            "bairro_comunidade",
            "ponto_referencia",
            "telefone",
            "whatsapp",
            "email",
            "instagram",
            "facebook",
            "outras_redes",
            "descricao",
            "historia",
            "dias_funcionamento",
            "horario_funcionamento",
            "atende_agendamento",
            "valoriza_cultura_local",
            "como_valoriza_cultura",
            "sustentabilidade",
            "acessibilidade",
        ]

        widgets = {
            # ==================================================
            # IDENTIFICAÇÃO
            # ==================================================
            "nome": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "Nome do empreendimento",
                }
            ),
            "responsavel": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "Nome do responsável",
                }
            ),
            "categorias": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "space-y-2",
                }
            ),
            "cpf_responsavel": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "000.000.000-00",
                    "maxlength": "14",
                }
            ),
            "cnpj": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "00.000.000/0000-00",
                    "maxlength": "18",
                }
            ),
            # ==================================================
            # CADASTUR
            # ==================================================
            "possui_cadastur": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "numero_cadastur": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "Número do Cadastur",
                }
            ),
            # ==================================================
            # LOCALIZAÇÃO
            # ==================================================
            "zona": forms.Select(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 bg-white focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    )
                }
            ),
            "endereco": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "Rua, número ou localização",
                }
            ),
            "bairro_comunidade": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "Bairro ou comunidade rural",
                }
            ),
            "ponto_referencia": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "Ponto de referência",
                }
            ),
            # ==================================================
            # CONTATO
            # ==================================================
            "telefone": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "(83) 00000-0000",
                }
            ),
            "whatsapp": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "(83) 00000-0000",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "email@exemplo.com",
                }
            ),
            "instagram": forms.URLInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "https://instagram.com/...",
                }
            ),
            "facebook": forms.URLInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "https://facebook.com/...",
                }
            ),
            "outras_redes": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": "TikTok, YouTube ou outra rede",
                }
            ),
            # ==================================================
            # INFORMAÇÕES DO EMPREENDIMENTO
            # ==================================================
            "descricao": forms.Textarea(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "rows": 5,
                    "placeholder": (
                        "Descreva o empreendimento, os serviços "
                        "oferecidos e seus principais diferenciais."
                    ),
                }
            ),
            "historia": forms.Textarea(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "rows": 5,
                    "placeholder": ("Conte um pouco da história do empreendimento."),
                }
            ),
            "dias_funcionamento": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": ("Ex.: Segunda a sábado"),
                }
            ),
            "horario_funcionamento": forms.TextInput(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "placeholder": ("Ex.: 08h às 18h"),
                }
            ),
            # ==================================================
            # AGENDAMENTO
            # ==================================================
            "atende_agendamento": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            # ==================================================
            # CULTURA LOCAL
            # ==================================================
            "valoriza_cultura_local": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "como_valoriza_cultura": forms.Textarea(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "rows": 4,
                    "placeholder": (
                        "Explique como o empreendimento valoriza " "a cultura local."
                    ),
                }
            ),
            # ==================================================
            # SUSTENTABILIDADE
            # ==================================================
            "sustentabilidade": forms.Textarea(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "rows": 4,
                    "placeholder": (
                        "Informe ações de sustentabilidade, "
                        "preservação ambiental ou uso consciente "
                        "dos recursos."
                    ),
                }
            ),
            # ==================================================
            # ACESSIBILIDADE
            # ==================================================
            "acessibilidade": forms.Textarea(
                attrs={
                    "class": (
                        "w-full border border-gray-300 rounded-lg "
                        "p-3 focus:ring-2 focus:ring-green-600 "
                        "focus:border-green-600"
                    ),
                    "rows": 4,
                    "placeholder": (
                        "Informe recursos ou condições de "
                        "acessibilidade disponíveis."
                    ),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ==================================================
        # OBRIGA O USUÁRIO A ESCOLHER SIM OU NÃO
        # ==================================================

        self.fields["possui_cadastur"].required = True
        self.fields["atende_agendamento"].required = True
        self.fields["valoriza_cultura_local"].required = True

        # ==================================================
        # EVITA QUE OS CAMPOS BOOLEANOS VENHAM MARCADOS
        # AUTOMATICAMENTE COMO "NÃO"
        # ==================================================

        if not self.is_bound:
            self.fields["possui_cadastur"].initial = None
            self.fields["atende_agendamento"].initial = None
            self.fields["valoriza_cultura_local"].initial = None

        # ==================================================
        # LABELS
        # ==================================================

        self.fields["nome"].label = "Nome do empreendimento"
        self.fields["responsavel"].label = "Responsável"
        self.fields["categorias"].label = "Categoria(s)"
        self.fields["cpf_responsavel"].label = "CPF do responsável"
        self.fields["cnpj"].label = "CNPJ"
        self.fields["possui_cadastur"].label = "Possui Cadastur?"
        self.fields["numero_cadastur"].label = "Número do Cadastur"
        self.fields["zona"].label = "Localização"
        self.fields["endereco"].label = "Endereço"
        self.fields["bairro_comunidade"].label = "Bairro ou comunidade"
        self.fields["ponto_referencia"].label = "Ponto de referência"
        self.fields["telefone"].label = "Telefone"
        self.fields["whatsapp"].label = "WhatsApp"
        self.fields["email"].label = "E-mail"
        self.fields["instagram"].label = "Instagram"
        self.fields["facebook"].label = "Facebook"
        self.fields["outras_redes"].label = "Outras redes sociais"
        self.fields["descricao"].label = "Descrição do empreendimento"
        self.fields["historia"].label = "História do empreendimento"
        self.fields["dias_funcionamento"].label = "Dias de funcionamento"
        self.fields["horario_funcionamento"].label = "Horário de funcionamento"
        self.fields["atende_agendamento"].label = "Atende mediante agendamento?"
        self.fields["valoriza_cultura_local"].label = "Valoriza a cultura local?"
        self.fields["como_valoriza_cultura"].label = "Como valoriza a cultura local?"
        self.fields["sustentabilidade"].label = "Sustentabilidade"
        self.fields["acessibilidade"].label = "Acessibilidade"
