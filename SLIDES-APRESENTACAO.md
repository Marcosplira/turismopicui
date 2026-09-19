# Slides - Turismo de Picuí

## Slide 1 - Capa

**Turismo de Picuí**

Catálogo Digital do Guia Turístico de Picuí - PB

Sistema para cadastro, análise e divulgação de empreendimentos turísticos.

## Slide 2 - Objetivo

- Reunir serviços turísticos do município.
- Fortalecer a divulgação de empreendedores locais.
- Facilitar o acesso de moradores e visitantes.
- Organizar os cadastros em um painel administrativo.

## Slide 3 - Quem pode se cadastrar

- Hotéis, pousadas e hospedagens.
- Restaurantes, bares e gastronomia.
- Artesãos e produtores culturais.
- Guias e condutores locais.
- Atrativos naturais e culturais.
- Eventos, transporte e serviços turísticos.

## Slide 4 - Como funciona o cadastro

1. O empreendedor acessa o formulário pelo site ou QR Code.
2. Informa os dados do empreendimento.
3. Pode selecionar várias categorias.
4. Envia até quatro fotos JPG ou PNG.
5. Aceita o aviso de privacidade.
6. A Prefeitura analisa o cadastro.

## Slide 5 - Informações coletadas

- Identificação do empreendimento e responsável.
- CPF, CNPJ e cadastros turísticos.
- Endereço, zona, bairro e contatos.
- Redes sociais e tipo de empreendimento.
- Hospedagem, quartos, leitos e diárias.
- Funcionamento, estacionamento e acessibilidade.
- Cultura local, sustentabilidade e interesse no selo municipal.

## Slide 6 - Guia público

O guia exibe somente empreendimentos aprovados pela equipe responsável.

Recursos:

- Busca por nome, tipo, bairro e descrição.
- Filtro por categoria.
- Filtro por zona urbana ou rural.
- Botão de WhatsApp.
- Localização no Google Maps.
- Fotos e descrição do empreendimento.

## Slide 7 - Administração

No painel `/admin/`, a equipe pode:

- consultar todos os cadastros;
- pesquisar por nome, responsável, telefone ou e-mail;
- revisar fotos e informações;
- aprovar ou reprovar cadastros;
- administrar categorias;
- acompanhar a data de cadastro.

## Slide 8 - Acesso do cliente

Após enviar o cadastro, o cliente pode clicar em **Meus dados** para consultar automaticamente o cadastro recente no mesmo navegador.

Não é necessário criar senha para o cliente.

## Slide 9 - Acesso e divulgação

- Site: https://turismo-picui.onrender.com/
- Cadastro: https://turismo-picui.onrender.com/cadastro/
- Guia: https://turismo-picui.onrender.com/guia/
- QR Code para home e cadastro.
- Revista turística integrada.
- Site e Instagram oficiais da Prefeitura.

## Slide 10 - Tecnologia

- Django e Python.
- PostgreSQL no Render.
- Gunicorn para produção.
- WhiteNoise para arquivos estáticos.
- Docker e Docker Compose preparados.
- GitHub para versionamento.
- Render para hospedagem HTTPS.

## Slide 11 - Segurança e privacidade

- Área administrativa protegida por usuário de equipe.
- Dados de CPF e contatos tratados para finalidade institucional.
- Aviso de privacidade no formulário.
- Fotos limitadas a JPG/PNG com até 5 MB cada.
- `DEBUG=False` em produção.
- Chave secreta mantida em variável de ambiente.

## Slide 12 - Próximas melhorias

- Armazenamento permanente das fotos em Cloudinary, Google Cloud Storage ou S3.
- Configuração de SMTP para confirmação por e-mail.
- Domínio oficial da Prefeitura.
- Backup automático do PostgreSQL.
- Página detalhada para cada empreendimento.

## Slide 13 - Encerramento

**Turismo de Picuí**

Serviços, gastronomia, hospedagem e cultura em um só lugar.

Secretário de Agricultura, Turismo e Meio Ambiente: Robinson Santos

Diretor Municipal de Turismo e Meio Ambiente: Ismael Moisés

Assessor Municipal de Turismo: Manassés Araújo - Serginho