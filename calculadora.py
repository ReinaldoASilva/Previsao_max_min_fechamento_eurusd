# Calculadora

import os

print('=============')
Operations = {
    '0': 'Soma',
    '1': 'Subtração',
    '2': 'Multiplicação',
    '3': "Divisão",
    '4':"Exponenciação"
}

while True:
    os.system('Clear')
    i = 0
    for op, name in Operations.items():
        print(i, ':', name)
        i += 1
    print('')
    print('Escolha a operação que deseja realizar?')
    op = input()

    

input('Qual operação deseja realizar?')
if input == 0:
    print(">>> + Escolhida")        
    if input == 1:
        print (">>> - Escolhida")
    if input == 2:
        print('>>> * Escolhida')
    if input == 3:
        print ('>>> / Escolhida ')
    if input == 4:
        print(" >>> ** escolhido ")    


input(int('Qual o primeiro Valor?'))
input(int( 'Qual o segundo valor?'))