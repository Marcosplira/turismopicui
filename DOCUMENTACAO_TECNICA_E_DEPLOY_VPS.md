# Turismo de Picuí — documentação técnica e publicação em VPS

**Objetivo:** orientar a equipe técnica a instalar, publicar, atualizar e manter este projeto Django em uma VPS Linux.

> **Atenção sobre a hospedagem atual:** o endereço público documentado do sistema é `https://turismopicui.pythonanywhere.com/`. Este manual descreve uma instalação separada em VPS; seguir estes passos não altera automaticamente o site do PythonAnywhere nem o DNS do domínio. Planeje a migração e a troca de DNS separadamente.

## 1. Resumo da arquitetura

- Aplicação web: Django 6.0.1, Python 3.12 ou superior compatível.
- Servidor de aplicação: Gunicorn.
- Banco: PostgreSQL recomendado para VPS. SQLite é usado por padrão em desenvolvimento e não é recomendado para uma instalação multiusuário de produção.
- Proxy HTTPS: Nginx com certificado TLS.
- Arquivos estáticos: WhiteNoise e `collectstatic`.
- Fotos enviadas: gravadas em `MEDIA_ROOT` (`media/` no projeto); em VPS, precisam de armazenamento persistente e backup.
- Mapa: Leaflet e tiles ArcGIS/Esri. Não requer chave de API do Google. O mapa depende de serviços externos e não deve ser submetido ao teste de carga HTTP.

Principais diretórios:

| Caminho | Conteúdo |
|---|---|
| `cadastro/` | Modelos, formulários, páginas, rotas e administração |
| `config/` | Configurações Django, URLs e inicialização WSGI |
| `cadastro/migrations/` | Migrações versionadas do banco |
| `cadastro/static/` | CSS, JavaScript, imagens e outros arquivos estáticos |
| `media/` | Fotos enviadas pelos usuários em execução |
| `staticfiles/` | Resultado gerado por `collectstatic`; não editar manualmente |
| `scripts/validar_carga_local.py` | Teste HTTP local de 50 e 100 clientes |

## 2. Antes de iniciar

Providencie:

- VPS Ubuntu 24.04 LTS ou versão equivalente, com Python 3.12;
- domínio apontado para o endereço IP da VPS;
- acesso administrativo à VPS;
- portas TCP 22, 80 e 443 liberadas no firewall;
- repositório Git e método de autenticação de deploy;
- senha longa para o usuário do banco e credenciais SMTP válidas, se o sistema enviar e-mails;
- política de backup para o PostgreSQL e para as fotos.

Use um hostname definitivo. Neste projeto, `ALLOWED_HOSTS` pode ser complementado pela variável de ambiente `ALLOWED_HOSTS` (nomes separados por vírgula). O código também cria origens HTTPS confiáveis para esses hosts. A configuração não lê a variável `CSRF_TRUSTED_ORIGINS` do ambiente.

## 3. Instalar pacotes do sistema

Conecte-se à VPS por SSH. Os comandos abaixo são executados no Ubuntu:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python3.12 python3.12-venv python3-pip \
  nginx postgresql postgresql-contrib certbot python3-certbot-nginx
```

Confirme as versões:

```bash
python3.12 --version
psql --version
nginx -v
```

Não execute uma atualização de sistema em horário de operação sem janela de manutenção e backup.

## 4. Criar banco e usuário PostgreSQL

Abra o console administrativo local:

```bash
sudo -u postgres psql
```

No prompt do PostgreSQL, crie uma conta e um banco próprios para o sistema:

```sql
CREATE ROLE turismo_picui LOGIN;
\password turismo_picui
CREATE DATABASE turismo_picui OWNER turismo_picui;
\q
```

O comando `\password` solicita a senha de forma interativa. Guarde-a em um gerenciador de segredos; não a inclua no Git ou em documentos compartilhados.

## 5. Baixar o projeto e preparar o ambiente Python

Crie uma conta de serviço sem login interativo e clone o repositório:

```bash
sudo adduser --system --group --home /opt/turismo-picui \
  --shell /usr/sbin/nologin turismo
sudo -u turismo git clone --branch main \
  https://github.com/Marcosplira/turismopicui.git /opt/turismo-picui
```

Se o repositório não for público no momento da instalação, configure uma deploy key ou outro método aprovado; não coloque token de Git na URL.

Crie o ambiente virtual e instale as dependências:

```bash
sudo -u turismo python3.12 -m venv /opt/turismo-picui/venv
sudo -u turismo /opt/turismo-picui/venv/bin/pip install --upgrade pip
sudo -u turismo /opt/turismo-picui/venv/bin/pip install \
  -r /opt/turismo-picui/requirements.txt
