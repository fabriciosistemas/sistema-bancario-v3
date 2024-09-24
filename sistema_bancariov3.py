from abc import ABC, abstractmethod

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
        
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Historico:
    
    def __init__(self):
        self.historico = []

    def historico(self):
        return self.historico

    def adicionar_transacao(self, transacao):
        if   isinstance(transacao, Saque):
            self.historico.append({"tipo": Saque.__name__, "valor": transacao.valor})
        elif isinstance(transacao, Deposito):
            self.historico.append({"tipo": Deposito.__name__, "valor": transacao.valor})

class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        if  valor > self.saldo:
            print("Falha! Não há saldo suficiente na conta. Não foi possível realizar a operação.")
            return False
        
        if valor > 0:
            self.saldo -= valor
            print("Operação realizada!")
            return True
        else:
            print("Falha! Informe um valor válido.")
        
        return False
        
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("Operação realizada!")
        else:
            print("Falha! Não é possível depositar este valor.")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        if  (len([transacao for transacao in self.historico.historico if transacao["tipo"] == Saque.__name__]) >= self.limite_saques):
            print("Falha! Limite de saques excedidos!")
            return False
        elif valor > self.limite:
            print("Falha! Valor máximo para saque excedido!")
            return False
        else:
            super().sacar(valor)
            return True

class Cliente:
    
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if   isinstance(transacao, Saque):
            if conta.sacar(transacao.valor):
                conta.historico.adicionar_transacao(transacao)
        elif isinstance(transacao, Deposito):
            if conta.depositar(transacao.valor):
                conta.historico.adicionar_transacao(transacao)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

def menu():
    print(
          """
            [1] Depositar
            [2] Sacar
            [3] Extrato
            [4] Criar usuário
            [5] Criar conta
            [Q] Sair
          """
         )

def main():
    contas = []
    clientes = []

    while True:
        menu()
        opcao = input("Informe a operação: ")

        if   opcao == '1':
            depositar(clientes)
        elif opcao == '2':
            sacar(clientes)
        elif opcao == '3':
            extrato(clientes)
        elif opcao == '4':
            criar_usuario(clientes)
        elif opcao == '5':
            cpf = input("Informe o CPF do usuario: ")
            criar_conta_corrente(clientes, cpf, contas)
        elif opcao == 'q' or opcao == 'Q':
            break
        else:
            print("Operação inválida! Por favor, escolha novamente.")

    print("Volte sempre!")

def depositar(clientes):
    cliente, conta = generalista(clientes)
    if not cliente or not conta:
        print("Dados inválidos")
        return
    
    valor = float(input("Informe o valor: "))
    
    cliente.realizar_transacao(conta, Deposito(valor))
        
def sacar(clientes):
    cliente, conta = generalista(clientes)
    if not cliente or not conta:
        print("Dados inválidos")
        return
    
    valor = float(input("Informe o valor: "))
    
    cliente.realizar_transacao(conta, Saque(valor))
    
def generalista(clientes):
    print("Identificando o cliente...")
    cpf = input("Informe o CPF: ")
    cliente = procurar_cliente(cpf, clientes)

    if not cliente:
        print("Falha! Cliente não encontrado.")
        return None, None

    print("Identificando a conta...")
    numero_conta = input("Informe a conta: ")
    conta = encontrar_conta(numero_conta, cliente)

    if not conta:
        print("Falha! Conta não encontrada.")
        return None, None
    
    return cliente, conta

def procurar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None
    
def encontrar_conta(numero_conta, cliente):
    if not cliente.contas:
        print("Cliente sem conta cadastrada!")
        return
    
    for conta in cliente.contas:
        if int(conta.numero) == int(numero_conta):
            return conta
        
    print("Conta não encontrada")
    return None

def extrato(clientes):
    cliente, conta = generalista(clientes)
    if not cliente or not conta:
        print("Dados inválidos")
        return
    
    print("====================EXTRATO====================")
    if len(conta.historico.historico) == 0:
        print("Não foram feitas operações na conta.")
    else:    
        print(conta.historico.historico)
        print(f"Saldo: R$ {conta.saldo:.2f}")
    
    print("===============================================")

def criar_usuario(clientes):
    cpf = input("Informe o CPF do usuário: ")
    
    if procurar_cliente(cpf, clientes):
        print("Erro!! Já existe um usuário com esse CPF!")
        return
    
    nome = input("Informe o nome do usuário: ")
    data_nascimento = input("Informe a data de nascimento do usuário (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")
    
    clientes.append(PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco))
    print("Cliente cadastrado!")

def criar_conta_corrente(clientes, cpf, contas):
    cliente = procurar_cliente(cpf, clientes)

    if not cliente:
        print("Falha! Cliente não encontrado.")
        criar_cpf = input("Usuário com esse CPF não existe. Responda com a tecla <S> se deseja criar usuário: ")
        if criar_cpf == 'S' or criar_cpf == 's':
            criar_usuario(clientes)
            return
        else:
            return
    if len(contas) > 0:
        numero_conta = contas[-1].numero + 1
    else:
        numero_conta = 1
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("Conta criada com sucesso!")

main()