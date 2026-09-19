# Turismo de Picuí

Aplicativo web em Django para cadastro de empreendimentos turísticos.

## Documentação de entrega

Consulte [DOCUMENTACAO-ENTREGA.md](DOCUMENTACAO-ENTREGA.md) para abrir o sistema no computador e no celular, configurar o admin, fazer backup e publicar em um provedor.

## Requisitos
- Python 3.12+
- pip
- virtualenv (opcional)

## Execução local

1. Crie o ambiente virtual:
   python -m venv venv

2. Ative o ambiente:
   - Windows (PowerShell): .\venv\Scripts\Activate.ps1
   - Windows (CMD): venv\Scripts\activate.bat

3. Instale as dependências:
   pip install -r requirements.txt

4. Execute as migrações:
   python manage.py migrate

5. Rode o projeto:
   python manage.py runserver 127.0.0.1:8001

6. Acesse:
   http://127.0.0.1:8001/cadastro/

## Docker

### Build e execução

docker build -t turismo-picui .
docker run -p 8000:8000 turismo-picui

Ou com Docker Compose:

docker-compose up --build

## Observações
- A aplicação usa upload de imagens e guarda os arquivos em media/
- Em produção, configure SECRET_KEY e ALLOWED_HOSTS com valores reais
- Para deploy real, use um provedor como Render, Railway, Azure App Service, VPS ou similar
