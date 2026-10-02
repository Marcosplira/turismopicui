# Turismo de Picuí

Sistema de cadastro, análise e divulgação de empreendimentos turísticos de Picuí, desenvolvido em Django.

## Visão geral

O projeto permite:
- cadastrar empreendimentos turísticos;
- selecionar categorias e informações de localização/contato;
- enviar fotos do empreendimento;
- revisar cadastros em área administrativa;
- aprovar ou reprovar registros;
- exibir somente empreendimentos aprovados no guia público;
- disponibilizar acesso rápido por QR Code, WhatsApp e Google Maps.

## Documentação de entrega

- [DOCUMENTACAO-ENTREGA.md](DOCUMENTACAO-ENTREGA.md): instruções de uso local, celular, painel admin, backups e publicação.
- [SLIDES-APRESENTACAO.md](SLIDES-APRESENTACAO.md): roteiro para apresentação ao cliente.
- [ROADMAP-MELHORIAS.md](ROADMAP-MELHORIAS.md): planejamento profissional para evoluir o sistema com PWA, dashboard, QR Code, automação e IA.

## Requisitos

- Python 3.12+
- pip
- virtualenv (opcional)
- Docker e Docker Compose (opcional para containerização)

## Execução local

1. Crie e ative o ambiente virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```

3. Aplique as migrações:
   ```powershell
   python manage.py migrate
   ```

4. Inicie o servidor:
   ```powershell
   python manage.py runserver 127.0.0.1:8001
   ```

5. Acesse:
   - Home: http://127.0.0.1:8001/
   - Cadastro: http://127.0.0.1:8001/cadastro/
   - Guia público: http://127.0.0.1:8001/guia/
   - Admin: http://127.0.0.1:8001/admin/

## Docker

### Build local

```powershell
docker build -t turismo-picui .
docker run -p 8000:8000 turismo-picui
```

### Docker Compose

```powershell
docker compose up --build
```

A aplicação fica disponível em:
- http://127.0.0.1:8000/

## Configuração de produção

Para publicação em Render, Railway, VPS ou outra hospedagem, defina as variáveis de ambiente:

```bash
DEBUG=False
DJANGO_SECRET_KEY=sua-chave-secreta
ALLOWED_HOSTS=seu-dominio.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://seu-dominio.com
```

## Checklist de entrega

- [x] Projeto Django funcionando localmente
- [x] Cadastro de empreendimentos operacional
- [x] Guia público com filtros
- [x] Administração para análise e aprovação
- [x] Preparado para deploy em host com Gunicorn
- [x] Docker configurado para execução em container
- [x] Documentação de uso e apresentação atualizada

## Observações importantes

- Os arquivos enviados pelo cliente ficam em `media/` localmente.
- Em produção, recomenda-se armazenar imagens em serviço externo, como Cloudinary, Google Cloud Storage ou S3.
- Nunca publique senhas ou chaves de produção no GitHub.
