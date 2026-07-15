import os
# Operações básicas: Saque, Saldo, Deposito
# Operações avançadas: Login, Impressão de Recibo, Suporte, Cofrinho

saldo_inicial = 0
usuario = "joao"
senha = "1234"


def limpar():
    os.system("cls")

def saque(saldo):
    valor = int(input("Digite o valor desejado\n"))
    saldo -= valor
    return saldo

def deposito(saldo):
    valor = int(input("Digite o valor desejado\n"))
    saldo += valor
    return saldo

def cofrinho(saldo_cofrinho):
    valor = int(input("depositer seu saldo.\n"))
    saldo_cofrinho += valor
     
    
    for mes in range(1,13):
        montante = saldo_cofrinho*(1+0.01)
        saldo_cofrinho = montante
        print(f"o cofrinho rendu! Valor atual: {montante}")

    return saldo_cofrinho


def menu():
    saldo_inicial = 0
    saldo_cofrinho = 0 
    
    while True:
        
            escolha_usuario = int(input("Menu\n1-Saldo\n2-Saque\n3-Deposito\n4-cofrinho\n5-sair\n"))

            if escolha_usuario == 1:
                limpar()
                print(saldo_inicial)

            elif escolha_usuario == 2:
                saldo_inicial = saque(saldo_inicial)
                limpar()
                
            elif escolha_usuario == 3:
                saldo_inicial = deposito(saldo_inicial)
                limpar()

            elif escolha_usuario == 4:
                saldo_cofrinho = cofrinho(saldo_cofrinho)

            elif escolha_usuario == 5:
                limpar()
                print("Obrigado por usar o nosso sistema.")
                break
    



while True:
    usuario_digitado = input("insira o seu cartão.\n")
    if usuario_digitado == usuario:
        while True:
            senha_digitada = input("digite sua senha\n")
            if senha_digitada == senha:
                menu()
                break
            else:
                print("senha incorreta.")
        break
    else:
        print("conta inválida. Verifique se o cartão foi inserido corretamente e se a conta está ativa.\n")
