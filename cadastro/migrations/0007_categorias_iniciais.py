from django.db import migrations
from django.utils.text import slugify


CATEGORIAS_INICIAIS = [
    "Hospedagem",
    "Restaurante e gastronomia",
    "Artesanato",
    "Produtor cultural",
    "Guia ou condutor de turismo",
    "Atrativo natural",
    "Atrativo cultural",
    "Comércio voltado ao turismo",
    "Mototáxi e transporte turístico",
    "Eventos e serviços turísticos",
]


def criar_categorias(apps, schema_editor):
    categoria_model = apps.get_model("cadastro", "Categoria")
    for nome in CATEGORIAS_INICIAIS:
        categoria_model.objects.get_or_create(
            slug=slugify(nome),
            defaults={"nome": nome},
        )


def remover_categorias(apps, schema_editor):
    categoria_model = apps.get_model("cadastro", "Categoria")
    categoria_model.objects.filter(nome__in=CATEGORIAS_INICIAIS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("cadastro", "0006_empreendimento_autoriza_divulgacao_and_more"),
    ]

    operations = [
        migrations.RunPython(criar_categorias, remover_categorias),
    ]