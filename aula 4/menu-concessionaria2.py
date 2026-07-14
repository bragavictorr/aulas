#importações

# Variáveis globais

# desclarações de Funções

# Resto do programa

def exibir_menu_infantil():
    print("Relampago marquinhos")
    print("hotwheels")
    print("patrulha Canina")
    print("thomas e seus amigos")

def exibir_menu_normal():
    print("Toyota -> À partir de R$ 180.000")
    print("Mercedez -> À partir de R$300.000")
    print("Fiat -> À partir de R$ 70.000")

def checar_idade(idade):
    if idade < 18:
        exibir_menu_infantil()
    else:
        exibir_menu_normal()

while True:
     idade = int(input("Digite sua idade ou digite 0 para sair:"))
     if idade == 0:
         break
     else:
         checar_idade(idade)