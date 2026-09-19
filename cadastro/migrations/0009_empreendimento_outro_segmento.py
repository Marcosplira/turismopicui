from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cadastro", "0008_categorias_complementares"),
    ]

    operations = [
        migrations.AddField(
            model_name="empreendimento",
            name="outro_segmento",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]