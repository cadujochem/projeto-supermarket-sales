import pandas as pd
from sqlalchemy import create_engine

# 1. Configurações de Conexão com o PostgreSQL, Preencha as variaveis abaixo com os dados do seu banco
# Formato: postgresql://usuario:senha@host:porta/nome_do_banco


USUARIO = "postgres"
SENHA = "990957"  # <- Altere para a sua senha do PostgreSQL
HOST = "localhost"
PORTA = "5432"
BANCO = "supermarket_db"

conexao_url = f"postgresql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"


#Função para carregar os dados brutos do CSV para a tabela raw_vendas no PostgreSQL

def carregar_dados_raw():
    try:
        # Criar a engine de conexão com o SQLAlchemy
        engine = create_engine(conexao_url)
        
        # 2. Ler o arquivo CSV original da pasta data/raw/
        caminho_csv = "data/raw/supermarket_sales.csv"

        print(f"Lendo o arquivo CSV:")

        
        df_raw = pd.read_csv("data/raw/supermarket_sales.csv", encoding="utf-8")

        # 3. Mapear e renomear as colunas do CSV para corresponder à tabela raw_vendas (snake_case)
        mapeamento_colunas = {
            'Invoice ID': 'invoice_id',
            'Branch': 'branch',
            'City': 'city',
            'Customer type': 'customer_type',
            'Gender': 'gender',
            'Product line': 'product_line',
            'Unit price': 'unit_price',
            'Quantity': 'quantity',
            'Tax 5%': 'tax_5_percent',
            'Total': 'total',
            'Date': 'date',
            'Time': 'time',
            'Payment': 'payment',
            'cogs': 'cogs',
            'gross margin percentage': 'gross_margin_percentage',
            'gross income': 'gross_income',
            'Rating': 'rating'
        }
        df_raw.rename(columns=mapeamento_colunas, inplace=True)

        # 4. Inserir os dados na tabela raw_vendas no PostgreSQL
        # if_exists='append': insere os dados mantendo as regras e restrições da tabela criada previamente
        
        print("Inserindo dados brutos na tabela 'raw_vendas'...")
        
        df_raw.to_sql(
            name='raw_vendas',
            con=engine,
            if_exists='replace',
            index=False,
            chunksize=500  # Inserção em lotes para melhor desempenho
        )
        
        print(" Sucesso! Dados brutos carregados na tabela 'raw_vendas'.")

    except Exception as e:
        print(f" Erro ao carregar os dados no PostgreSQL: {e}")

if __name__ == "__main__":
    carregar_dados_raw()

