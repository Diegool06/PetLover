import hashlib
from datetime import datetime
import random

# Funções auxiliares para o sistema
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

def gerar_codigo_autenticacao():
    return str(random.randint(100000, 999999))  # Gera um código de 6 dígitos para 2FA

# Classes do sistema
class Usuario:
    def __init__(self, cpf_email, senha, tipo):
        self.cpf_email = cpf_email
        self.senha = hash_senha(senha)
        self.tipo = tipo  # A = Administrador, U = Usuário

    def verificar_senha(self, senha):
        return self.senha == hash_senha(senha)

class Cliente:
    def __init__(self, nome, cpf, celular, email, cep, sexo):
        self.nome = nome
        self.cpf = cpf
        self.celular = celular
        self.email = email
        self.cep = cep
        self.sexo = sexo

class Pet:
    def __init__(self, id_pet, nome, categoria, raca, data_nascimento, cpf_dono):
        self.id_pet = id_pet
        self.nome = nome
        self.categoria = categoria
        self.raca = raca
        self.data_nascimento = data_nascimento
        self.cpf_dono = cpf_dono

class Servico:
    def __init__(self, id_servico, descricao, valor, orientacao):
        self.id_servico = id_servico
        self.descricao = descricao
        self.valor = valor
        self.orientacao = orientacao

class Atendimento:
    def __init__(self, id_servico, id_pet, data_agendamento):
        self.id_servico = id_servico
        self.id_pet = id_pet
        self.data_agendamento = data_agendamento
        self.data_atendimento = None
        self.data_conclusao = None
        self.situacao = "A"  # A = Agendado, C = Cancelado, E = Efetivado, R = Remarcado

    def iniciar_atendimento(self):
        self.data_atendimento = datetime.now()
        self.situacao = "E"

    def remarcar_atendimento(self, nova_data):
        self.data_agendamento = nova_data
        self.situacao = "R"

    def cancelar_atendimento(self):
        self.situacao = "C"

# Classe principal do sistema para cadastro e gerenciamento
class SistemaCadastro:
    def __init__(self):
        self.usuarios = [Usuario("inspetor@gmail.com", "inspetor40", "A")]
        self.clientes = []
        self.pets = []
        self.servicos = []
        self.atendimentos = []

    def login_usuario(self, cpf_email, senha):
        for usuario in self.usuarios:
            if usuario.cpf_email == cpf_email and usuario.verificar_senha(senha):
                print("Login bem-sucedido!")
                if self.autenticacao_2fa(usuario):
                    return usuario
                else:
                    print("Autenticação 2FA falhou!")
                    return None
        print("Usuário ou senha incorretos!")
        return None

    def autenticacao_2fa(self, usuario):
        codigo_esperado = gerar_codigo_autenticacao()
        print(f"Código de autenticação 2FA enviado: {codigo_esperado}")
        codigo_recebido = input("Digite o código de autenticação: ")
        return codigo_recebido == codigo_esperado

    def cadastrar_usuario(self, cpf_email, senha, tipo, usuario_logado):
        if usuario_logado and usuario_logado.tipo == "A":
            novo_usuario = Usuario(cpf_email, senha, tipo)
            self.usuarios.append(novo_usuario)
            print("Usuário cadastrado com sucesso.")
        else:
            print("Apenas administradores podem cadastrar usuários.")

    def consultar_usuarios(self):
        for usuario in self.usuarios:
            print(f"Usuário: {usuario.cpf_email}, Tipo: {usuario.tipo}")

    def cadastrar_cliente(self, nome, cpf, celular, email, cep, sexo, usuario_logado):
        if usuario_logado and usuario_logado.tipo == "A" and validar_cpf(cpf):
            novo_cliente = Cliente(nome, cpf, celular, email, cep, sexo)
            self.clientes.append(novo_cliente)
            print("Cliente cadastrado com sucesso.")
        else:
            print("Apenas administradores podem cadastrar clientes.")

    def cadastrar_pet(self, id_pet, nome, categoria, raca, data_nascimento, cpf_dono, usuario_logado):
        if usuario_logado and usuario_logado.tipo == "A":
            novo_pet = Pet(id_pet, nome, categoria, raca, data_nascimento, cpf_dono)
            self.pets.append(novo_pet)
            print("Pet cadastrado com sucesso.")
        else:
            print("Apenas administradores podem cadastrar pets.")

    def cadastrar_servico(self, id_servico, descricao, valor, orientacao, usuario_logado):
        if usuario_logado and usuario_logado.tipo == "A":
            novo_servico = Servico(id_servico, descricao, valor, orientacao)
            self.servicos.append(novo_servico)
            print("Serviço cadastrado com sucesso.")
        else:
            print("Apenas administradores podem cadastrar serviços.")

    def agendar_atendimento(self, id_servico, id_pet, data_agendamento):
        novo_atendimento = Atendimento(id_servico, id_pet, data_agendamento)
        self.atendimentos.append(novo_atendimento)
        print("Atendimento agendado com sucesso.")

    def listar_atendimentos(self):
        for atendimento in self.atendimentos:
            print(f"Serviço: {atendimento.id_servico}, Pet: {atendimento.id_pet}, Status: {atendimento.situacao}")

