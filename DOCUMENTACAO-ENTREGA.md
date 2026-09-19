# Documentacao de entrega - Turismo de Picui

## Acesso oficial publicado

- Site: https://turismo-picui.onrender.com/
- Cadastro: https://turismo-picui.onrender.com/cadastro/
- Guia publico: https://turismo-picui.onrender.com/guia/
- Administracao: https://turismo-picui.onrender.com/admin/

## 1. O que o aplicativo faz

O sistema permite:

- cadastrar empreendimentos e atrativos turisticos;
- enviar ate quatro fotos por cadastro;
- aceitar o aviso de privacidade;
- receber confirmacao por e-mail quando o SMTP estiver configurado;
- revisar cadastros no painel administrativo;
- aprovar ou reprovar empreendimentos;
- exibir somente empreendimentos aprovados no guia publico;
- pesquisar por nome, categoria e zona;
- abrir conversa no WhatsApp e localizacao no Google Maps;
- acessar home e cadastro por QR Code.

Rotas principais:

- Home: `/`
- Cadastro: `/cadastro/`
- Guia publico: `/guia/`
- Administracao: `/admin/`
- Privacidade: `/cadastro/privacidade/`

## 2. Abrir no computador hoje

No PowerShell, dentro da pasta do projeto:

```powershell
cd "C:\Users\Marcos Paulo\Desktop\TurismoPicui"
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8001
```

Abrir no navegador:

```text
http://127.0.0.1:8001/
```

O servidor deve permanecer aberto no terminal enquanto o sistema estiver sendo usado.

## 3. Abrir no celular pela mesma Wi-Fi

1. Conecte computador e celular na mesma rede Wi-Fi.
2. Descubra o IPv4 do computador com:

```powershell
ipconfig
```

3. Inicie o servidor aceitando conexoes da rede:

```powershell
.\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8002
```

4. No celular, abra o endereco usando o IPv4 do computador:

```text
http://192.168.3.17:8002/
```

O IP pode mudar. Se o Windows perguntar sobre firewall, permita acesso em rede privada.

O QR Code precisa ser visualizado na pagina aberta pelo IP da rede. Um QR Code criado com `127.0.0.1` nao funciona no celular.

## 4. Painel administrativo

Acesse:

```text
http://127.0.0.1:8001/admin/
```

Para criar o primeiro usuario administrador local:

```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

### Criar o administrador no Render

O login do administrador e diferente do cadastro do cliente. No Render, abra o servico `turismo-picui`, entre em **Shell** e execute:

```text
python manage.py createsuperuser
```

Quando aparecerem as perguntas, informe:

```text
Username: adminturismo
Email: um e-mail administrativo valido
Password: uma senha forte, com letras, numeros e simbolos
```

O valor `admin` e muito fraco e pode ser recusado pelas regras de senha do Django. Nao coloque a senha no GitHub, na documentacao publica ou no codigo.

Se `adminturismo` ja existir e a senha tiver sido esquecida, use o Shell do Render:

```text
python manage.py changepassword adminturismo
```

Na tela de login, use `adminturismo` no campo **Usuario**, nao no campo de e-mail. O Django Admin aceita o nome de usuario criado no comando acima.

O cliente nao precisa criar usuario, e-mail ou senha para consultar o cadastro. Depois de enviar o formulario, o sistema abre automaticamente o cadastro recente em `Meus dados` naquele navegador. Por seguranca, essa consulta fica vinculada a sessao do navegador; o administrador continua sendo o responsavel por localizar todos os dados no painel.

No admin:

1. Cadastre as categorias.
2. Cadastre ou revise empreendimentos.
3. Adicione fotos.
4. Use a acao `Aprovar empreendimentos selecionados`.
5. Confira o resultado em `/guia/`.

## 5. Backup local

Para criar uma copia do SQLite:

```powershell
.\venv\Scripts\python.exe manage.py backup_db
```

O arquivo sera salvo em `backups/`. Em producao PostgreSQL, use `pg_dump` ou o backup automatico do provedor.

## 6. Docker

Com o Docker Desktop instalado, na pasta do projeto:

```powershell
$env:DJANGO_SECRET_KEY = "gere-uma-chave-secreta-e-nao-compartilhe"
docker compose up --build
```

Abrir localmente:

```text
http://127.0.0.1:8000/
```

O Docker usa Gunicorn, executa a aplicacao na porta 8000 e exige `DJANGO_SECRET_KEY` real no ambiente.

## 7. Publicacao recomendada para a entrega

### Opcao mais simples: Render

O projeto ja inclui `render.yaml` e `build.sh`. Ao conectar o repositorio no Render como Blueprint, essa configuracao cria o servico web e o PostgreSQL, instala as dependencias, coleta os arquivos estaticos e aplica as migracoes.

A documentacao oficial do Render para Django recomenda:

- Web Service para a aplicacao;
- PostgreSQL gerenciado;
- variavel `DATABASE_URL`;
- variavel `DJANGO_SECRET_KEY` gerada pelo provedor;
- `DEBUG=False`;
- `ALLOWED_HOSTS` com o dominio publicado;
- comando de build com `collectstatic` e `migrate`;
- Gunicorn para iniciar a aplicacao.

Passos gerais:

1. Criar uma conta no Render.
2. Colocar o projeto em um repositorio privado no GitHub.
3. No Render, escolher **New > Blueprint** e selecionar o repositorio.
4. Conferir os servicos criados pelo arquivo `render.yaml`.
5. Criar um Web Service ligado ao repositorio, caso o Blueprint nao faca isso automaticamente.
6. Configurar:

```text
Build Command: bash build.sh
Start Command: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