```

## 6. Configurar variáveis de ambiente

Gere uma chave secreta fora do repositório:

```bash
python3.12 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Crie um arquivo restrito para o serviço:

```bash
sudo install -o root -g turismo -m 640 /dev/null /etc/turismo-picui.env
sudo nano /etc/turismo-picui.env
```

O arquivo também será lido pelo comando de manutenção abaixo; mantenha-o em sintaxe compatível com shell, coloque valores com espaços entre aspas e não use `source` em arquivo editável por usuários não confiáveis. Exemplo (substitua todos os valores; não copie senha real para documentação):

```dotenv
DEBUG=False
DJANGO_SECRET_KEY=COLE_AQUI_UMA_CHAVE_ALEATORIA_LONGA
ALLOWED_HOSTS=turismo.seudominio.gov.br,www.turismo.seudominio.gov.br,localhost,127.0.0.1
DATABASE_URL=postgresql://turismo_picui:SENHA_URL_ENCODED@127.0.0.1:5432/turismo_picui

EMAIL_HOST=smtp.seu-provedor.gov.br
EMAIL_PORT=587
EMAIL_HOST_USER=conta-de-envio@seudominio.gov.br
EMAIL_HOST_PASSWORD=SENHA_OU_TOKEN_SMTP
EMAIL_USE_TLS=True
EMAIL_TIMEOUT=10
DEFAULT_FROM_EMAIL="Turismo de Picuí <conta-de-envio@seudominio.gov.br>"
ADMIN_EMAIL=turismo@seudominio.gov.br
```

Cuidados:

- `ALLOWED_HOSTS` recebe nomes de host, sem `https://` e separados por vírgula.
- Codifique caracteres especiais da senha do banco para uso em URL (`DATABASE_URL`).
- O SMTP precisa ser fornecido pelo provedor de e-mail e testado na própria hospedagem. Se falhar, o cadastro ainda pode ser salvo, mas a aplicação pode avisar que a notificação não foi enviada.
- Não defina credenciais `DJANGO_BOOTSTRAP_ADMIN_*` permanentemente no ambiente do serviço.
- O arquivo deve continuar fora do repositório e protegido com permissão `640`, dono `root` e grupo `turismo`.

## 7. Configuração de HTTPS necessária antes do uso real

O Nginx deste manual termina o TLS e encaminha tráfego para Gunicorn. Com `DEBUG=False`, o projeto marca automaticamente os cookies de sessão e CSRF como seguros. **A configuração Django não liga automaticamente o redirecionamento HTTPS nem HSTS e não confia automaticamente no proxy.** Antes de disponibilizar dados pessoais em produção, ajuste `config/settings.py`, dentro do bloco de configurações de segurança, para aplicar os controles após confirmar que o proxy não é acessível diretamente pela internet:

```python
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
```

No início, deixe HSTS em `0`. Depois de verificar certificado, redirecionamento e funcionamento do login em HTTPS, configure um período curto de teste; só aumente para um ano (31.536.000 segundos) após validar todos os subdomínios e a política do domínio. Não ative `includeSubDomains` ou `preload` sem revisão da infraestrutura.

O cabeçalho `X-Forwarded-Proto` deve ser definido pelo seu Nginx confiável, como na configuração abaixo. Não confie nesse cabeçalho de clientes externos se a aplicação/Gunicorn estiver acessível fora do proxy.

## 8. Preparar dados, estáticos e usuário gerente

Antes de mexer no banco de uma instalação já existente, faça backup. Em uma instalação nova:

```bash
turismo_manage() {
  sudo -u turismo bash -c '
    set -a
    . /etc/turismo-picui.env
    set +a
    cd /opt/turismo-picui
    exec /opt/turismo-picui/venv/bin/python manage.py "$@"
  ' _ "$@"
}

turismo_manage migrate
turismo_manage collectstatic --noinput
turismo_manage check
turismo_manage check --deploy
turismo_manage createsuperuser
```

Defina essa função uma vez no terminal administrativo e execute os comandos apresentados. Ela carrega as mesmas variáveis usadas pelo serviço, sem colocar a senha do gerente no histórico. Use `createsuperuser` no terminal para cadastrar o gerente; depois, entre no Admin e confira `is_staff`/permissões. O dashboard exige usuário autenticado com acesso administrativo.

### Aviso: registros de demonstração

**Não execute `python manage.py popular_dados` em produção.** Esse comando cria/atualiza empreendimentos e depoimentos de demonstração; ele pode inserir conteúdo não validado e atualizar os registros de exemplo. Os dados devem ser cadastrados e aprovados pela equipe.

