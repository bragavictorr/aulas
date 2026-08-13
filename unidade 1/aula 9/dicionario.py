carro = {
    "motor" : "v12",
    "banco" : " de couro esportivo",
    "volante": "de couro esportivo",
    "modelo" : "supra",
    "cor" : "roxo",
    "marca" : "nissan"
}

carro.update({"cor":"branco"})
del carro ["volante"]

lista_chaves = carro.keys()
for chaves in lista_chaves:
    print(chaves)