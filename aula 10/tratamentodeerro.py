from colorama import Fore, Style, init

try:
    print(x)
except(NameError):
    print("variavel X nao fou defenida")

except:
    print(Fore.YELLOW + "ocorreu um erro.")