7. Configurar as variaveis:

```text
DEBUG=False
DJANGO_SECRET_KEY=chave-gerada-pelo-provedor
DATABASE_URL=url-do-postgresql
ALLOWED_HOSTS=seu-endereco.onrender.com
CSRF_TRUSTED_ORIGINS=https://seu-endereco.onrender.com
```

8. Criar o usuario admin no Shell do servico:

```text
python manage.py createsuperuser
```

Render gera um endereco HTTPS para o servico. Depois que o endereco estiver funcionando, gere novamente os QR Codes.

### Railway

Railway tambem oferece deploy por GitHub, banco PostgreSQL e dominio publico gerado no painel. O fluxo e semelhante: conectar repositorio, adicionar PostgreSQL, configurar variaveis e gerar o dominio na area Networking.

### Google Cloud

Google Cloud Run e uma opcao profissional, mas exige mais configuracao: projeto, faturamento, Artifact Registry, Cloud Run, Cloud SQL PostgreSQL e Cloud Storage. Para uma entrega urgente, Render ou Railway reduzem o risco operacional.

## 8. Fotos em producao

A pasta `media/` funciona localmente, mas o disco de muitos servicos de hospedagem pode ser temporario. Antes de divulgar o sistema, configurar um armazenamento permanente, como:

- Google Cloud Storage;
- Cloudinary;
- Amazon S3.

## 9. E-mail em producao

Localmente, o projeto usa o backend de console e mostra a mensagem no terminal. Para envio real, configurar SMTP:

```text
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.seu-provedor.com
EMAIL_PORT=587
EMAIL_HOST_USER=usuario
EMAIL_HOST_PASSWORD=senha-ou-token
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=Turismo de Picui <noreply@seu-dominio.com>
```

Nunca colocar senha de e-mail dentro do codigo ou do repositorio.

## 10. Checklist antes de divulgar

- [x] Home abre no endereco publico.
- [x] Cadastro abre pelo celular.
- [ ] Consentimento e aviso de privacidade funcionam.
- [ ] Upload de JPG e PNG funciona.
- [ ] Fotos aparecem no armazenamento permanente.
- [ ] E-mail de confirmacao foi testado.
- [ ] Admin consegue aprovar um cadastro.
- [ ] Empreendimento aprovado aparece em `/guia/`.
- [ ] WhatsApp abre com o numero correto.
- [ ] Google Maps abre o endereco correto.
- [x] HTTPS esta ativo no Render.
- [ ] Backup foi configurado.
- [ ] QR Codes foram gerados usando o dominio publico.
