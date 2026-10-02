from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cadastro", "0010_alter_empreendimento_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="empreendimento",
            name="facebook",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="empreendimento",
            name="instagram",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="empreendimento",
            name="outras_redes",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
