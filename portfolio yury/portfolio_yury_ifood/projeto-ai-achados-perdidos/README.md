# Assistente IA para Achados e Perdidos

<sub>Protótipo de portfólio em desenvolvimento - não é um produto publicado.</sub>

## Problema

Ao registrar um objeto perdido ou encontrado, a pessoa pode descrevê-lo de formas diferentes. Isso dificulta padronizar os registros e localizar itens que talvez correspondam.

## Proposta

Uma interface recebe a descrição de um item. Um modelo de linguagem sugere uma categoria, reescreve a descrição de forma objetiva e extrai palavras-chave. Em seguida, uma lógica simples compara essas informações com registros de exemplo e apresenta possíveis correspondências.

## O que este protótipo demonstra

- Integração de uma aplicação Python com um LLM pela API oficial.
- Criação de endpoint HTTP com FastAPI.
- Engenharia de prompt com categorias e formato de saída definidos.
- Validação da resposta gerada antes de usá-la.
- Comparação transparente de candidatos por categoria e palavras-chave.
- Interface web simples consumindo a API.

## Arquitetura

```text
Navegador
   |
   | POST /api/analyze
   v
FastAPI ----> Serviço de IA / Responses API
   |
   v
Validação da saída
   |
   v
Comparação local por categoria e palavras-chave
   |
   v
Lista de possíveis correspondências
```

## Requisitos

- Python 3.11 ou superior.
- Uma chave de API da OpenAI com acesso a um modelo habilitado para a conta. O modelo pode ser configurado em `OPENAI_MODEL`.

## Executar localmente

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Abra `.env` e informe sua chave em `OPENAI_API_KEY`. Nunca publique esse arquivo. O modelo padrão pode ser alterado pela variável `OPENAI_MODEL`.

```powershell
uvicorn app.main:app --reload
```

Acesse `http://127.0.0.1:8000`. A documentação interativa da API fica em `http://127.0.0.1:8000/docs`.

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edite .env e configure OPENAI_API_KEY
uvicorn app.main:app --reload
```

## Testes

Os testes da lógica de correspondência não precisam de chave de API:

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

## Endpoint

`POST /api/analyze`

Exemplo de entrada:

```json
{
  "description": "Encontrei um estojo azul com duas canetas perto da biblioteca.",
  "candidate_items": [
    {
      "id": "item-01",
      "description": "Estojo azul com canetas encontrado no corredor da biblioteca.",
      "category": "Material escolar"
    }
  ]
}
```

A resposta contém a categoria sugerida, uma descrição padronizada, palavras-chave e os possíveis registros ordenados por pontuação.

## Limitações conhecidas

- Os registros candidatos são enviados pelo cliente para esta demonstração; ainda não existe banco de dados.
- A pontuação é uma heurística explicável, não uma probabilidade de que dois itens sejam iguais.
- A saída do LLM pode variar. A aplicação valida campos e categorias, mas o resultado sempre precisa de revisão humana.
- Não há autenticação, deploy ou persistência nesta versão.
- Não envie informações pessoais, documentos, telefones ou dados sensíveis para a demonstração.

## Próximas evoluções

1. Persistir itens em banco de dados.
2. Criar testes de integração para o endpoint e simular falhas do provedor.
3. Criar fluxo no n8n para receber um novo registro, executar a classificação e notificar um responsável.
4. Implantar uma demonstração pública com limites de uso e proteção de credenciais.

## Referência técnica

A integração usa a biblioteca Python oficial e a API Responses. Consulte a [documentação oficial da API](https://developers.openai.com/api/docs/quickstart) para verificar modelos disponíveis, credenciais e limites da sua conta.
