from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('Operação Inválida! Saldo insuficiente.')
        
        elif valor > 0:
            self._saldo -= valor
            print('SALDO REALIZADO COM SUCESSO')
        
        else:
            print('Operação falhou, Valor incorreto!!!')
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!!")
        else:
            print("Operação falhada")
            return False
        
        return False

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime
            ("%d-%m-%Y %H:%M:%s")
        })
    
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class ContaCorrente(Conta):
    
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super()().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"]== Saque.__name__])

        excedeu_limite = valor > self.limite
        if excedeu_limite:
            print("Operação falhada! Limite excedidio")
        else:
            return False
    
        excedeu_limites_saques = numero_saques >= self.limite_saques
        if excedeu_limites_saques:
            print("Seu limite diario foi atingido!!!")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\T\T{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    
    return envelope

def menu():
    menu= """\n
    ===============MENU=================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo Usuario
    [5]\tNova Conta
    [6]\tContas
    [7]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    clientes=[]
    contas=[]

    while True:
        opcao=menu()

        if opcao=="1":
            depositar(clientes)

        elif opcao =="2":
            sacar(clientes)

        elif opcao=="3":
            exibir_extrato(clientes)
            
        elif opcao=="4":
            criar_cliente(clientes)

        elif opcao=="5":
            numero_conta = len(contas) + 1
            criar_conta( numero_conta, clientes, contas)

        elif opcao=="6":
            listar_contas(contas)

        else:
            break

@log_transacao
def depositar(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!!')
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Depositar(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [clientes for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

@log_transacao
def sacar(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n====================EXTRATO=======================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio( tipo_transacao="Saque"):
        tem_transacao = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    if not tem_transacao:
        extrato = "Não foam realizadas movimentações"
    
    print(extrato)
    print(f"\nSaldo: \n\tR$ {conta.saldo:.2f}")
    print("==========================================")

@log_transacao
def criar_conta(numero_da_conta, clientes, contas):
    cpf = str(input('Digite seu cpf sem traços: '))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não econtrado, fluxo de criação de conta encerado!")
        return 
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_da_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n Conta criada com sucesso!\n")

def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

@log_transacao
def criar_cliente(clientes):
    cpf = input('Digite seu cpf sem traços: ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Este cpf já foi cadastrado")
        return

    nome= input('Digite seu nome: ')
    data_de_nascimento = input('Informe sua data de nascimento(dd-mm-aa): ')
    cliente = PessoaFisica(nome=nome, data_nascimento=data_de_nascimento, cpf=cpf)

    clientes.append(cliente)

    print("=======>USUARIO CRIADO COM SUCESSO<=======")

main()