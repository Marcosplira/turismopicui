# Turismo de Picuí

Sistema web para **cadastro, análise, organização e divulgação de empreendimentos turísticos de Picuí-PB**, desenvolvido com Django.

## 🌐 Acesso ao sistema

**Turismo de Picuí:**  
https://turismopicui.pythonanywhere.com/

O sistema pode ser acessado pelo navegador em computadores, tablets e celulares.

---

## 📌 Visão geral

O **Turismo de Picuí** foi desenvolvido para facilitar o cadastro e a divulgação dos empreendimentos turísticos do município.

O sistema permite:

- cadastrar empreendimentos turísticos;
- selecionar categorias;
- informar localização e dados de contato;
- enviar fotos dos empreendimentos;
- analisar cadastros através da área administrativa;
- aprovar ou reprovar registros;
- exibir somente empreendimentos aprovados no guia público;
- disponibilizar acesso rápido por QR Code;
- facilitar o contato através do WhatsApp;
- abrir a localização do empreendimento no Google Maps;
- disponibilizar um guia turístico digital para visitantes.

---

## 🚀 Funcionalidades

### 🏨 Cadastro de empreendimentos

Permite cadastrar informações como:

- nome do empreendimento;
- categoria;
- descrição;
- endereço;
- telefone;
- WhatsApp;
- localização;
- fotos;
- outras informações relevantes.

### 🔎 Guia turístico público

O guia público apresenta os empreendimentos aprovados e permite ao visitante consultar as informações disponíveis.

Acesso:

**https://turismopicui.pythonanywhere.com/guia/**

### 📱 QR Code

O sistema possui recursos de acesso rápido através de QR Code, facilitando o acesso às informações turísticas pelo celular.

### 📍 Google Maps

Os empreendimentos podem disponibilizar sua localização para facilitar a chegada dos visitantes.

### 💬 WhatsApp

O visitante pode utilizar o WhatsApp para entrar em contato diretamente com o empreendimento quando o número estiver cadastrado.

---

## 📚 Documentação de entrega

- [DOCUMENTACAO-ENTREGA.md](https://github.com/Marcosplira/turismopicui/blob/main/DOCUMENTACAO-ENTREGA.md) — instruções de uso local, celular, painel administrativo, backups e publicação.
- [SLIDES-APRESENTACAO.md](https://github.com/Marcosplira/turismopicui/blob/main/SLIDES-APRESENTACAO.md) — roteiro para apresentação do sistema ao cliente.
- [ROADMAP-MELHORIAS.md](https://github.com/Marcosplira/turismopicui/blob/main/ROADMAP-MELHORIAS.md) — planejamento de melhorias e evolução do sistema.

---

## 🛠️ Tecnologias utilizadas

- Python
- Django
- HTML5
- CSS3
- JavaScript
- PostgreSQL
- Gunicorn
- Git/GitHub

---

## 💻 Requisitos

Para executar o projeto localmente, é necessário ter instalado:

- Python 3.12+
- pip
- virtualenv (opcional)
- Git
- Docker e Docker Compose (opcional)

---

## ⚙️ Execução local

### 1. Criar o ambiente virtual

```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual

No Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Aplicar as migrações

```bash
python manage.py migrate
```

### 5. Iniciar o servidor

```bash
python manage.py runserver 127.0.0.1:8001
```

### 6. Acessar o sistema

- **Home:** http://127.0.0.1:8001/
- **Cadastro:** http://127.0.0.1:8001/cadastro/
- **Guia público:** http://127.0.0.1:8001/guia/
- **Admin:** http://127.0.0.1:8001/admin/
- **Dashboard do gerente:** http://127.0.0.1:8001/cadastro/dashboard-gerente/

---

## 🌐 Produção

### Site

https://turismopicui.pythonanywhere.com/

### Guia público

https://turismopicui.pythonanywhere.com/guia/

### Administração

https://turismopicui.pythonanywhere.com/admin/

### Dashboard do gerente

https://turismopicui.pythonanywhere.com/cadastro/dashboard-gerente/

> O acesso ao painel administrativo e ao dashboard exige um usuário administrativo configurado no ambiente de produção.

**Nunca publique senhas ou credenciais no GitHub.**

---

## 🐳 Docker

### Build da imagem

```bash
docker build -t turismo-picui .
```

### Executar o container

```bash
docker run -p 8000:8000 turismo-picui
```

### Docker Compose

```bash
docker compose up --build
```

---

## 🔐 Configuração de produção

As variáveis de ambiente devem ser configuradas na hospedagem.

Exemplo:

```env
DEBUG=False
DJANGO_SECRET_KEY=sua-chave-secreta
ALLOWED_HOSTS=seu-dominio.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://seu-dominio.com
```

**Não coloque chaves, senhas ou outras credenciais diretamente no código ou no GitHub.**

---

## 📋 Checklist de entrega

- [x] Projeto Django funcionando
- [x] Cadastro de empreendimentos
- [x] Guia turístico público
- [x] Filtros no guia
- [x] Área administrativa
- [x] Aprovação e reprovação de cadastros
- [x] Integração com WhatsApp
- [x] Integração com Google Maps
- [x] Acesso por QR Code
- [x] Preparado para publicação em hospedagem
- [x] Documentação de uso
- [x] Documentação de apresentação
- [x] Dashboard executivo com gráficos
- [x] Exportação de relatórios CSV
- [x] Galeria de fotos interativa
- [x] Animações e micro-interações
- [x] Página institucional "Sobre"
- [x] Hero Section premium com gradiente
- [x] Mapa interativo de todos os empreendimentos
- [x] Contadores de estatísticas na Home
- [x] Seção de depoimentos de empresários
- [x] Botão de acesso da equipe em destaque
- [x] Interface otimizada para apresentação ao gerente

---

## 📸 Imagens e arquivos

Os arquivos enviados pelos usuários podem ser armazenados no diretório `media/` durante o desenvolvimento local.

Em produção, recomenda-se utilizar um serviço de armazenamento externo para imagens, como:

- Cloudinary;
- Google Cloud Storage;
- Amazon S3.

---

## 🔒 Segurança

Algumas boas práticas devem ser mantidas no projeto:

- nunca publicar `SECRET_KEY`;
- nunca publicar senhas do banco de dados;
- utilizar variáveis de ambiente;
- manter `DEBUG=False` em produção;
- configurar corretamente `ALLOWED_HOSTS`;
- configurar `CSRF_TRUSTED_ORIGINS`;
- não armazenar credenciais diretamente no código-fonte.

---

## 👨‍💻 Desenvolvedor

**Marcos Paulo Santos Lira**

Projeto desenvolvido para contribuir com a divulgação e organização do turismo de **Picuí-PB** através da tecnologia.
