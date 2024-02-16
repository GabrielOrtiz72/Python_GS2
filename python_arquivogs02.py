import oracledb
import json


conexao = oracledb.connect("rm98642/010404@oracle.fiap.com.br:1521/orcl")
cursor = conexao.cursor()

def menu():
    print("1. Inserir dados de usuário e saúde")
    print("2. Excluir dados de usuário")
    print("3. Alterar dados de usuário")
    print("4. Consultar dados de usuário")
    print("5. Exportar consultas para JSON")
    print("0. Sair")

def validar_dados_saude(idade, altura, peso, pressao_arterial):
    if idade <= 0 or altura <= 0 or peso <= 0:
        return False

    partes_pressao = pressao_arterial.split('/')
    if len(partes_pressao) != 2:
        return False

    try:
        parte1 = int(partes_pressao[0])
        parte2 = int(partes_pressao[1])
    except ValueError:
        return False

    return True

def inserir_dados():
    nome = input("Digite o nome do usuário: ")
    idade = int(input("Digite a idade do usuário: "))
    altura = float(input("Digite a altura do usuário (em metros): "))
    peso = float(input("Digite o peso do usuário (em quilogramas): "))
    pressao_arterial = input("Digite a pressão arterial do usuário (Digite o número dessa forma n/n):  ")


    if not validar_dados_saude(idade, altura, peso, pressao_arterial):
        print("Dados de saúde inválidos. Verifique e tente novamente.")
        return


    try:
        cursor.execute("""
            INSERT INTO usuarios_saude (nome, idade, altura, peso, pressao_arterial)
            VALUES (:nome, :idade, :altura, :peso, :pressao_arterial)
        """, {'nome': nome, 'idade': idade, 'altura': altura, 'peso': peso, 'pressao_arterial': pressao_arterial})

        conexao.commit()
        print("Dados inseridos com sucesso!")

    except oracledb.DatabaseError as ex:
        erro, = ex.args
        print(f"Erro ao inserir dados: {erro.message}")

def excluir_dados():
    try:
        id_usuario = int(input("Digite o ID do usuário que deseja excluir: "))

        cursor.execute("""
            DELETE FROM usuarios_saude
            WHERE id = :id_usuario
        """, {'id_usuario': id_usuario})

        conexao.commit()
        print(f"Usuário com ID {id_usuario} excluído com sucesso!")

    except oracledb.DatabaseError as error:
        print(f"Erro ao excluir dados: {error}")

def alterar_dados():
    try:
        id_usuario = int(input("Digite o ID do usuário que deseja alterar: "))

        nome = input("Digite o novo nome do usuário: ")
        idade = int(input("Digite a nova idade do usuário: "))
        altura = float(input("Digite a nova altura do usuário (em metros): "))
        peso = float(input("Digite o novo peso do usuário (em quilogramas): "))
        pressao_arterial = input("Digite a nova pressão arterial do usuário: ")


        if not validar_dados_saude(idade, altura, peso, pressao_arterial):
            print("Dados de saúde inválidos. Verifique e tente novamente.")
            return

        cursor.execute("""
            UPDATE usuarios_saude
            SET nome = :nome, idade = :idade, altura = :altura, peso = :peso, pressao_arterial = :pressao_arterial
            WHERE id = :id_usuario
        """, {'id_usuario': id_usuario, 'nome': nome, 'idade': idade, 'altura': altura, 'peso': peso,
              'pressao_arterial': pressao_arterial})

        conexao.commit()
        print(f"Dados do usuário com ID {id_usuario} alterados com sucesso!")

    except oracledb.DatabaseError as error:
        print(f"Erro ao alterar dados: {error}")

def consultar_dados():
    try:
        id_usuario = int(input("Digite o ID do usuário que deseja consultar: "))

        cursor.execute("""
            SELECT * FROM usuarios_saude
            WHERE id = :id_usuario
        """, {'id_usuario': id_usuario})

        resultado = cursor.fetchall()

        if resultado:
            print("Dados do usuário:")
            print(resultado)
        else:
            print(f"Usuário com ID {id_usuario} não encontrado.")

    except oracledb.DatabaseError as error:
        print(f"Erro ao consultar dados: {error}")

def exportar_para_json(consulta_resultado):
    try:
        nome_arquivo = input("Digite o nome do arquivo JSON para exportar (inclua a extensão .json): ")

        with open(nome_arquivo, 'w') as json_file:
            json.dump(consulta_resultado, json_file)

        print(f"Consulta exportada para {nome_arquivo} com sucesso!")

    except IOError as error:
        print(f"Erro ao exportar para JSON: {error}")

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        inserir_dados()
    elif opcao == "2":
        excluir_dados()
    elif opcao == "3":
        alterar_dados()
    elif opcao == "4":
        consultar_dados()
    elif opcao == "5":
        # Consultas fictícias para exemplo
        consulta1 = "SELECT * FROM usuarios_saude"

        cursor.execute(consulta1)
        resultado1 = cursor.fetchall()

        exportar_para_json({"usuarios_saude": resultado1})
    elif opcao == "0":
        print("Saindo do programa. Até mais!")
        break
    else:
        print("Opção inválida. Tente novamente.")


cursor.close()
conexao.close()
