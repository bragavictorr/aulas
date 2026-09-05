import pyfiglet

frase = input("digite uma frase:")
frase_formatada =  pyfiglet.figlet_format(frase)

print(frase_formatada)