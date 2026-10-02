from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cadastro", "0009_empreendimento_outro_segmento"),
    ]

    operations = [
        migrations.AlterField(
            model_name="empreendimento",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
