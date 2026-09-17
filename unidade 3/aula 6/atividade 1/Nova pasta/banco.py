class Conta:
    def __init__(self, titula, numero):
        self.titula = titula
        self.numero = numero
        self.saldo = 0
    
    
    def sacar(self):
        valor = int(input("Digite o valor desejado\n"))
        if valor <= self.saldo:
            self.saldo -= valor
        
        else:
            print("você não tem saldo suficiente")
        
        
        return self.saldo
    
    def deposita(self):
        valor = int(input("Digite o valor desejado\n"))
        self.saldo += valor
        return self.saldo
    
    def __add__(self,  other):
        return self.saldo + other.saldo
    

class Conta_corrente(Conta):
    def __init__(self, numero, titula):
        super().__init__(numero, titula)
        self.limite_especial = 150
    def sacar(self):
        valor = int(input("Digite o valor desejado\n"))
        if valor <= self.saldo + self.limite_especial:
            self.saldo -= valor
        else:
            print("nao tem limite")




class Contapoupanca(Conta):
    def __init__(self, titula, numero ):
        super().__init__( titula, numero)
        self.rendimento = 0.05
    
    def aplica_rendimento(self):
        rendimento = self.saldo * self.rendimento
        self.saldo += rendimento
        return self.saldo
    


conta1 = Contapoupanca("joao", "1234")
conta2 = Contapoupanca("joao", " 32342")

conta1.aplica_rendimento()
print( conta1.saldo)
 
conta2.aplica_rendimento()
print( conta2.saldo)

print(conta1 + conta2)


while True:
        escolha_usuario = int(input("Menu\n1-Saldo\n2-Saque\n3-Deposito\n0-Sair"))

        if escolha_usuario == 1:
            print(f"saldo: R${conta1.saldo}")
        
        elif escolha_usuario == 2:
            conta1.sacar()
        
        elif escolha_usuario == 3:
            conta1.deposita()
        
        elif escolha_usuario == 4:
            break

        



