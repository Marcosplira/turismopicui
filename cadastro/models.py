from django.db import models


class Categoria(models.Model):

    nome = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Empreendimento(models.Model):

    # ==========================================
    # ZONA
    # ==========================================

    ZONA_CHOICES = [
        ("urbana", "Zona Urbana"),
        ("rural", "Comunidade Rural"),
    ]

    # ==========================================
    # STATUS
    # ==========================================

    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("aprovado", "Aprovado"),
        ("reprovado", "Reprovado"),
    ]

    # ==========================================
    # IDENTIFICAÇÃO
    # ==========================================

    nome = models.CharField(max_length=200)

    responsavel = models.CharField(max_length=200)

    categorias = models.ManyToManyField(
        Categoria, blank=True, related_name="empreendimentos"
    )

    cpf_responsavel = models.CharField(max_length=14)

    cnpj = models.CharField(max_length=18, blank=True)

    # ==========================================
    # CADASTUR
    # ==========================================

    possui_cadastur = models.BooleanField(default=False)

    numero_cadastur = models.CharField(max_length=50, blank=True)

    # ==========================================
    # LOCALIZAÇÃO
    # ==========================================

    zona = models.CharField(max_length=10, choices=ZONA_CHOICES)

    endereco = models.CharField(max_length=255)

    bairro_comunidade = models.CharField(max_length=150)

    ponto_referencia = models.CharField(max_length=255, blank=True)

    # ==========================================
    # CONTATO
    # ==========================================

    telefone = models.CharField(max_length=20)

    whatsapp = models.CharField(max_length=20, blank=True)

    email = models.EmailField(blank=True)

    # ==========================================
    # REDES SOCIAIS
    # ==========================================

    instagram = models.CharField(max_length=255, blank=True)

    facebook = models.CharField(max_length=255, blank=True)

    outras_redes = models.CharField(max_length=255, blank=True)

    # ==========================================
    # DESCRIÇÃO
    # ==========================================

    descricao = models.TextField()

    historia = models.TextField(blank=True)

    # ==========================================
    # FUNCIONAMENTO
    # ==========================================

    dias_funcionamento = models.CharField(max_length=255, blank=True)

    horario_funcionamento = models.CharField(max_length=255, blank=True)

    atende_agendamento = models.BooleanField(default=False)

    # ==========================================
    # CULTURA
    # ==========================================

    valoriza_cultura_local = models.BooleanField(default=False)

    como_valoriza_cultura = models.TextField(blank=True)

    # ==========================================
    # SUSTENTABILIDADE
    # ==========================================

    sustentabilidade = models.TextField(blank=True)

    acessibilidade = models.TextField(blank=True)

    # ==========================================
    # CONTROLE
    # ==========================================

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")

    observacoes = models.TextField(blank=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class FotoEmpreendimento(models.Model):

    empreendimento = models.ForeignKey(
        Empreendimento, on_delete=models.CASCADE, related_name="fotos"
    )

    imagem = models.ImageField(upload_to="empreendimentos/")

    descricao = models.CharField(max_length=200, blank=True)

    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto de {self.empreendimento.nome}"