### Resultado de `check --deploy`

Este comando é uma revisão de configuração, não um teste de tráfego. Com as configurações atuais sem o ajuste de HTTPS acima, são esperados avisos de segurança sobre HSTS e redirecionamento SSL. Corrija os avisos aplicáveis antes de considerar o ambiente pronto para dados pessoais. Warnings devem ser analisados, não silenciados.

## 9. Configurar Gunicorn como serviço systemd

Crie `/etc/systemd/system/turismo-picui.service`:

```ini
[Unit]
Description=Turismo de Picuí Django
After=network.target postgresql.service

[Service]
Type=notify
User=turismo
Group=turismo
WorkingDirectory=/opt/turismo-picui
EnvironmentFile=/etc/turismo-picui.env
ExecStart=/opt/turismo-picui/venv/bin/gunicorn config.wsgi:application \
  --bind 127.0.0.1:8000 --workers 2 --timeout 60
Restart=on-failure
RestartSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Ative o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now turismo-picui
sudo systemctl status turismo-picui --no-pager
sudo journalctl -u turismo-picui -n 100 --no-pager
```

Gunicorn escuta somente `127.0.0.1`; não o exponha diretamente na internet.

## 10. Configurar Nginx

Crie `/etc/nginx/sites-available/turismo-picui` e troque os domínios:

```nginx
server {
    listen 80;
    server_name turismo.seudominio.gov.br www.turismo.seudominio.gov.br;

    client_max_body_size 25m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }

    location /media/ {
        alias /opt/turismo-picui/media/;
        add_header X-Content-Type-Options nosniff;
    }
}
```

Crie o diretório de uploads com permissões para a conta do serviço e habilite o site:

```bash
sudo install -d -o turismo -g turismo -m 750 /opt/turismo-picui/media
sudo ln -s /etc/nginx/sites-available/turismo-picui \
  /etc/nginx/sites-enabled/turismo-picui
sudo nginx -t
sudo systemctl reload nginx
```

Após o DNS apontar para a VPS, obtenha o certificado:

```bash
sudo certbot --nginx -d turismo.seudominio.gov.br \
  -d www.turismo.seudominio.gov.br
sudo certbot renew --dry-run
```

Revise a configuração do Certbot: HTTP deve redirecionar para HTTPS e somente o bloco HTTPS deve encaminhar a aplicação. O servidor de aplicação não deve ficar acessível publicamente pela porta 8000.

## 11. Atualização e rotina de deploy

Antes de cada atualização:

1. Agende a janela de publicação e avise a equipe.
2. Faça backup do banco e dos uploads.
3. Confira o branch e os commits publicados; não atualize com mudanças locais não revisadas.
4. Baixe o código e dependências.
5. Aplique migrações e gere estáticos.
6. Rode os checks, reinicie e faça smoke test.

Exemplo de atualização simples (redefina `turismo_manage` com o trecho da seção 8 sempre que abrir uma nova sessão SSH):

```bash
cd /opt/turismo-picui
sudo -u turismo git fetch origin
sudo -u turismo git pull --ff-only origin main
sudo -u turismo /opt/turismo-picui/venv/bin/pip install \
  -r /opt/turismo-picui/requirements.txt
turismo_manage migrate
turismo_manage collectstatic --noinput
turismo_manage check
sudo systemctl restart turismo-picui
sudo systemctl status turismo-picui --no-pager
```

`git pull` atualiza código, mas não garante rollback do banco. Migrações que removem/renomeiam colunas podem ser incompatíveis com a versão anterior: planeje backup e rollback caso a release inclua uma alteração destrutiva. Nunca reverta banco de produção sem procedimento aprovado.

## 12. Backup e recuperação

### PostgreSQL

Crie uma pasta acessível apenas à equipe de operação. Um backup manual pelo administrador local do PostgreSQL:

```bash
sudo install -d -o postgres -g postgres -m 700 /var/backups/turismo-picui
sudo -u postgres bash -c \
  'pg_dump -Fc turismo_picui > /var/backups/turismo-picui/db-$(date +%Y%m%d-%H%M%S).dump'
```

### Fotos enviadas

O banco não contém os arquivos de imagem; faça backup de `media/` separadamente:

```bash
sudo tar -czf /var/backups/turismo-picui/media-$(date +%Y%m%d-%H%M%S).tar.gz \
  -C /opt/turismo-picui media
```

Copie backups para armazenamento fora da VPS com acesso restrito, defina retenção e teste restauração em ambiente separado. Um backup só é confiável após uma restauração de teste.

