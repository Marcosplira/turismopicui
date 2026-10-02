# Documentação de entrega e funcionamento do sistema - Turismo de Picuí

## 1. Visão geral do software

O sistema foi desenvolvido para centralizar o processo de cadastro, análise e divulgação de empreendimentos turísticos do município de Picuí. Ele conecta três partes principais:

- empreendedor: cadastra o empreendimento e envia dados e fotos;
- administração: revisa os cadastros e aprova ou reprova a divulgação;
- público: consulta o guia turístico com informações aprovadas.

Em termos de negócio, o software resolve um problema real: organizar em um único ambiente os dados dos empreendimentos locais, facilitar a análise pela prefeitura e melhorar a visibilidade dos negócios para moradores e turistas.

## 2. Objetivo do sistema para o gerente

O gerente precisa acompanhar o processo de forma simples e objetiva. O sistema foi pensado para permitir:

- receber novos cadastros de empreendimentos;
- revisar informações cadastrais;
- validar fotos e dados de contato;
- aprovar ou reprovar os registros;
- manter o guia municipal atualizado;
- reduzir o trabalho manual e a dispersão de informações em mensagens ou planilhas.

## 3. Como o software funciona

### Fluxo do empreendedor

1. O empreendedor acessa a página de cadastro.
2. Preenche os dados do empreendimento, responsável, endereço, categoria e contatos.
3. Envia fotos do local ou serviço.
4. Aceita o aviso de privacidade.
5. O sistema salva o cadastro e marca como pendente.
6. O cadastro passa para análise administrativa.

### Fluxo da administração

1. O gerente ou a equipe responsável acessa o painel administrativo.
2. Visualiza todos os empreendimentos cadastrados.
3. Revê nome, responsáveis, endereço, telefone, email, fotos e categoria.
4. Aprova ou reprova o registro.
5. O status do empreendimento muda para aprovado ou reprovado.

### Fluxo do público

1. Usuários acessam o guia turístico.
2. A busca e os filtros ajudam a encontrar empreendimentos por categoria, nome e zona.
3. Apenas os cadastros aprovados são exibidos.
4. O visitante pode ver fotos, dados de contato, WhatsApp e localização.

## 4. Funcionamento do painel administrativo

O painel administrativo permite:

- consultar todos os registros;
- filtrar por zona, categoria e status;
- pesquisar por nome, responsável, telefone e email;
- visualizar fotos e informações do empreendimento;
- aprovar ou reprovar em lote;
- manter as categorias organizadas.

Esse painel é o centro de operação do gerente, porque é nele que as decisões de divulgação são tomadas.

## 5. O que o gerente acompanha no dia a dia

O gerente deve acompanhar principalmente:

- quantos cadastros chegaram;
- quantos estão pendentes;
- quantos foram aprovados;
- quantos foram rejeitados;
- quais categorias têm mais demanda;
- se há falta de dados ou fotos incompletas.

Com isso, a prefeitura consegue administrar melhor a divulgação turística do município.

## 6. Benefícios do sistema

- organização dos dados em um único sistema;
- redução de falhas por cadastro disperso;
- melhora na comunicação com empreendedores;
- controle de aprovação da equipe da prefeitura;
- acesso rápido do público ao guia turístico;
- ambiente mais profissional para a gestão do turismo local.

## 7. Acesso ao sistema

### Local

- Home: http://127.0.0.1:8001/
- Cadastro: http://127.0.0.1:8001/cadastro/
- Guia público: http://127.0.0.1:8001/guia/
- Administração: http://127.0.0.1:8001/admin/
- Dashboard do gerente: http://127.0.0.1:8001/cadastro/dashboard-gerente/

### Produção

- Site: https://turismo-picui.onrender.com/
- Administração: https://turismo-picui.onrender.com/admin/
- Dashboard do gerente: https://turismo-picui.onrender.com/cadastro/dashboard-gerente/

## 8. Usuário administrativo

O painel e o dashboard são restritos a usuários da equipe com permissão de acesso administrativo (`is_staff`). Para criar um usuário administrador no ambiente local:

```powershell
python manage.py createsuperuser
```

O banco local e o banco PostgreSQL do Render são separados. Usuários e senhas criados localmente não são copiados para produção. Os comandos abaixo só alteram o ambiente no qual o Django está conectado; execute-os em um shell conectado ao banco de produção, nunca suponha que o terminal local altera o Render.

Para criar o primeiro administrador de produção, execute no ambiente conectado ao banco do Render:

```bash
python manage.py createsuperuser
```

Para redefinir a senha de um administrador existente nesse mesmo ambiente:

```powershell
python manage.py changepassword nome_do_usuario
```

Use uma senha forte e exclusiva. Não coloque credenciais em arquivos do projeto, documentação, GitHub ou mensagens. Depois do login, abra o Dashboard do gerente pelo link de produção acima.

## 9. E-mail e alertas

O sistema envia notificações por e-mail para:

- responsável pelo cadastro;
- administrador do projeto/prefeitura.

Essas mensagens avisam que houve um novo empreendimento em análise e ajudam a reduzir demora na resposta.

## 10. Segurança e boas práticas

- manter a chave secreta em variável de ambiente;
- usar DEBUG em False em produção;
- não publicar senhas dentro do código;
- manter backups do banco;
- controlar acessos ao painel administrativo;
- criar usuários administrativos diretamente no ambiente de produção, sem reutilizar credenciais padrão;
- configurar armazenamento permanente de fotos em produção.

## 11. Checklist para entrega ao gerente

- [x] Sistema funcionando localmente
- [x] Cadastro do empreendedor acessível
- [x] Guia público com informações aprovadas
- [x] Painel administrativo para revisão
- [x] E-mails de confirmação e alerta
- [x] Organização por categorias e status
- [x] Estrutura pronta para apresentação ao cliente

## 12. Observação final

O software foi construído para ser um sistema prático de gestão do turismo local. Ele não é apenas um formulário; ele é uma ferramenta operacional para a gestão de empreendimentos, o controle das aprovações e a divulgação municipal dos serviços turísticos.

Com a utilização correta do painel administrativo e da rotina de aprovação, o gerente passa a ter uma visão mais organizada e profissional do setor turístico da cidade.
