import re
from urllib.parse import quote_plus

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


cpf_validator = RegexValidator(
    r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    "CPF inválido. Use o formato 000.000.000-00."
)

cnpj_validator = RegexValidator(
    r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
    "CNPJ inválido. Use o formato 00.000.000/0000-00."
)


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Empreendimento(models.Model):
    ZONA_CHOICES = [
        ("urbana", "Zona Urbana"),
        ("rural", "Comunidade Rural"),
    ]

    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("aprovado", "Aprovado"),
        ("reprovado", "Reprovado"),
    ]

    nome = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=200)
    categorias = models.ManyToManyField(
        Categoria, blank=True, related_name="empreendimentos"
    )
    cpf_responsavel = models.CharField(max_length=14, validators=[cpf_validator])
    cnpj = models.CharField(max_length=18, blank=True, validators=[cnpj_validator])
    proprietario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="empreendimentos",
    )

    possui_cadastur = models.BooleanField(default=False)
    numero_cadastur = models.CharField(max_length=50, blank=True)
    possui_sicab = models.BooleanField(default=False)
    possui_caf = models.BooleanField(default=False)

    zona = models.CharField(max_length=10, choices=ZONA_CHOICES)
    endereco = models.CharField(max_length=255)
    bairro_comunidade = models.CharField(max_length=150)
    ponto_referencia = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=20, blank=True)

    telefone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    outras_redes = models.CharField(max_length=255, blank=True, null=True)

    @property
    def whatsapp_url(self):
        numero = self.whatsapp or self.telefone
        if not numero:
            return ""

        numero_limpo = re.sub(r"\D", "", numero)
        if len(numero_limpo) < 10:
            return ""

        if numero_limpo.startswith("55"):
            numero_final = numero_limpo
        else:
            numero_final = f"55{numero_limpo}"

        return f"https://wa.me/{numero_final}"

    @property
    def mapa_url(self):
        endereco = ", ".join(
            parte for parte in [
                self.endereco,
                self.bairro_comunidade,
                "Picuí - PB",
                "Brasil",
            ] if parte
        )
        if not endereco:
            return ""
        return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(endereco)

    tipo_empreendimento = models.CharField(max_length=255, blank=True)
    outro_segmento = models.CharField(max_length=255, blank=True)
    numero_quartos = models.CharField(max_length=100, blank=True)
    numero_leitos = models.CharField(max_length=100, blank=True)
    quarto_acessibilidade = models.BooleanField(default=False)
    cafe_incluso = models.BooleanField(default=False)
    possui_garagem = models.BooleanField(default=False)
    valor_diarias = models.TextField(blank=True)

    descricao = models.TextField()
    historia = models.TextField(blank=True)

    dias_funcionamento = models.CharField(max_length=255, blank=True)
    horario_funcionamento = models.CharField(max_length=255, blank=True)
    atende_agendamento = models.BooleanField(default=False)
    possui_estacionamento = models.BooleanField(default=False)

    valoriza_cultura_local = models.BooleanField(default=False)
    como_valoriza_cultura = models.TextField(blank=True)
    sustentabilidade = models.TextField(blank=True)
    acessibilidade = models.TextField(blank=True)
    praticas_sustentabilidade = models.TextField(blank=True)

    deseja_selo_turismo = models.BooleanField(default=False)
    autoriza_divulgacao = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendente",
    )
    observacoes = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empreendimento"
        verbose_name_plural = "Empreendimentos"
        ordering = ["-data_cadastro"]

    def __str__(self):
        return self.nome


class FotoEmpreendimento(models.Model):
    empreendimento = models.ForeignKey(
        Empreendimento, on_delete=models.CASCADE, related_name="fotos"
    )
    imagem = models.ImageField(upload_to="empreendimentos/")
    descricao = models.CharField(max_length=200, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foto do Empreendimento"
        verbose_name_plural = "Fotos dos Empreendimentos"
        ordering = ["-data_upload"]

    def __str__(self):
        return f"Foto de {self.empreendimento.nome}"
