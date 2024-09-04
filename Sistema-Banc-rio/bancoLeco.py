menu= """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Saldo
[5] Sair
=> """
limite=500
extrato=""
LIMITE_DIARIO=3
saques=0
saldo=0
while True:
    opcao=input(menu)
    if opcao=="1":
        deposito=float(input('Qual o valor que deseja depositar?: R$'))
        if deposito<0:
            print('Operação Inválida')
        else:
            saldo+=deposito
            extrato+=f"Depósito: R$ {deposito:.2f}\n"
            print(f"Saldo: R${saldo:.2f}")
    
    elif opcao=="2":
        valor_de_saque=float(input('Qual valor deseja sacar? R$'))

        if valor_de_saque > saldo:
            print('Operação Inválida! Saldo insuficiente.')
        else:
            saques+=1
            extrato+=f"Saque: R$ {valor_de_saque:.2f}\n"

            if valor_de_saque>limite:
                print('Você atingiu o seu limite diário!')
                break

            if saques>LIMITE_DIARIO:
                print('Você atingiu o seu limite diário!')
            else:
                saldo-=valor_de_saque
                print (f"O valor de R${valor_de_saque:.2f} foi sacado")
                print('Saques:{} '.format(saques))

    elif opcao=="3":
        print('>='*10,'Extrato', '<='*10)
        print(extrato)
        print(f"Saldo: R${saldo:.2f}")
        print('>='*20)
        if saldo==0:
            print('Nenhuma ação foi feita')

    elif opcao=="4":
        print(f"Saldo: R${saldo:.2f}")

    else:
        print('Volte Sempre')
        break    