Para SQLite local, o comando disponível é:

```bash
python manage.py backup_db
```

Esse comando foi feito para SQLite e recusa PostgreSQL. Em produção PostgreSQL, use `pg_dump` e siga a política de backup do administrador do banco.

## 13. Verificações pós-publicação

Faça as verificações a seguir pelo navegador e, quando aplicável, pelo terminal:

1. Home responde e os links principais abrem.
2. Cadastro de teste controlado é enviado e aparece como pendente no painel.
3. Gerente entra no dashboard e no Admin com HTTPS.
4. Revisão de pendentes, edição e filtros funcionam.
5. Um registro de teste é aprovado e aparece no Guia; depois, é removido/ajustado conforme a política de dados da equipe.
6. CSV e relatório executivo abrem somente para usuário autorizado.
7. Uma foto de teste é carregada, servida por HTTPS e incluída no backup de mídia.
8. E-mail é enviado; se SMTP falhar, confira alerta da tela e logs.
9. Mapa base, geossítios, botões de foco e retorno ao mapa completo funcionam.
10. Logs do serviço e Nginx não contêm erros:

```bash
sudo journalctl -u turismo-picui -n 100 --no-pager
sudo tail -n 100 /var/log/nginx/error.log
```

### Testes automatizados e teste de carga

Rode primeiro a suíte:

```bash
cd /opt/turismo-picui
turismo_manage test
```

O script `scripts/validar_carga_local.py` simula 50 e 100 clientes HTTP acessando Home, Guia e Mapa. Ele aceita somente `localhost`/loopback e verifica migrações. Execute em ambiente local ou staging com banco próprio, nunca contra o domínio público nem contra o banco da VPS de produção:

```bash
sudo -u turismo bash -c '
  cd /opt/turismo-picui
  exec /opt/turismo-picui/venv/bin/python scripts/validar_carga_local.py
'
```

Execute esse comando apenas em uma cópia local/staging com banco próprio, depois de aplicar as migrações nessa cópia. Não carregue as variáveis do banco de produção nesse teste.

Esse teste mede respostas HTML da aplicação; não mede o provedor do mapa, entrega de e-mail, upload de arquivos ou capacidade real de produção. Os resultados obtidos em uma máquina local não são uma garantia de capacidade da VPS.

## 14. Dados, privacidade e limitações conhecidas

- Os formulários coletam dados pessoais, incluindo CPF e contatos. Dê acesso administrativo somente a pessoas autorizadas, proteja exports/backups e siga a política institucional de retenção e privacidade.
- O CSV administrativo inclui CPF, CNPJ, contatos e outros dados. Não envie a planilha em grupos públicos nem a armazene sem proteção.
- A publicação no Guia depende da aprovação do registro. A equipe deve revisar conteúdo e autorização de divulgação antes de aprovar.
- Os três geossítios possuem coordenadas informadas no mapa. Para empreendimentos sem georreferenciamento cadastrado, o mapa pode exibir posições aproximadas geradas pela aplicação. **Confirme as coordenadas reais com a equipe antes de orientar visitantes por esses pontos.**
- Tiles, Tailwind, Chart.js e outras bibliotecas externas dependem de terceiros e de conexão de internet. Uma indisponibilidade externa pode afetar o mapa ou os gráficos sem derrubar o cadastro e o banco.
- Não use registros de demonstração ou depoimentos de exemplo como informação oficial sem validação e autorização.

## 15. Checklist de entrada no ar da VPS

- [ ] Domínio e DNS apontam para a VPS correta.
- [ ] Python e dependências instalados de forma reproduzível.
- [ ] PostgreSQL acessível somente localmente/rede privada; usuário sem privilégios excessivos.
- [ ] Variáveis secretas estão fora do repositório e com permissões restritas.
- [ ] Migrações aplicadas; dados demonstrativos não foram executados em produção.
- [ ] `DEBUG=False`, host permitido e chave secreta forte.
- [ ] Redirecionamento HTTPS, proxy confiável, cookies seguros e HSTS revisados.
- [ ] `manage.py check --deploy` executado e cada aviso tratado.
- [ ] Nginx e Gunicorn operam como proxy e serviço; porta 8000 não exposta.
- [ ] Uploads persistentes; backup de banco e mídia agendado, externo e testado.
- [ ] Usuário gerente criado com senha individual e acesso mínimo necessário.
- [ ] Testes, smoke test, e-mail, mapa e fluxos de aprovação verificados.
- [ ] Plano de atualização, monitoramento e rollback aprovado pela equipe.

**Não declare a VPS pronta para produção até concluir os itens de segurança, backup e teste de restauração.**