from django.db import migrations
from django.utils.text import slugify


CATEGORIAS_COMPLEMENTARES = [
    "Agência de Turismo",
    "Atrativo Religioso",
    "Bar",
    "Evento",
    "Gastronomia",
    "Guia / Condutor Local",
    "Hotel",
    "Lanchonete",
    "Mototáxi",
    "Outro",
    "Pousada",
    "Restaurante",
    "Taxista",
    "Turismo Rural",
    "Turismo de Aventura",
]


def criar_categorias_complementares(apps, schema_editor):
    categoria_model = apps.get_model("cadastro", "Categoria")
    for nome in CATEGORIAS_COMPLEMENTARES:
        categoria_model.objects.get_or_create(
            slug=slugify(nome),
            defaults={"nome": nome},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("cadastro", "0007_categorias_iniciais"),
    ]

    operations = [
        migrations.RunPython(criar_categorias_complementares, migrations.RunPython.noop),
    ]