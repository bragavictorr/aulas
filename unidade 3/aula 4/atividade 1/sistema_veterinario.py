# Isso é uma superclasse! Ela tem vários atributos que as subclasses tem em comum.
# Isso é herança.
class Animal:
    def __init__ (self, nome, peso, idade):
        self.nome = nome
        self.peso = peso
        self.idade = idade
        self.esta_internado = False
    
    def medicar(self):
        print("Animal recebeu uma dosagem de remédio.")
    
    def internar(self):
        self.esta_internado = True
        print(f"O {self.nome} foi internado.")

    def receber_alta(self):
        self.esta_internado = False
        print(f"O {self.nome} recebeu alta.")

# Isso é uma subclasse. Todo cachorro é um animal.
class Cachorro(Animal):
    def __init__(self, nome, peso, idade):
        # Isso aqui pega os dados do Cachorro e leva pra classe Animal criar o objeto
        super().__init__(nome, peso, idade)
    
    # Só o cachorro recebe tosa. Por isso, definimos na subclasse
    def receber_tosa(self):
        print("Cachorro foi tosado.")
    
    # Cada animal recebe uma medicação diferente. Por isso fizemos override (sobrescrição)
    def medicar(self):
        print("Cachorro recebeu uma dosagem grande de remédio.")

# Isso é uma subclasse. Todo periquito é um animal.
class Periquito(Animal):
    def __init__(self, nome, peso, idade):
        # Isso aqui pega os dados do Periquito e leva pra classe Animal criar o objeto
        super().__init__(nome, peso, idade)
    
    # Cada animal recebe uma medicação diferente. Por isso fizemos override (sobrescrição)
    def medicar(self):
        print("Periquito recebeu uma dosagem pequena de remédio.")

novo_cachorro = Cachorro("Pepeu", 30, 10)
novo_periquito = Periquito("Cocota", 0.5, 5)

novo_cachorro.internar()
novo_periquito.internar()

# Todos tem o mesmo método, mas implementado de uma maneira diferente. Isso é polimorfismo.
novo_cachorro.medicar()
novo_periquito.medicar()
