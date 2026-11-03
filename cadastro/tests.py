import os
import smtplib
from unittest.mock import patch

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command, CommandError
from django.test import Client, RequestFactory, TestCase, override_settings
from django.urls import reverse
from io import BytesIO
from tempfile import TemporaryDirectory
from PIL import Image

from .admin import EmpreendimentoAdmin
from .models import Empreendimento, Categoria, FotoEmpreendimento

User = get_user_model()


class BootstrapAdminCommandTests(TestCase):
    def test_sem_variaveis_de_bootstrap_nao_cria_usuario(self):
        with patch.dict(os.environ, {}, clear=True):
            call_command("bootstrap_admin")

        self.assertEqual(User.objects.count(), 0)

    def test_cria_superusuario_com_credenciais_do_ambiente(self):
        with patch.dict(
            os.environ,
            {
                "DJANGO_BOOTSTRAP_ADMIN_USERNAME": "adminturismo",
                "DJANGO_BOOTSTRAP_ADMIN_EMAIL": "turismo@example.com",
                "DJANGO_BOOTSTRAP_ADMIN_PASSWORD": "Acesso-Seguro-2026!",
            },
        ):
            call_command("bootstrap_admin")

        usuario = User.objects.get(username="adminturismo")
        self.assertTrue(usuario.is_staff)
        self.assertTrue(usuario.is_superuser)
        self.assertTrue(usuario.check_password("Acesso-Seguro-2026!"))

    def test_usa_adminturismo_quando_usuario_nao_foi_configurado(self):
        with patch.dict(
            os.environ,
            {
                "DJANGO_BOOTSTRAP_ADMIN_EMAIL": "turismo@example.com",
                "DJANGO_BOOTSTRAP_ADMIN_PASSWORD": "Acesso-Seguro-2026!",
            },
            clear=True,
        ):
            call_command("bootstrap_admin")

        usuario = User.objects.get(username="adminturismo")
        self.assertTrue(usuario.is_staff)
        self.assertTrue(usuario.is_superuser)

    def test_redefine_senha_de_superusuario_existente(self):
        usuario = User.objects.create_superuser(
            "adminturismo", "turismo@example.com", "Senha-Antiga-2026!"
        )

        with patch.dict(
            os.environ,
            {
                "DJANGO_BOOTSTRAP_ADMIN_USERNAME": "adminturismo",
                "DJANGO_BOOTSTRAP_ADMIN_PASSWORD": "Acesso-Novo-2026!",
            },
        ):
            call_command("bootstrap_admin")

        usuario.refresh_from_db()
        self.assertTrue(usuario.check_password("Acesso-Novo-2026!"))

    def test_nao_promove_usuario_comum_a_administrador(self):
        User.objects.create_user("adminturismo", password="Senha-Comum-2026!")

        with patch.dict(
            os.environ,
            {
                "DJANGO_BOOTSTRAP_ADMIN_USERNAME": "adminturismo",
                "DJANGO_BOOTSTRAP_ADMIN_PASSWORD": "Acesso-Seguro-2026!",
            },
        ):
            with self.assertRaises(CommandError):
                call_command("bootstrap_admin")


