import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Iniciar Faker para Português Brasileiro
fake = Faker('pt_BR')

# 1. Definir categorias
categories = {
    "Mercado": ["Carrefour", "Pão de Açúcar", "Assai", "Mercearia Maria", "Shopper"],
    "Alimentação": ["Starbucks", "Z Deli", "Rascal", "McDonald's", "Churrascaria", "Coffee Lab", "Kotay Sushi"],
    "Transporte": ["Uber", "Taxi", "99APP", "Bilhere Único", "Posto Ipiranga", "Posto Shell", "Sem Parar"],
    "Compras": ["Amazon", "Mercado Livre", "Shopee", "Zara", "Lojas Renner"], 
    "Assinaturas": ["Netflix", "Apple Plus", "Spotify", "HBO Max", "Icloud"],
    "Contas": ["Conta de Luz - Enel", "Conta de Água - Sabesp", "Internet", "Aluguel"],
    "Renda": ["Salário", "Pagamento Freelance", "PIX Recebido"],
    "Saúde": ["Droga Raia", "Drogaria São Paulo", "Drogasil", "Bradesco Saúde", "Amil Saúde", "Academia", "Wellhub"],
    "Delivery": ["iFood", "99Food", "Rappi"]
}

# 2. Gerar Transações

data = []
num_transactions = 500 # Gerar 500 transações
start_date = datetime.now() - timedelta(days=365) # Um ano de dados

print(f"Gerando {num_transactions} transações fictícias")

for _ in range(num_transactions):
    category = random.choice(list(categories.keys()))
    description = random.choice(categories[category])

    # Atribuir valores com base na categoria 
    if category == "Renda":
        amount = round(random.uniform(2000, 10000), 2) * -1 # Negativo para renda
    elif category == "Compras":
        amount = round(random.uniform(50.0, 1000), 2)
    elif category == "Contas":
        amount = round(random.uniform(100.0, 6000), 2)
    elif category == "Mercado":
        amount = round(random.uniform(150.0, 3000.0), 2)
    else:
        amount = round(random.uniform(10.0, 500.0), 2)
    
    date = fake.date_between(start_date=start_date, end_date="now").strftime("%Y-%m-%d")

    data.append({
        "Date": date,
        "Description": description,
        "Category": category,
        "Amount": amount,
        "Account": random.choice(["Conta Corrente (..1234)", "Cartão Visa (..5678)", "Cartão Amex (..2005)"])
    })

    # 3. Criar DataFrame e ordenar por data
df = pd.DataFrame(data)
df = df.sort_values(by="Date", ascending=False)

    # 4. Salvar em CSV
output_file = "mock_transactions.csv"
df.to_csv(output_file, index=False)

print(f"Sucesso! Gerado '{output_file}' com {len(df)} linhas.")