import textwrap

def menu():
    menu= """\n
    ===============MENU=================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tSaldo
    [5]\tNovo Usuario
    [6]\tNova Conta
    [7]\tContas
    [8]\tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, deposito, extrato, /):
    if deposito<0:
            print('Operação Inválida')
    else:
     saldo+=deposito
    extrato+=f"Depósito: R$ {deposito:.2f}\n"
    print(f"Saldo: R${saldo:.2f}")
    
    return saldo, extrato

def saque(valor_de_saque, saldo, saques, limite, LIMITE_DIARIO, extrato):
    if valor_de_saque > saldo:
        print('Operação Inválida! Saldo insuficiente.')
    else:
        saques+=1
        extrato+=f"Saque: R$ {valor_de_saque:.2f}\n"

        if valor_de_saque>limite:
            print('Você atingiu o seu limite diário!')

        if saques>LIMITE_DIARIO:
            print('Você atingiu o seu limite diário!')
        else:
            saldo-=valor_de_saque
            print (f"O valor de R${valor_de_saque:.2f} foi sacado")
            print('Saques:{} '.format(saques))
    return saldo, extrato

def exibir_extrato(saque,saldo,/,*,extrato):
    print('>='*10,'Extrato', '<='*10)
    print(extrato)
    print(f"Saldo: R${saldo:.2f}")
    print('>='*20)
     

def exibir_saldo(saldo):
    print(f"Saldo: R${saldo:.2f}")

def novo_usuario(usuarios):
    cpf = input('Digite seu cpf sem traços: ')
    usuario = teste_de_usuario(cpf,usuarios)
    if usuario:
        print("Este cpf já foi cadastrado")
        return

    nome= input('Digite seu nome: ')
    data_de_nascimento = input('Informe sua data de nascimento(dd-mm-aa): ')
    endereco = input('Informe seu endereço(logradouro-nmr-bairro-cidade/sigla estado): ')
    usuarios.append({"nome":nome, "data de nascimento":data_de_nascimento, "endereço":endereco, "cpf":cpf})
    print("=======>USUARIO CRIADO COM SUCESSO<=======")

def teste_de_usuario(cpf,usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario["cpf"]==cpf]
    return usuario_filtrado[0] if usuario_filtrado else None
    
def criar_conta(agencia, nova_conta, usuarios):
    cpf = str(input('Digite seu cpf sem traços: '))
    usuario = teste_de_usuario(cpf,usuarios)
    if usuario:
        print("======CONTA CRIADA COM SUCESSO======")
        return {"usuario":usuario, "conta":nova_conta, "agência":agencia}
    print("USUARIO NÃO ENCONTRADO")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:{conta['agência']}
            C/C:{conta['conta']}
            Titular da conta:{conta['usuario']['nome']}"""
        print("="*100)
        print(textwrap.dedent(linha))

def sair():
    print("Obrigado, volte sempre")

def main():
    limite=500
    extrato=""
    LIMITE_DIARIO=3
    AGENCIA="0001"
    saques=0
    saldo=0 
    usuarios=[]
    contas=[]
    while True:
        opcao=menu()
        if opcao=="1":
            deposito=float(input('Qual o valor que deseja depositar?: R$'))

            saldo, extrato = depositar(saldo, deposito, extrato)
        elif opcao =="2":
            valor_de_saque=float(input('Qual valor deseja sacar? R$'))

            saldo, extrato= saque(
                saldo = saldo,
                valor_de_saque = valor_de_saque,
                extrato = extrato,
                saques = saques,
                limite = limite,
                LIMITE_DIARIO = LIMITE_DIARIO,
            )
        elif opcao=="3":
            if saldo==0:
                print('Nenhuma ação foi feita') 
            exibir_extrato(saques,saldo, extrato=extrato)
        elif opcao=="4":
            exibir_saldo(saldo)
        elif opcao=="5":
            novo_usuario(usuarios)
        elif opcao=="6":
            nova_conta = len(contas)+1
            conta = criar_conta(AGENCIA, nova_conta, usuarios )
            if conta:
                contas.append(conta)
        elif opcao=="7":
            listar_contas(contas)
        else:
            print(sair)
            break

main()