import os
import random
import unicodedata
from decimal import Decimal
import django

# Configuração do ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minicrm.settings')  # Altere para o nome do seu projeto
django.setup()

from core.models import Cliente  # Altere para o nome do seu app

NOMES = [
    'Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo', 'Fernanda', 'Gabriel', 'Helena',
    'Igor', 'Juliana', 'Lucas', 'Mariana', 'Nicolas', 'Olivia', 'Paulo', 'Rafaela',
    'Samuel', 'Tatiane', 'Vinicius', 'Yasmin'
]

SOBRENOMES = [
    'Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira',
    'Lima', 'Gomes', 'Costa', 'Ribeiro', 'Martins', 'Carvalho', 'Almeida', 'Lopes'
]

DOMINIOS = ['gmail.com', 'outlook.com', 'empresa.com.br', 'uol.com.br', 'techcorp.io']
STATUS_OPCOES = ['negociacao', 'fechado', 'perdido']

def normalizar_str(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

TOTAL = 120
BATCH_SIZE = 100
clientes = []

for i in range(1, TOTAL + 1):
    p_nome = random.choice(NOMES)
    s_nome = random.choice(SOBRENOMES)
    nome_completo = f'{p_nome} {s_nome}'
    
    email_user = f'{normalizar_str(p_nome)}.{normalizar_str(s_nome)}{i}'
    email = f'{email_user}@{random.choice(DOMINIOS)}'
    
    ddd = random.choice(['11', '21', '22', '31', '41', '51', '61'])
    numero = f'9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}'
    telefone = f'({ddd}) {numero}'
    
    valor = Decimal(str(round(random.uniform(1500.0, 75000.0), 2)))
    status = random.choice(STATUS_OPCOES)

    clientes.append(
        Cliente(
            nome=nome_completo[:50],
            email=email,
            telefone=telefone,
            valor_proposta=valor,
            status=status
        )
    )

Cliente.objects.bulk_create(clientes, batch_size=BATCH_SIZE)
print(f'Sucesso: {len(clientes)} clientes inseridos via bulk_create.')