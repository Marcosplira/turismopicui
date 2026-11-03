# Guia do usuário — Turismo de Picuí

Guia prático para visitantes, empreendedores e equipe responsável pela gestão do sistema.

## 1. Endereços principais

O site público atualmente documentado é:

- **Página inicial:** https://turismopicui.pythonanywhere.com/
- **Guia de empreendimentos:** https://turismopicui.pythonanywhere.com/guia/
- **Mapa:** https://turismopicui.pythonanywhere.com/mapa/
- **Cadastro de empreendimento:** https://turismopicui.pythonanywhere.com/cadastro/
- **Acesso da equipe:** link “Acesso da equipe” na página inicial
- **Administração:** https://turismopicui.pythonanywhere.com/admin/
- **Dashboard do gerente:** https://turismopicui.pythonanywhere.com/dashboard-gerente/

> Se o sistema for transferido para outro domínio/VPS, substitua os endereços por aqueles aprovados pela equipe de TI. A publicação em VPS não muda o endereço acima automaticamente.

## 2. Para visitantes

### Encontrar um empreendimento

1. Abra o Guia.
2. Use a busca por nome, atividade ou bairro.
3. Use as categorias e os filtros de localização para reduzir os resultados.
4. Abra o cartão para ver detalhes, fotos e contatos disponíveis.
5. Se o empreendimento tiver WhatsApp ou localização, use os links apresentados na página.

O Guia público apresenta somente empreendimentos aprovados pela equipe. Um cadastro pendente ou reprovado não deve aparecer como opção pública.

### Usar o mapa

1. Abra **Mapa** na página inicial ou o endereço do mapa.
2. Use os filtros **Todos**, **Zona Urbana**, **Comunidade Rural** ou **Geossítios & Ecoturismo**.
3. Para exibir apenas os geossítios, clique em **Destacar Geossítios no Mapa**.
4. Para retornar, clique em **Mostrar todos os pontos** ou em **Todos**.
5. Nos cartões, clique em **Ver no mapa** ou **Ver ponto** para focar e abrir o ponto.
6. Para desfazer o foco, clique novamente no botão do ponto, agora identificado como **Voltar ao mapa completo**, ou use **Mostrar todos os pontos**.

O mapa usa tiles ArcGIS/Esri e não precisa de uma chave do Google. O mapa base depende de um serviço externo e pode não carregar em redes que bloqueiem esse serviço. As coordenadas de pontos não confirmadas devem ser verificadas pela equipe antes de orientar uma visita.

## 3. Para empreendedores: cadastrar um estabelecimento

1. Abra **Cadastro de empreendimento**.
2. Preencha identificação do empreendimento, responsável, CPF e, quando aplicável, CNPJ.
3. Informe zona, endereço, bairro/comunidade e ponto de referência.
4. Adicione telefone, WhatsApp e e-mail atualizados.
5. Escolha as categorias corretas e complete a descrição e demais informações relevantes.
6. Informe somente dados verdadeiros e atualizados. Marque as autorizações e leia o aviso de privacidade antes de concordar.
7. Anexe fotos permitidas pelo formulário. O sistema limita cada foto a 5 MB e aceita JPG/JPEG, PNG ou WEBP.
8. Envie o formulário e aguarde a confirmação.

Ao enviar, o registro fica **pendente de análise**. O envio não significa aprovação nem publicação automática. Se houver erro, revise os campos destacados e envie novamente.

O sistema pode avisar que um e-mail de notificação não foi enviado. Nessa situação, o cadastro pode ter sido salvo mesmo assim; anote o nome do empreendimento e entre em contato com a equipe para confirmar, sem reenviar várias vezes.

### Consultar o status

Após o envio, a página de sucesso oferece o link **Acessar meus dados**. A sessão do mesmo navegador pode mostrar o cadastro recém-enviado. O acompanhamento por conta depende de estar autenticado com o usuário proprietário; em caso de dúvida, contate a equipe e informe o nome do empreendimento e a data do cadastro. Não envie CPF em canais públicos.

Os status possíveis:

- **Pendente:** recebido e aguardando análise.
- **Aprovado:** autorizado pela equipe para divulgação no Guia.
- **Reprovado:** não aprovado para divulgação neste momento; contate a equipe se precisar de orientação.

## 4. Para gerente e equipe: rotina de análise

### Acessar com segurança

1. Na página inicial, clique em **Acesso da equipe** ou abra o Dashboard do gerente.
2. Entre com sua conta institucional autorizada.
3. Se a conta não tiver permissão administrativa, solicite acesso ao responsável técnico. Não compartilhe senhas entre funcionários.
4. Ao terminar, use **Sair** e feche o navegador em computadores compartilhados.

Dashboard e Administração são áreas restritas. Não tente contornar a autenticação nem use uma conta pessoal compartilhada.

### Ler o Dashboard

O Dashboard apresenta:

- total de registros e quantidades de aprovados, pendentes e reprovados;
- cadastros aguardando análise e alertas de dados incompletos;
- busca por nome, responsável ou telefone;
- filtros por status;
- gráficos de categorias, zonas e situação;
- links para relatório executivo e CSV.

