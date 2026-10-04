Markdown

# 🛒 Análise de Vendas de Supermercados (Supermarket Sales)

## Sobre o Projeto

Este projeto consiste na construção de um pipeline de dados estruturado para analisar os registos de vendas de uma rede de supermercados. O fluxo integra o armazenamento de dados brutos num banco de dados relacional (PostgreSQL) e a utilização do ecossistema Python (Pandas, Matplotlib, Seaborn) para realizar processos de ETL (Extração, Transformação e Carga) e Análise Exploratória.

A estrutura foi elaborada dividindo os dados nas seguintes camadas:

* **Camada Raw (Bruta):** Dados originais mantidos sem alterações no banco de dados.
* **Camada Tratada (Processed):** Dados limpos, tipados e com novas colunas derivadas de regras de negócio.
* **Camada Gold (Resultados):** Geração de relatórios com estatísticas descritivas e visualizações gráficas.

## Tecnologias Utilizadas

* **Linguagens:** Python 3, SQL
* **Banco de Dados:** PostgreSQL
* **Bibliotecas Python:** `pandas`, `sqlalchemy`, `psycopg2-binary`, `matplotlib`, `seaborn`
* **Ferramentas:** DBeaver / pgAdmin, Git, GitHub

## Estrutura de Diretórios

```text
projeto-supermarket-sales/
├── data/
│   ├── processed/          # CSV com dados limpos e tratados
│   └── raw/                # CSV original com dados brutos
├── resultados/
│   ├── estatisticas/       # Relatório de texto com as respostas de negócio
│   └── graficos/           # Imagens dos gráficos gerados
├── sql/
│   ├── 01_criar_banco.sql      # Script de criação do banco de dados
│   ├── 02_criar_tabelas.sql    # Script com a estrutura das tabelas Raw e Tratada
│   └── 03_consultas.sql        # Script SQL com consultas de análise exploratória
├── src/
│   ├── 01_leitura_dados.py     # Script para carregar o CSV original no PostgreSQL
│   ├── 02_etl_vendas.py        # Limpeza, tipagem e transformação dos dados
│   └── 03_estatistica.py       # Estatística descritiva e geração de gráficos
├── .gitignore              # Ficheiros ignorados pelo versionamento
├── README.md               # Documentação do projeto
└── requirements.txt        # Dependências do projeto

Como Executar o Projeto

1. Preparação do Banco de Dados
Execute o script sql/01_criar_banco.sql no seu servidor PostgreSQL ou execute os comandos passo a passo criando um script 
no seu banco de dados.

Conecte-se ao banco supermarket_db que acabou de ser criado e execute o 
script sql/02_criar_tabelas.sql para gerar a estrutura das tabelas.

2. Configuração do Ambiente Python
Crie um ambiente virtual e/ou instale as dependências:

Bash
pip install -r requirements.txt
(Nota: Lembre-se de configurar as credenciais nas variáveis identificadas como CONEXÃO nos ficheiros 
dentro da pasta "src/01_leituradados.py", com a senha e informações do seu banco de dados local).

3. Execução do Pipeline de Dados
Execute os scripts na seguinte ordem no seu terminal:

Passo 1: python src/01_leitura_dados.py  - (Carga Raw) - Faz leitura do arquivo CSV disponibilizado e salva no banco de dados.

Passo 2 (ETL e Tratamento): python src/02_etl_vendas.py - Faz leitura dos dados do banco, efetua tratamento e limpeza e
salva no banco supermarket_db na tabela vendas_tratadas.  Também salva em um arquivo CSV em /data/processed/vendas_tratadas.csv

Passo 3 (Análises e Gráficos): python src/03_estatistica.py - Efetua, consultas, filtros e monta gráficos 
para responder os questionamentos relacionado ao negócio.



Perguntas de Negócio Respondidas

O projeto extrai de forma automatizada as respostas para questões fundamentais da rede de supermercados, tais como:

Qual filial apresentou o maior faturamento?

Qual filial realizou a maior quantidade de vendas?

Qual linha de produto apresentou o maior faturamento?

Qual linha de produto recebeu a melhor avaliação média?

Qual foi a forma de pagamento mais utilizada?

Qual foi o valor médio das vendas?

Qual foi a maior venda registrada?

Em qual dia da semana ocorreu a maior quantidade de vendas?

Os resultados detalhados ficam disponíveis em resultados/estatisticas/respostas_negocio.txt.




---
```
