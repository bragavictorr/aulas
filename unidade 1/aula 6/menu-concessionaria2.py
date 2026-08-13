#importações

# Variáveis globais

# desclarações de Funções

# Resto do programa

def exibir_menu_infantil():
    menu_infantil = ["Relampago marquinhos","hotwheels","patrulha Canina","thomas e seus amigos"]

    for index, item in enumerate(menu_infantil):
        print(f"{index+1}-{item}")

def exibir_menu_normal():
    menu_adulto = ["Toyota -> À partir de R$ 180.000","Mercedez -> À partir de R$300.000","Fiat -> À partir de R$ 70.000"]
    for index, item in enumerate(menu_adulto):
        print(f"{index+1}-{item}")
   

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