class CadastroPublicoTests(TestCase):
    @override_settings(
        ANDROID_PACKAGE_NAME="com.turismopicui.guia",
        ANDROID_SHA256_CERT_FINGERPRINT="AA:BB:CC, DD:EE:FF",
    )
    def test_assetlinks_publica_pacote_e_certificados_configurados(self):
        resposta = self.client.get("/.well-known/assetlinks.json")

        self.assertEqual(resposta.status_code, 200)
        associacao = resposta.json()[0]
        self.assertEqual(
            associacao["target"]["package_name"], "com.turismopicui.guia"
        )
        self.assertEqual(
            associacao["target"]["sha256_cert_fingerprints"],
            ["AA:BB:CC", "DD:EE:FF"],
        )

    @override_settings(ANDROID_SHA256_CERT_FINGERPRINT="")
    def test_assetlinks_nao_publica_associacao_sem_certificado(self):
        resposta = self.client.get("/.well-known/assetlinks.json")

        self.assertEqual(resposta.status_code, 404)

    def test_login_admin_exibe_identidade_visual_do_turismo(self):
        resposta = self.client.get(reverse("admin:login"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Gestão do Turismo de Picuí")
        self.assertContains(resposta, "cadastro/admin.css")

    def test_home_exibe_acesso_da_equipe_e_dashboard_para_staff(self):
        resposta = self.client.get(reverse("home"))

        self.assertContains(resposta, "Acesso da equipe")
        self.assertContains(resposta, reverse("dashboard_gerente"))

        gerente = User.objects.create_user("gerente", password="senha-forte")
        gerente.is_staff = True
        gerente.save()
        self.client.force_login(gerente)

        resposta = self.client.get(reverse("home"))

        self.assertContains(resposta, "Dashboard do gerente")

    def test_home_nao_exibe_depoimentos_de_exemplo_sem_depoimentos_cadastrados(self):
        resposta = self.client.get(reverse("home"))

        self.assertEqual(resposta.status_code, 200)
        self.assertNotContains(resposta, "João Silva")
        self.assertNotContains(resposta, "Maria Alves")
        self.assertNotContains(resposta, "Pedro Costa")
        self.assertNotContains(resposta, "DEPOIMENTOS")

    def test_mapa_publico_usa_leaflet_e_serializa_dados_com_seguranca(self):
        empreendimento = Empreendimento.objects.create(
            nome='<img src=x onerror="alert(1)">',
            responsavel="Pessoa",
            cpf_responsavel="000.000.000-00",
            zona="urbana",
            endereco="Rua Principal",
            bairro_comunidade="Centro",
            telefone="83999999999",
            descricao="<script>alert(1)</script>",
            status="aprovado",
        )

        resposta = self.client.get(reverse("mapa_turistico"))
        dados = resposta.context["empreendimentos_json"]

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "leaflet@1.9.4")
        self.assertContains(resposta, "server.arcgisonline.com")
        self.assertContains(resposta, "OpenStreetMap contributors")
        self.assertNotContains(resposta, "maps.googleapis.com")
        self.assertContains(resposta, "Mirante dos Brandões")
        self.assertContains(resposta, 'id="btn-reset-map"')
        self.assertContains(resposta, "Mostrar todos os pontos")
        self.assertContains(resposta, 'data-map-point="Serra do Pedro"')
        self.assertEqual(dados[0]["id"], empreendimento.pk)
        self.assertContains(resposta, r"\u003Cimg")
        self.assertNotContains(resposta, '<img src=x onerror="alert(1)">')

    def test_formulario_nao_exibe_tags_template_como_texto(self):
        resposta = self.client.get(reverse("cadastrar_empreendimento"))

        self.assertEqual(resposta.status_code, 200)
        self.assertNotContains(resposta, "{{ form.")
        self.assertContains(resposta, 'name="fotos" id="fotos" multiple')

    def test_cadastro_salva_multiplas_fotos(self):
        arquivos = []
        for nome, formato, content_type in [
            ("fachada.jpg", "JPEG", "image/jpeg"),
            ("quarto.jpeg", "JPEG", "image/jpeg"),
            ("area.png", "PNG", "image/png"),
            ("cafe.webp", "WEBP", "image/webp"),
        ]:
            imagem = BytesIO()
            Image.new("RGB", (2, 2), color="white").save(imagem, format=formato)
            arquivos.append(
                SimpleUploadedFile(nome, imagem.getvalue(), content_type=content_type)
            )

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                resposta = self.client.post(
                    reverse("cadastrar_empreendimento"),
                    {
                        "nome": "Pousada com fotos",
                        "responsavel": "Maria Silva",
                        "cpf_responsavel": "000.000.000-00",
                        "zona": "urbana",
                        "endereco": "Rua Principal",
                        "bairro_comunidade": "Centro",
                        "telefone": "83999999999",
                        "descricao": "Hospedagem familiar.",
                        "consentimento": "on",
                        "fotos": arquivos,
                    },
                )

                self.assertRedirects(resposta, reverse("cadastro_sucesso"))
                self.assertEqual(FotoEmpreendimento.objects.count(), 4)

    def test_cadastro_rejeita_lote_de_fotos_invalido_sem_salvar_registro(self):
        imagem = BytesIO()
        Image.new("RGB", (2, 2), color="white").save(imagem, format="JPEG")
        conteudo_jpeg = imagem.getvalue()
        fotos_invalidas = [
            (
                "mais de quatro",
                [
                    SimpleUploadedFile(f"{indice}.jpg", conteudo_jpeg, content_type="image/jpeg")
                    for indice in range(5)
                ],
                "no máximo 4 fotos",
            ),
            (
                "arquivo acima do limite",
                [
                    SimpleUploadedFile(
                        "grande.jpg",
                        b"x" * (5 * 1024 * 1024 + 1),
                        content_type="image/jpeg",
                    )
                ],
                "máx. 5 MB",
            ),
            (
                "extensão incompatível",
                [
                    SimpleUploadedFile(
                        "imagem.png",
                        conteudo_jpeg,
                        content_type="image/png",
                    )
                ],
                "não corresponde ao formato",
            ),
            (
                "imagem corrompida",
                [
                    SimpleUploadedFile(
                        "corrompida.jpg",
                        b"not an image",
                        content_type="image/jpeg",
                    )
                ],
                "Não foi possível validar",
            ),
            (
                "extensão não permitida",
                [
                    SimpleUploadedFile(
                        "documento.pdf",
                        conteudo_jpeg,
                        content_type="application/pdf",
                    )
                ],
                "Formato inválido",
            ),
        ]

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                for descricao, fotos, mensagem in fotos_invalidas:
                    with self.subTest(descricao=descricao):
                        resposta = self.client.post(
                            reverse("cadastrar_empreendimento"),
                            {
                                "nome": "Cadastro com foto inválida",
                                "responsavel": "Maria Silva",
                                "cpf_responsavel": "000.000.000-00",
                                "zona": "urbana",
                                "endereco": "Rua Principal",
                                "bairro_comunidade": "Centro",
                                "telefone": "83999999999",
                                "descricao": "Hospedagem familiar.",
                                "consentimento": "on",
                                "fotos": fotos,
                            },
                        )

                        self.assertEqual(resposta.status_code, 200)
                        self.assertContains(resposta, mensagem)
                        self.assertEqual(Empreendimento.objects.count(), 0)
                        self.assertEqual(FotoEmpreendimento.objects.count(), 0)

    def test_cadastro_cria_conta_para_o_responsavel(self):
        resposta = self.client.post(
            reverse("cadastrar_empreendimento"),
            {
                "nome": "Pousada Serra",
                "responsavel": "Maria Silva",
                "cpf_responsavel": "000.000.000-00",
                "zona": "urbana",
                "endereco": "Rua Principal",
                "bairro_comunidade": "Centro",
                "telefone": "83999999999",
                "email": "maria@example.com",
                "descricao": "Hospedagem familiar.",
                "consentimento": "on",
                "autoriza_divulgacao": "True",
            },
        )

        self.assertRedirects(resposta, reverse("cadastro_sucesso"))
        self.assertEqual(Empreendimento.objects.count(), 1)
        area = self.client.get(reverse("minha_area"))
        self.assertContains(area, "Pousada Serra")

    def test_area_privada_nao_exibe_cadastro_de_outro_usuario(self):
        resposta = self.client.get(reverse("minha_area"))

        self.assertContains(resposta, "Nenhum cadastro recente")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend", ADMIN_EMAIL="admin@prefeiturapicui.gov.br")
    def test_cadastro_envia_email_para_responsavel_e_administrador(self):
        resposta = self.client.post(
            reverse("cadastrar_empreendimento"),
            {
                "nome": "Pousada do Sol",
                "responsavel": "Ana Souza",
                "cpf_responsavel": "111.222.333-44",
                "zona": "urbana",
                "endereco": "Rua das Flores",
                "bairro_comunidade": "Centro",
                "telefone": "83988887777",
                "email": "ana@example.com",
                "descricao": "Pousada familiar com café.",
                "consentimento": "on",
                "autoriza_divulgacao": "True",
            },
        )

        self.assertRedirects(resposta, reverse("cadastro_sucesso"))
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("Novo cadastro de empreendimento", mail.outbox[0].subject)
        self.assertIn("admin@prefeiturapicui.gov.br", mail.outbox[0].to)
        self.assertIn("ana@example.com", [dest for msg in mail.outbox for dest in msg.to])

    @patch("cadastro.views.send_mail", side_effect=smtplib.SMTPException("SMTP indisponível"))
    def test_falha_de_email_nao_perde_cadastro_e_avisa_usuario(self, send_mail_mock):
        with self.assertLogs("cadastro.views", level="ERROR"):
            resposta = self.client.post(
                reverse("cadastrar_empreendimento"),
                {
                    "nome": "Pousada do Sol",
                    "responsavel": "Ana Souza",
                    "cpf_responsavel": "111.222.333-44",
                    "zona": "urbana",
                    "endereco": "Rua das Flores",
                    "bairro_comunidade": "Centro",
                    "telefone": "83988887777",
                    "email": "ana@example.com",
                    "descricao": "Pousada familiar com café.",
                    "consentimento": "on",
                    "autoriza_divulgacao": "True",
                },
                follow=True,
            )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Empreendimento.objects.count(), 1)
        self.assertContains(resposta, "uma notificação por e-mail não foi enviada")
        self.assertEqual(send_mail_mock.call_count, 2)

    def test_guia_exibe_apenas_aprovados(self):
        Empreendimento.objects.create(
            nome="Local aprovado",
            responsavel="Pessoa",
            cpf_responsavel="000.000.000-00",
            zona="urbana",
            endereco="Rua A",
            bairro_comunidade="Centro",
            telefone="83999999999",
            descricao="Descricao",
            status="aprovado",
            tipo_empreendimento="Pousada",
        )
        Empreendimento.objects.create(
            nome="Local pendente",
            responsavel="Pessoa",
            cpf_responsavel="000.000.000-00",
            zona="urbana",
            endereco="Rua B",
            bairro_comunidade="Centro",
            telefone="83999999999",
            descricao="Descricao",
        )

        resposta = self.client.get(reverse("catalogo_publico"))

        self.assertContains(resposta, "Local aprovado")
        self.assertNotContains(resposta, "Local pendente")

    def test_dashboard_do_gerente_mostra_resumo_e_status(self):
        User.objects.create_superuser("admin", "admin@example.com", "123456")
        self.client.login(username="admin", password="123456")

        Empreendimento.objects.create(
            nome="Pousada A",
            responsavel="Pessoa A",
            cpf_responsavel="111.222.333-44",
            zona="urbana",
            endereco="Rua A",
            bairro_comunidade="Centro",
            telefone="83999999999",
            descricao="Descricao A",
            status="aprovado",
        )
        Empreendimento.objects.create(
            nome="Pousada B",
            responsavel="Pessoa B",
            cpf_responsavel="222.333.444-55",
            zona="urbana",
            endereco="Rua B",
            bairro_comunidade="Centro",
            telefone="83988887777",
            descricao="Descricao B",
            status="pendente",
        )
        Empreendimento.objects.create(
            nome="Pousada C",
            responsavel="Pessoa C",
            cpf_responsavel="333.444.555-66",
            zona="rural",
            endereco="Rua C",
            bairro_comunidade="Comunidad",
            telefone="83977776666",
            descricao="Descricao C",
            status="reprovado",
        )

        resposta = self.client.get(reverse("dashboard_gerente"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Dashboard do gerente")
        self.assertContains(resposta, "3")
        self.assertContains(resposta, "Aprovados")
        self.assertContains(resposta, "Pendentes")
        self.assertContains(resposta, "Reprovados")

    def test_acoes_rapidas_exigem_post_e_atualizam_status(self):
        gerente = User.objects.create_user("gerente", "gerente@example.com", "123456")
        gerente.is_staff = True
        gerente.save()
        client = Client(enforce_csrf_checks=True)
        client.force_login(gerente)
        dashboard = client.get(reverse("dashboard_gerente"))
        csrf_token = dashboard.cookies["csrftoken"].value

        empreendimento = Empreendimento.objects.create(
            nome="Pousada para revisão",
            responsavel="Pessoa",
            cpf_responsavel="111.222.333-44",
            zona="urbana",
            endereco="Rua A",
            bairro_comunidade="Centro",
            telefone="83999999999",
            descricao="Cadastro para teste.",
        )

        url_aprovar = reverse("aprovar_rapido", args=[empreendimento.pk])
        resposta = client.get(url_aprovar)

        self.assertEqual(resposta.status_code, 405)
        empreendimento.refresh_from_db()
        self.assertEqual(empreendimento.status, "pendente")

        resposta = client.post(
            url_aprovar,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resposta.status_code, 403)

        resposta = client.post(
            url_aprovar,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["novo_status"], "aprovado")
        empreendimento.refresh_from_db()
        self.assertEqual(empreendimento.status, "aprovado")

        url_reprovar = reverse("reprovar_rapido", args=[empreendimento.pk])
        resposta = client.get(url_reprovar)

        self.assertEqual(resposta.status_code, 405)
        empreendimento.refresh_from_db()
        self.assertEqual(empreendimento.status, "aprovado")

        resposta = client.post(
            url_reprovar,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["novo_status"], "reprovado")
        empreendimento.refresh_from_db()
        self.assertEqual(empreendimento.status, "reprovado")

    def test_chatbot_exibe_ajuda_para_usuario(self):
        resposta = self.client.get(reverse("chatbot_assistente"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Assistente de Turismo")
        self.assertContains(resposta, "Como cadastrar")

    def test_empreendimento_tem_pagina_detalhada_com_qrcode(self):
        empreendimento = Empreendimento.objects.create(
            nome="Pousada do Vale",
            responsavel="João da Silva",
            cpf_responsavel="444.555.666-77",
            zona="urbana",
            endereco="Rua da Paz",
            bairro_comunidade="Centro",
            telefone="83977778888",
            descricao="Pousada familiar",
            status="aprovado",
        )

        resposta = self.client.get(reverse("detalhe_empreendimento", args=[empreendimento.pk]))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Pousada do Vale")
        self.assertContains(resposta, "Código QR")

    def test_dashboard_executivo_mostra_metrica_por_categoria_e_zona(self):
        User.objects.create_superuser("admin", "admin@example.com", "123456")
        self.client.login(username="admin", password="123456")

        categoria_hospedagem = Empreendimento.objects.create(
            nome="Hotel Central",
            responsavel="Pessoa A",
            cpf_responsavel="001.002.003-04",
            zona="urbana",
            endereco="Rua A",
            bairro_comunidade="Centro",
            telefone="83911112222",
            descricao="Hotel",
            status="aprovado",
        )
        categoria_hospedagem.categorias.add(
            *[Categoria.objects.get_or_create(nome="Hospedagem", slug="hospedagem")[0]],
        )

        categoria_gastronomia = Empreendimento.objects.create(
            nome="Churrascaria do Vale",
            responsavel="Pessoa B",
            cpf_responsavel="010.020.030-40",
            zona="rural",
            endereco="Rua B",
            bairro_comunidade="Sítio",
            telefone="83933334444",
            descricao="Gastronomia",
            status="pendente",
        )
        categoria_gastronomia.categorias.add(
            *[Categoria.objects.get_or_create(nome="Gastronomia", slug="gastronomia")[0]],
        )

        resposta = self.client.get(reverse("dashboard_gerente"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Distribuição por categoria")
        self.assertContains(resposta, "Distribuição por zona")
        self.assertContains(resposta, "Hospedagem")
        self.assertContains(resposta, "Gastronomia")

    def test_dashboard_exibe_alertas_gerenciais(self):
        User.objects.create_superuser("admin", "admin@example.com", "123456")
        self.client.login(username="admin", password="123456")

        Empreendimento.objects.create(
            nome="Pousada em revisão",
            responsavel="Pessoa X",
            cpf_responsavel="111.222.333-44",
            zona="urbana",
            endereco="Rua X",
            bairro_comunidade="Centro",
            telefone="83944445555",
            descricao="Aguardando análise",
            status="pendente",
        )

        resposta = self.client.get(reverse("dashboard_gerente"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Alertas gerenciais")
        self.assertContains(resposta, "Cadastros pendentes")

    def test_admin_aprova_empreendimento_e_envia_email_com_observacao(self):
        usuario = User.objects.create_user("gerente", "gerente@example.com", "123456")
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save()
        empreendimento = Empreendimento.objects.create(
            nome="Pousada do Leste",
            responsavel="Maria Almeida",
            cpf_responsavel="777.888.999-00",
            zona="urbana",
            endereco="Rua da Praia",
            bairro_comunidade="Centro",
            telefone="83955556666",
            email="maria@example.com",
            descricao="Pousada em análise",
            status="pendente",
            proprietario=usuario,
        )

        factory = RequestFactory()
        request = factory.post(
            "/admin/cadastro/empreendimento/",
            {"observacoes": "Documentação revisada com sucesso."},
        )
        request.user = usuario
        admin_instance = EmpreendimentoAdmin(Empreendimento, admin.site)

        with self.settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"):
            admin_instance.marcar_aprovados(request, Empreendimento.objects.filter(pk=empreendimento.pk))

        empreendimento.refresh_from_db()
        self.assertEqual(empreendimento.status, "aprovado")
        self.assertIn("Documentação revisada com sucesso.", empreendimento.observacoes)
        self.assertTrue(any("Aprovado" in msg.subject for msg in mail.outbox))

    @patch("cadastro.admin.send_mail", side_effect=smtplib.SMTPException("SMTP indisponível"))
    def test_falha_email_admin_nao_reverte_aprovacao(self, send_mail_mock):
        usuario = User.objects.create_user("gerente", "gerente@example.com", "123456")
        empreendimento = Empreendimento.objects.create(
            nome="Pousada em análise",
            responsavel="Maria Almeida",
            cpf_responsavel="777.888.999-00",
            zona="urbana",
            endereco="Rua da Praia",
            bairro_comunidade="Centro",
            telefone="83955556666",
            email="maria@example.com",
            descricao="Pousada em análise",
            status="pendente",
        )
        request = RequestFactory().post("/admin/cadastro/empreendimento/")
        request.user = usuario

        with self.assertLogs("cadastro.admin", level="ERROR"):
            EmpreendimentoAdmin(Empreendimento, admin.site).marcar_aprovados(
                request, Empreendimento.objects.filter(pk=empreendimento.pk)
            )

        empreendimento.refresh_from_db()
        self.assertEqual(empreendimento.status, "aprovado")
        send_mail_mock.assert_called_once()