Use **Revisar Pendentes Agora** ou o filtro **Pendentes** para priorizar novos cadastros.

### Revisar, aprovar ou reprovar

Antes de aprovar, confira:

- nome e tipo de atividade;
- dados do responsável e forma de contato;
- endereço e bairro/comunidade;
- categoria e descrição;
- fotos, se enviadas;
- autorização de divulgação e adequação do conteúdo;
- se o ponto do mapa representa localização real ou apenas estimada.

No cartão do Dashboard, a ação rápida **Aprovar** publica o registro aprovado no Guia. **Reprovar** retira o registro da divulgação pública. Essas ações alteram o status imediatamente; revise o cadastro antes de clicar.

Para fazer uma conferência detalhada ou ajustar informações, clique em **Editar** para abrir o registro no Admin. O Admin também permite filtrar, pesquisar e aplicar ações a registros selecionados; ações em lote exigem cuidado porque podem alterar mais de um cadastro.

Registros reprovados podem ser reavaliados e aprovados posteriormente. Confirme dados e autorização novamente antes de reaprovar.

### Acompanhar a publicação

Depois de aprovar:

1. Confirme que o contador e o status no Dashboard foram atualizados.
2. Abra **Visualizar Guia Público** em outra aba.
3. Pesquise o empreendimento e confira descrição, categoria, contato e fotos.
4. Abra o mapa quando a localização for relevante e confirme se o posicionamento é confiável.

Não prometa e-mail de aprovação em todos os casos: a disponibilidade depende do SMTP e do caminho usado para alterar o status. Confira a mensagem exibida e o log/suporte técnico quando uma notificação for importante.

## 5. Relatórios, planilhas e dados pessoais

- **Relatório oficial:** abre a visão executiva para conferência e impressão em PDF pelo navegador.
- **Planilha CSV:** exporta todos os registros, incluindo status e dados pessoais como CPF, CNPJ e contatos.

O CSV é restrito à equipe. Salve-o somente em local institucional protegido, limite os destinatários e apague cópias temporárias conforme a política de retenção da organização. Não publique ou encaminhe a planilha em grupos abertos.

## 6. Administração de conteúdo

O Admin permite manter empreendimentos, categorias, fotos e depoimentos. Depoimentos só devem ser publicados com autorização e texto validado. Não use depoimentos, nomes, imagens ou empreendimentos demonstrativos como declarações reais sem confirmar origem e consentimento.

Alterações de cadastro, categorias, aprovação e depoimentos devem seguir as regras internas da Secretaria de Turismo. Não exclua dados históricos sem autorização e backup.

## 7. Segurança e privacidade

- CPF, CNPJ, telefone e e-mail são dados restritos.
- Use senha individual forte; não a envie por mensagem ou planilha.
- Evite acessar o painel em Wi-Fi público; sempre confira o HTTPS e o domínio.
- Não compartilhe capturas de tela com dados pessoais visíveis.
- Para corrigir ou remover um dado, contate a equipe administrativa conforme a política institucional.
- Em caso de suspeita de acesso indevido ou exposição de dados, avise imediatamente o responsável técnico e a gestão.

## 8. Problemas comuns

| Problema | O que fazer |
|---|---|
| Não consigo entrar no Dashboard | Confirme o endereço e a conta autorizada; peça ao administrador para verificar `is_staff`/permissões. |
| Cadastro não aparece no Guia | Verifique se foi aprovado; pendentes e reprovados não são públicos. |
| Cadastro foi enviado, mas o e-mail não chegou | O envio de e-mail depende do SMTP. Confirme o cadastro no painel antes de enviar novamente. |
| Foto não é aceita | Confira o formato permitido e limite de 5 MB por imagem. |
| Mapa sem imagem de fundo | Atualize a página e confira a conexão/rede; o mapa depende do provedor externo. Use os cartões de pontos enquanto ele estiver indisponível. |
| “Ver ponto” ou destaque continua ativo | Use **Mostrar todos os pontos**; para desfazer um foco, clique novamente em **Voltar ao mapa completo**. |
| Planilha não abre com acentos | Abra o CSV pelo Excel/LibreOffice e escolha UTF-8 ou solicite ao suporte uma exportação orientada. |

Ao solicitar suporte, informe a página, o horário aproximado, o navegador e uma descrição do que ocorreu. Nunca envie senha, CPF completo ou arquivo de backup em um chamado aberto.

## 9. Contatos operacionais

Os responsáveis institucionais devem completar antes da entrega:

- **Responsável do sistema:** [preencher nome/setor]
- **Suporte técnico / hospedagem:** [preencher canal institucional]
- **Responsável por privacidade e dados:** [preencher nome/setor]
- **Prazo de atendimento e horário de suporte:** [definir com a gestão]

Não publique contatos pessoais sem autorização.

## 10. Checklist diário do gerente

- [ ] Abrir o Dashboard usando conta autorizada.
- [ ] Conferir cadastros pendentes e alertas.
- [ ] Revisar dados e autorização antes de aprovar.
- [ ] Verificar no Guia o conteúdo aprovado.
- [ ] Usar CSV/relatório somente quando necessário e armazená-los com segurança.
- [ ] Sair do sistema em dispositivo compartilhado.