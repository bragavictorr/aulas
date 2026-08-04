import os
import ia
# Operações básicas: Saque, Saldo, Deposito
# Operações avançadas: Login, Impressão de Recibo, Suporte, Cofrinho

# Uma lista de usuários/senhas. Cada item da lista é uma outra lista com dois itens: o primeiro é o usuário, o segundo é a senha
usuarios_senhas = [["joao", "1234"],["carlos","2421"]]

# os.system interage com o CMD. É uma biblioteca, então é importada na linha 1 do código.
# cls é o comando para limpar o terminal
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

# Função para receber depósito e render 12 meses no cofrinho!
def cofrinho(saldo_cofrinho):
    valor = float(input("Digite o valor para adicionar:\n"))
    saldo_cofrinho += valor

    for mes in range(1,13):
        montante = saldo_cofrinho*(1+0.01)
        saldo_cofrinho = montante
        print(f"O cofrinho rendeu! Valor atual: {montante}")
    
    return saldo_cofrinho

def menu():
    saldo_inicial = 0
    saldo_cofrinho = 0

    while True:
        escolha_usuario = int(input("Menu\n1-Saldo\n2-Saque\n3-Deposito\n4-Cofrinho\n5-fala com suporte\n0-Sair"))

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
            ia.pergunta_na_IA()
            

        elif escolha_usuario == 0:
            limpar()
            print("Obrigado por usar o nosso sistema.")
            break
        
# Enquanto o usuário não digitar o nome do usuário correto, pedimos pra digitar novamente
while True:
    usuario_digitado = input("Insira o seu cartão.\n")
    # Para cada item na lista usuários e senhas... ou seja, usuario = ["joao", "1234"] na primeira iteração
    for usuario in usuarios_senhas:
        # Comparamos se usuario[0] é o que o nosso usuário digitou. Lembrando que usuario = ["joao", "1234"], então usuario[0] = "joao". Comparamos "joao" com o que foi digitado como usuário.
        if usuario[0] == usuario_digitado:
            # Enquanto o usuário não digitar a senha correta, pedimos pra digitar novamente
            while True:
                senha_digitada = input("Digite sua senha\n")
                # Comparamos se usuario[1] é o que nosso usuário digitou. Lembrando que usuario = ["joao", "1234"], então usuario[1] = "1234". Comparamos "1234" com o que foi digitado como senha.
                if usuario[1] == senha_digitada:
                    # Se tudo estiver correto, entra no programa
                    menu()
                    # Depois de executar todo o menu, usamos o break para encerrar
                    break
                else:
                    print("Senha incorreta.")
            break
        else:
            print("Conta inválida. Verifique se o cartão foi inserido corretamente e se a conta está ativa.")