# Estrutura do Menu do Sistema
def menu_principal(sistema, usuario_logado):
    while True:
        print("\nMenu Principal")
        print("1. Cadastros")
        print("2. Atendimento")
        print("3. Consultas/Relatórios")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_cadastros(sistema, usuario_logado)
        elif opcao == "2":
            menu_atendimento(sistema)
        elif opcao == "3":
            menu_consultas(sistema)
        elif opcao == "4":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida, tente novamente.")

def menu_cadastros(sistema, usuario_logado):
    while True:
        print("\nMenu de Cadastros")
        print("1. Usuários")
        print("2. Clientes")
        print("3. Pets")
        print("4. Serviços")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cpf_email = input("CPF/Email do novo usuário: ")
            senha = input("Senha do novo usuário: ")
            tipo = input("Tipo (A-Administrador, U-Usuário): ")
            sistema.cadastrar_usuario(cpf_email, senha, tipo, usuario_logado)
        elif opcao == "2":
            nome = input("Nome do cliente: ")
            cpf = input("CPF do cliente: ")
            celular = input("Celular do cliente: ")
            email = input("Email do cliente: ")
            cep = input("CEP do cliente: ")
            sexo = input("Sexo do cliente: ")
            sistema.cadastrar_cliente(nome, cpf, celular, email, cep, sexo, usuario_logado)
        elif opcao == "3":
            id_pet = input("ID do pet: ")
            nome = input("Nome do pet: ")
            categoria = input("Categoria (felino, canino, bovino, etc): ")
            raca = input("Raça do pet: ")
            data_nascimento = input("Data de nascimento do pet: ")
            cpf_dono = input("CPF do dono: ")
            sistema.cadastrar_pet(id_pet, nome, categoria, raca, data_nascimento, cpf_dono, usuario_logado)
        elif opcao == "4":
            id_servico = input("ID do serviço: ")
            descricao = input("Descrição do serviço: ")
            valor = input("Valor do serviço: ")
            orientacao = input("Orientação do serviço: ")
            sistema.cadastrar_servico(id_servico, descricao, valor, orientacao, usuario_logado)
        elif opcao == "5":
            break
        else:
            print("Opção inválida, tente novamente.")

def menu_atendimento(sistema):
    while True:
        print("\nMenu de Atendimento")
        print("1. Agendar Atendimento")
        print("2. Listar Atendimentos")
        print("3. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            id_servico = input("ID do serviço: ")
            id_pet = input("ID do pet: ")
            data_agendamento = input("Data de agendamento (AAAA-MM-DD): ")
            sistema.agendar_atendimento(id_servico, id_pet, data_agendamento)
        elif opcao == "2":
            sistema.listar_atendimentos()
        elif opcao == "3":
            break
        else:
            print("Opção inválida, tente novamente.")

def menu_consultas(sistema):
    print("\nConsultas e Relatórios")
    sistema.listar_atendimentos()

# Inicialização do sistema com login e menu
if __name__ == "__main__":
    sistema = SistemaCadastro()
    print("Bem-vindo ao sistema Pet Lover")

    usuario_logado = None
    while not usuario_logado:
        cpf_email = input("Digite seu CPF/Email: ")
        senha = input("Digite sua senha: ")
        usuario_logado = sistema.login_usuario(cpf_email, senha)

    menu_principal(sistema, usuario_logado)
