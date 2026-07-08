salario = float(input("DIGITE O SEU SALARIO"))

desconto_vale_transporte = salario * 0.06

desconto_plano_saude = salario * 0.03

salario_liquido = salario - desconto_plano_saude - desconto_vale_transporte

print("desconto vale transporte:" , desconto_vale_transporte)
print