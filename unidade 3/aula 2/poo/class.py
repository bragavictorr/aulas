celular = input("digite o modelo do seu celular")
cor = input("digiter a cor")
armazenamento = input("digite o armazenamento")
memoria_ram = input("digite a memoria ram")




class Celular:
    def __init__(self, modelo, cor, armazenamento, memoria_ram):
        self.modelo = modelo
        self.cor = cor
        self.armazenamento = armazenamento
        self.memoria_ram = memoria_ram
    

    def exibir_info(self):
        print("seu modelo adicionado foi : " + celular)
        print("cor  do : " + celular + cor)
        print( "armazenamento do : " +  celular + armazenamento, "GB")
        print(" memoria_ram do :  " + celular + memoria_ram, "GB")


    def ligaçao (self):
        print("seu item foi adicionado com sucesso!!")
       



celular2 = Celular(cor, celular,armazenamento , memoria_ram )
celular1= Celular("sansung", "azul", 512, 32 )

celular2.exibir_info()
celular2.ligaçao()


