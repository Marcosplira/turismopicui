from django import forms
from .models import Empreendimento


class EmpreendimentoForm(forms.ModelForm):
    consentimento = forms.BooleanField(
        required=True,
        label="Aceito o uso dos dados para análise do cadastro.",
        error_messages={
            "required": (
                "É necessário aceitar o aviso de privacidade "
                "para enviar o cadastro."
            )
        },
    )

    class Meta:
        model = Empreendimento

        # Campos que aparecerão no formulário
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
            "numero",
            "bairro_comunidade",
            "ponto_referencia",
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
            # ==============================
            # IDENTIFICAÇÃO
            # ==============================
            "nome": forms.TextInput(
                attrs={
                    "placeholder": "Digite nome do empreendimento...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "responsavel": forms.TextInput(
                attrs={
                    "placeholder": "Digite nome do responsável...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "categorias": forms.CheckboxSelectMultiple(
                attrs={"class": "categorias-grid"}
            ),
            # ==============================
            # INFORMAÇÕES
            # ==============================
            "cpf_responsavel": forms.TextInput(
                attrs={
                    "placeholder": "000.000.000-00",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "cnpj": forms.TextInput(
                attrs={
                    "placeholder": "00.000.000/0000-00",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            # ==============================
            # CADASTUR
            # ==============================
            "possui_cadastur": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "numero_cadastur": forms.TextInput(
                attrs={
                    "placeholder": "Digite número do CADASTUR...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "possui_sicab": forms.RadioSelect(
                choices=[(True, "Sim"), (False, "Não")]
            ),
            "possui_caf": forms.RadioSelect(
                choices=[(True, "Sim"), (False, "Não")]
            ),
            # ==============================
            # LOCALIZAÇÃO
            # ==============================
            "zona": forms.Select(
                attrs={"class": "w-full border border-gray-300 rounded-lg p-3"}
            ),
            "endereco": forms.TextInput(
                attrs={
                    "placeholder": "Digite endereço completo...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "numero": forms.TextInput(attrs={"placeholder": "Número"}),
            "bairro_comunidade": forms.TextInput(
                attrs={
                    "placeholder": "Digite bairro / comunidade...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "ponto_referencia": forms.TextInput(
                attrs={
                    "placeholder": "Digite ponto de referência...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            # ==============================
            # CONTATOS
            # ==============================
            "telefone": forms.TextInput(
                attrs={
                    "placeholder": "Digite telefone...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "whatsapp": forms.TextInput(
                attrs={
                    "placeholder": "Digite WhatsApp...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Digite e-mail...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "instagram": forms.TextInput(
                attrs={
                    "placeholder": "@seuinstagram",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "facebook": forms.TextInput(
                attrs={
                    "placeholder": "Digite Facebook...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "outras_redes": forms.TextInput(
                attrs={
                    "placeholder": "Digite outras redes sociais...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "tipo_empreendimento": forms.TextInput(
                attrs={
                    "placeholder": "Ex.: pousada, restaurante, artesanato..."
                }
            ),
            "outro_segmento": forms.TextInput(
                attrs={
                    "placeholder": (
                        "Ex.: manicure, pedicure, massagista, eletricista..."
                    )
                }
            ),
            "numero_quartos": forms.TextInput(
                attrs={"placeholder": "Ex.: 2 casal, 1 solteiro"}
            ),
            "numero_leitos": forms.TextInput(
                attrs={"placeholder": "Quantidade de leitos"}
            ),
            "quarto_acessibilidade": forms.RadioSelect(
                choices=[(True, "Sim"), (False, "Não")]
            ),
            "cafe_incluso": forms.RadioSelect(
                choices=[(True, "Sim"), (False, "Não")]
            ),
            "possui_garagem": forms.RadioSelect(
                choices=[(True, "Sim"), (False, "Não")]
            ),
            "valor_diarias": forms.Textarea(
                attrs={
                    "placeholder": "Informe os valores por tipo de quarto",
                    "rows": 3,
                }
            ),
            # ==============================
            # DESCRIÇÃO
            # ==============================
            "descricao": forms.Textarea(
                attrs={
                    "placeholder": "Descreva brevemente o empreendimento...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                    "rows": 4,
                }
            ),
            "historia": forms.Textarea(
                attrs={
                    "placeholder": "Conte a história do empreendimento...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                    "rows": 4,
                }
            ),
            "dias_funcionamento": forms.TextInput(
                attrs={
                    "placeholder": "Ex.: Segunda a sábado",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "horario_funcionamento": forms.TextInput(
                attrs={
                    "placeholder": "Ex.: 08:00 às 18:00",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                }
            ),
            "possui_estacionamento": forms.RadioSelect(
                choices=[(True, "Sim"), (False, "Não")]
            ),
            # ==============================
            # AGENDAMENTO
            # ==============================
            "atende_agendamento": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            # ==============================
            # CULTURA
            # ==============================
            "valoriza_cultura_local": forms.RadioSelect(
                choices=[
                    (True, "Sim"),
                    (False, "Não"),
                ]
            ),
            "como_valoriza_cultura": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Explique como o empreendimento valoriza a "
                        "cultura local..."
                    ),
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                    "rows": 4,
                }
            ),
            # ==============================
            # SUSTENTABILIDADE
            # ==============================
            "sustentabilidade": forms.Textarea(
                attrs={
                    "placeholder": "Descreva as ações de sustentabilidade...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                    "rows": 4,
                }
            ),
            "acessibilidade": forms.Textarea(
                attrs={
                    "placeholder": "Descreva as ações de acessibilidade...",
                    "class": "w-full border border-gray-300 rounded-lg p-3",
                    "rows": 4,
                }
            ),
            "praticas_sustentabilidade": forms.Textarea(
                attrs={
                    "placeholder": "Liste as práticas ESG adotadas",
                    "rows": 4,
                }
            ),
            "deseja_selo_turismo": forms.RadioSelect(
                choices=[(True, "Sim"), (False, "Não")]
            ),
            "autoriza_divulgacao": forms.RadioSelect(
                choices=[(True, "Autorizo"), (False, "Não autorizo")]
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Deixa SIM/NÃO sem nenhuma opção marcada
        # quando o formulário é aberto pela primeira vez.
        if not self.is_bound:
            self.fields["possui_cadastur"].initial = None
            self.fields["atende_agendamento"].initial = None
            self.fields["valoriza_cultura_local"].initial = None

