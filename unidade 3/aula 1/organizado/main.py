import os
import shutil

pastas_e_aquirvos = {
    "Imagens":["png","jpeg","webp","jpg"],
    "Planilhas": ["xls","cvs","xlsx"],
    "documentos": ["docx","pdf", "txt"],
}



pasta_alvo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Bagunça"
)
lista_arquivos = os.listdir(pasta_alvo)

for chave in pastas_e_aquirvos.keys():
    caminho_pasta = os.path.join(pasta_alvo, chave)
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)

        

for arquivo in lista_arquivos:
    extensao = arquivo.split(".")[-1]
    for chave in pastas_e_aquirvos.keys():
        if extensao in pastas_e_aquirvos[chave]:
           Path_origem = os.path.join(pasta_alvo, arquivo)
           Path_destino = os.path.join(pasta_alvo, chave)
           shutil.move(Path_origem, Path_destino)

