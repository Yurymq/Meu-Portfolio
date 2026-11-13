# Roadmap do portfólio

Este roteiro separa o que já existe do que ainda precisa ser construído.

## 1. Finalizar o protótipo de IA

- [x] Criar uma chave de API e armazená-la somente no arquivo `.env` local.
- [x] Executar a aplicação localmente e testar descrições curtas, longas e ambíguas.
- [x] Validar a resposta do modelo e tratar erros de autenticação, limite e indisponibilidade.
- [x] Adicionar testes para a lógica de comparação de itens.
- [ ] Incluir capturas de tela reais da aplicação funcionando.
- [ ] Publicar uma demonstração ou vídeo curto; nunca enviar a chave de API ao GitHub.

## 2. Demonstrar automação de ponta a ponta

- [x] Criar um fluxo no n8n: novo item recebido -> chamada da API de classificação -> registro do resultado -> notificação de um responsável.
- [ ] Registrar o desenho do fluxo e explicar o que acontece quando uma etapa falha.
- [ ] Medir o tempo do processo manual e automatizado em um teste real. Publicar somente números medidos.

## 3. Demonstrar construção de produto

- [ ] Melhorar a interface com estados de carregamento, mensagens de erro e acessibilidade.
- [ ] Adicionar persistência de dados e validação no backend, caso o escopo do projeto exija.
- [ ] Adicionar testes de API e instruções para reproduzir o ambiente.
- [ ] Fazer deploy e colocar o link da demonstração no README.

