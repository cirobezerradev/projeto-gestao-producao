# Controle de Produção

Aplicação de terminal para registrar e acompanhar a produção por setor. O projeto reúne operações de cadastro, consulta e análise em uma interface simples, com persistência local em SQLite.

![Python 3](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Testes](https://img.shields.io/badge/Testes-unittest-2E8B57)

## Visão geral

O sistema foi desenvolvido para acompanhar registros de produção e rejeição, organizados por setor. A interface orienta o usuário por um menu interativo, enquanto o módulo de persistência mantém os dados em um banco SQLite local.

### Recursos

- Cadastro de registros de produção por setor.
- Listagem e consulta de registros pelo identificador.
- Atualização parcial: campos deixados em branco preservam os valores atuais.
- Exclusão de registros existentes.
- Indicadores consolidados de peças produzidas, rejeitadas e taxa de rejeição.
- Inicialização automática do banco e da tabela quando o programa é executado.
- Testes automatizados isolados do banco de dados utilizado no dia a dia.

## Tecnologias

- **Python 3** para a aplicação e a suíte de testes.
- **SQLite** para armazenamento local, usando o módulo `sqlite3` da biblioteca padrão.
- **unittest** para testes automatizados, também incluído na biblioteca padrão.

Não é necessário instalar dependências externas.

## Começar

Certifique-se de que o Python 3 está instalado. Na pasta do projeto, inicie a aplicação:

```bash
python3 main.py
```

O banco `producao_db` fica na raiz do projeto. Se o arquivo ou a tabela ainda não existir, a aplicação os cria automaticamente. O arquivo fornecido no projeto contém dados demonstrativos.

## Menu da aplicação

| Opção | Ação |
| --- | --- |
| `1` | Cadastrar registro de produção |
| `2` | Listar registros |
| `3` | Consultar registro por ID |
| `4` | Atualizar registro |
| `5` | Excluir registro |
| `6` | Exibir indicadores de produção |
| `0` | Encerrar a aplicação |

Para atualizar um registro, informe o ID e preencha apenas os campos que deseja alterar. Pressione **Enter** nos demais campos para manter os valores atuais. Valores numéricos, inclusive `0`, são tratados como alterações quando digitados.

## Banco de dados

O arquivo SQLite `producao_db` contém a tabela `producao`:

| Coluna | Tipo | Regra |
| --- | --- | --- |
| `id` | `INTEGER` | Chave primária com incremento automático |
| `setor` | `TEXT` | Obrigatório |
| `pecas_produzidas` | `INTEGER` | Obrigatório |
| `pecas_rejeitadas` | `INTEGER` | Obrigatório |
| `custo_unitario` | `REAL` | Obrigatório |

A taxa de rejeição exibida é calculada como `peças rejeitadas / peças produzidas × 100`. Quando não há peças produzidas, a taxa é `0%`.

## Testes

Execute a suíte automatizada com:

```bash
python3 -m unittest discover -v
```

Os testes cobrem cadastro, listagem, consulta, atualização parcial, exclusão e indicadores. Cada caso usa um banco temporário, mantendo os dados de `producao_db` intactos.

## Estrutura do projeto

```text
.
├── database.py       # Conexão SQLite e operações de persistência
├── main.py           # Menu interativo e fluxo da aplicação
├── producao_db       # Banco SQLite com dados demonstrativos
├── test_database.py  # Testes automatizados
└── README.md         # Documentação do projeto
```