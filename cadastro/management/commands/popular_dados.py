from django.core.management.base import BaseCommand
from cadastro.models import Categoria, Empreendimento


class Command(BaseCommand):
    help = "Popula o banco com categorias e pontos turísticos emblemáticos de Picuí-PB para demonstração"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando população de dados turísticos de Picuí...")

        # 1. Categorias Essenciais
        categorias_dados = [
            ("Gastronomia", "gastronomia"),
            ("Hospedagem", "hospedagem"),
            ("Atrativo Natural", "atrativo-natural"),
            ("Atrativo Cultural", "atrativo-cultural"),
            ("Atrativo Religioso", "atrativo-religioso"),
            ("Artesanato", "artesanato"),
            ("Turismo Rural", "turismo-rural"),
            ("Turismo de Aventura", "turismo-de-aventura"),
            ("Eventos e Serviços Turísticos", "eventos-e-servicos-turisticos"),
        ]

        cat_objs = {}
        for nome, slug in categorias_dados:
            cat, _ = Categoria.objects.get_or_create(slug=slug, defaults={"nome": nome})
            cat_objs[slug] = cat

        # 2. Empreendimentos de Destaque
        dados_empreendimentos = [
            {
                "nome": "Restaurante e Churrascaria O Chero do Sertão",
                "responsavel": "Manoel Dantas dos Santos",
                "cpf_responsavel": "111.222.333-44",
                "cnpj": "12.345.678/0001-90",
                "zona": "urbana",
                "endereco": "Rua Coronel Severino Dantas, 145",
                "bairro_comunidade": "Centro",
                "telefone": "(83) 99876-1122",
                "whatsapp": "83998761122",
                "email": "cherodosertao.picui@gmail.com",
                "instagram": "cherodosertaopicui",
                "possui_cadastur": True,
                "numero_cadastur": "15.02.04.11-PB",
                "dias_funcionamento": "Terça a Domingo",
                "horario_funcionamento": "11:00 às 22:00",
                "possui_estacionamento": True,
                "descricao": "A legítima e consagrada carne de sol de Picuí, servida com pirão de leite, macaxeira na manteiga da terra, queijo coalho e feijão verde. Ambiente climatizado e acolhedor no coração da cidade.",
                "historia": "Tradição gastronômica familiar com mais de 30 anos valorizando a receita secular da carne de sol picuiense reconhecida nacionalmente.",
                "status": "aprovado",
                "categorias": ["gastronomia"],
            },
            {
                "nome": "Pousada Portal do Seridó",
                "responsavel": "Maria Aparecida de Lima",
                "cpf_responsavel": "222.333.444-55",
                "cnpj": "23.456.789/0001-01",
                "zona": "urbana",
                "endereco": "Avenida Juscelino Kubitschek, 320",
                "bairro_comunidade": "Bairro São José",
                "telefone": "(83) 99123-4567",
                "whatsapp": "83991234567",
                "email": "portaldoserido@pousada.com.br",
                "instagram": "pousadaportaldoserido",
                "possui_cadastur": True,
                "numero_cadastur": "15.01.03.99-PB",
                "quarto_acessibilidade": True,
                "acessibilidade": "Rampas de acesso e banheiros adaptados para PcD",
                "cafe_incluso": True,
                "possui_estacionamento": True,
                "dias_funcionamento": "Todos os dias",
                "horario_funcionamento": "Recepção 24 horas",
                "descricao": "Hospedagem confortável para turistas e profissionais. Quartos com ar-condicionado, Wi-Fi de alta velocidade, café da manhã regional farto e atendimento de excelência.",
                "status": "aprovado",
                "categorias": ["hospedagem"],
            },
            {
                "nome": "Mirante e Trilha da Serra dos Brandões",
                "responsavel": "Guia Ecoturismo de Picuí",
                "cpf_responsavel": "333.444.555-66",
                "zona": "rural",
                "endereco": "Serra dos Brandões, s/n",
                "bairro_comunidade": "Comunidade dos Brandões",
                "telefone": "(83) 98765-4321",
                "whatsapp": "83987654321",
                "dias_funcionamento": "Sexta, Sábado e Domingo (com agendamento)",
                "horario_funcionamento": "05:30 às 18:00",
                "descricao": "Ponto culminante da região com vista panorâmica impressionante de 360 graus do Seridó paraibano e potiguar. Ideal para contemplação do pôr do sol, fotografia da caatinga e trilhas ecológicas guiadas.",
                "status": "aprovado",
                "categorias": ["atrativo-natural", "turismo-de-aventura", "turismo-rural"],
            },
            {
                "nome": "Igreja Matriz de São Sebastião",
                "responsavel": "Paróquia de São Sebastião de Picuí",
                "cpf_responsavel": "444.555.666-77",
                "zona": "urbana",
                "endereco": "Praça João Pessoa, s/n",
                "bairro_comunidade": "Centro",
                "telefone": "(83) 3371-2100",
                "dias_funcionamento": "Terça a Domingo",
                "horario_funcionamento": "08:00 às 11:30 e 14:00 às 18:00",
                "descricao": "Templo histórico construído no século XIX, símbolo da fé, da fundação da cidade e da tradicional Festa de São Sebastião, padroeiro de Picuí, que reúne milhares de romeiros e visitantes anualmente.",
                "status": "aprovado",
                "categorias": ["atrativo-religioso", "atrativo-cultural"],
            },
            {
                "nome": "Associação Arte da Terra Picuiense",
                "responsavel": "Lúcia Helena Barbosa",
                "cpf_responsavel": "555.666.777-88",
                "zona": "urbana",
                "endereco": "Rua Ferreira de Macedo, 88",
                "bairro_comunidade": "Centro",
                "telefone": "(83) 99654-7890",
                "whatsapp": "83996547890",
                "instagram": "artedaterrapicui",
                "dias_funcionamento": "Segunda a Sábado",
                "horario_funcionamento": "08:00 às 17:30",
                "descricao": "Espaço de artesanato cooperativo exibindo bordados renascença, peças em couro legítimo, cerâmica típica sertaneja e doces regionais de pequenos produtores rurais.",
                "status": "aprovado",
                "categorias": ["artesanato", "atrativo-cultural"],
            },
            {
                "nome": "Pousada e Camping Recanto das Serras",
                "responsavel": "Antônio Bezerra de Farias",
                "cpf_responsavel": "666.777.888-99",
                "zona": "rural",
                "endereco": "Sítio Limeira, KM 4",
                "bairro_comunidade": "Zona Rural de Picuí",
                "telefone": "(83) 99432-8765",
                "whatsapp": "83994328765",
                "possui_cadastur": False,
                "dias_funcionamento": "Quinta a Domingo",
                "horario_funcionamento": "07:00 às 21:00",
                "descricao": "Experiência de turismo rural com chalés rústicos, área para acampamento sob o céu estrelado do sertão, açude para pesca esportiva e gastronomia típica da roça.",
                "status": "pendente",
                "categorias": ["hospedagem", "turismo-rural"],
            },
            {
                "nome": "Bodega do Seridó - Queijos e Doces",
                "responsavel": "Cláudio Roberto Silva",
                "cpf_responsavel": "777.888.999-00",
                "zona": "urbana",
                "endereco": "Mercado Público Municipal, Box 12",
                "bairro_comunidade": "Centro",
                "telefone": "(83) 99345-6789",
                "whatsapp": "83993456789",
                "dias_funcionamento": "Segunda a Sábado",
                "horario_funcionamento": "06:00 às 14:00",
                "descricao": "Ponto de parada obrigatória para comprar a legítima manteiga da garrafa, queijo de coalho curado, rapaduras artesanais e doces de leite de Picuí.",
                "status": "pendente",
                "categorias": ["gastronomia", "artesanato"],
            },
        ]

        for item in dados_empreendimentos:
            cats = item.pop("categorias")
            emp, created = Empreendimento.objects.update_or_create(
                nome=item["nome"],
                defaults=item,
            )
            for c_slug in cats:
                if c_slug in cat_objs:
                    emp.categorias.add(cat_objs[c_slug])

            action = "Criado" if created else "Atualizado"
            self.stdout.write(f"  [OK] {action}: {emp.nome} ({emp.status})")

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso com dados oficiais de Picui!"))
