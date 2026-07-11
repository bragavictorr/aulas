nota = float(input("digite uma nota : "))

while (nota < 0 or nota > 10) and nota != None:
    print("ERRO: digite uma nota: ")
    nota = float(input("digite uma nota"))