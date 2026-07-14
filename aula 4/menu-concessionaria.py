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

idade1 = 17
idade2 = 43
idade3 = 37
idade4 = 25
idade5 = 5

checar_idade(idade1)
checar_idade(idade2)
checar_idade(idade3)
checar_idade(idade4)
checar_idade(idade5)

