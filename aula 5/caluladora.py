


def soma(num1,num2):
    resultado_somatorio = num1 + num2
    return resultado_somatorio

def subtraçao(num1,num2):
    resultado_somatorio = num1 - num2
    return resultado_somatorio

def multiplicaçao(num1, num2):
    resultado_somatorio = num1 * num2
    return resultado_somatorio

def divisão(num1,num2):
    resultado_somatorio = num1 / num2
    return resultado_somatorio

def potencia(num1):

    resultado_somatori = num1*num1
    return resultado_somatori

operaçoes2 = ["*","-","+","/"]

while True:
    try:
        opereçoes = input("escolhar sua operaçao")
        if opereçoes not in operaçoes2:
            print ("digiter novamente")
            continue
        resultado = float(input("digite seu numero"))
        resultado2 = float(input("digite o outro numero"))
        


        if opereçoes == "+":
            print("soma:",soma(resultado,resultado2))

        elif opereçoes == "-":
            print("subtraçao:", subtraçao(resultado,resultado2))
        
        elif opereçoes == "*":
            print("multiplicaçao:" , multiplicaçao(resultado, resultado2))
        
        elif opereçoes == "/":
            print("divisão", divisão(resultado,resultado2))

        elif opereçoes == "^":
            print("potencia", potencia(resultado,resultado))

        else:
            print("operaçao não concluida")

    except(ValueError):
        print("erro tente novamente")
    except(ZeroDivisionError):
        print("Nao e possivel dividir por 0, Digiter outro numero.")
    except (Exception) as erro:
        print("Ocorreu um erro:", erro)

    
    

   



    


