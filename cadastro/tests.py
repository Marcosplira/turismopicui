from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Empreendimento


class CadastroPublicoTests(TestCase):
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
				"senha_acesso": "SenhaSegura123",
				"confirmar_senha": "SenhaSegura123",
				"consentimento": "on",
				"autoriza_divulgacao": "True",
			},
		)

		self.assertRedirects(resposta, reverse("cadastro_sucesso"))
		self.assertTrue(User.objects.filter(username="maria@example.com").exists())
		self.assertEqual(Empreendimento.objects.count(), 1)

	def test_area_privada_exige_login(self):
		resposta = self.client.get(reverse("minha_area"))

		self.assertRedirects(
			resposta,
			f"{reverse('entrar')}?next={reverse('minha_area')}",
		)

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
