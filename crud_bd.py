import sqlite3
from tabulate import tabulate


def adicionar_aluno(nome, matricula, nota1, nota2, nota3):
    try:
        banco = sqlite3.connect("estaciobd.db")
        cursor = banco.cursor()
        cursor.execute("INSERT INTO alunos (nome, matricula, nota1, nota2, nota3) VALUES (?, ?, ?, ?, ?)",
                       (nome, matricula, nota1, nota2, nota3))
        banco.commit()
        print(f"Aluno {nome} cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Matrícula já cadastrada.")
    except Exception as e:
        print("Erro ao adicionar aluno:", e)
    finally:
        banco.close()


#-------------------------------------------------------------------------------------------------


def listar_alunos():

    banco = sqlite3.connect("estaciobd.db")
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    banco.close()
    
    if alunos:
        print(tabulate(alunos, headers=["ID", "Nome", "Matrícula", "Nota 1", "Nota 2", "Nota 3"], tablefmt="grid"))
    else:
        print("Nenhum aluno cadastrado.")


#-------------------------------------------------------------------------------------------------


def editar_aluno(matricula, novo_nome=None, nova_nota1=None, nova_nota2=None, nova_nota3=None):
    try:
        banco = sqlite3.connect("estaciobd.db")
        cursor = banco.cursor()

        
        cursor.execute("SELECT * FROM alunos WHERE matricula = ?", (matricula,))
        aluno = cursor.fetchone()

        if not aluno:
            print("Aluno não encontrado.")
            return

        # Atualiza apenas os dados que foram informados
        if novo_nome:
            cursor.execute("UPDATE alunos SET nome = ? WHERE matricula = ?", (novo_nome, matricula))
        if nova_nota1 is not None:
            cursor.execute("UPDATE alunos SET nota1 = ? WHERE matricula = ?", (nova_nota1, matricula))
        if nova_nota2 is not None:
            cursor.execute("UPDATE alunos SET nota2 = ? WHERE matricula = ?", (nova_nota2, matricula))
        if nova_nota3 is not None:
            cursor.execute("UPDATE alunos SET nota3 = ? WHERE matricula = ?", (nova_nota3, matricula))

        banco.commit()
        print("Dados atualizados com sucesso!")

    except Exception as e:
        print("Erro ao editar aluno:", e)
    finally:
        banco.close()

#-------------------------------------------------------------------------------------------------

def excluir_aluno(matricula):
    try:
        banco = sqlite3.connect("estaciobd.db")
        cursor = banco.cursor()

        # Verifica se a matrícula existe
        cursor.execute("SELECT * FROM alunos WHERE matricula = ?", (matricula,))
        aluno = cursor.fetchone()

        if not aluno:
            print("Erro: matrícula não encontrada.")
            return

        cursor.execute("DELETE FROM alunos WHERE matricula=?", (matricula,))
        banco.commit()
        print(f"Aluno {matricula} removido com sucesso!")

    except Exception as e:
        print("Erro ao excluir aluno:", e)
    finally:
        banco.close()


#---------------------------------------------------------------------------------------------------

def calcular_media(matricula):
    try:
        banco = sqlite3.connect("estaciobd.db")
        cursor = banco.cursor()
        cursor.execute("SELECT nota1, nota2, nota3 FROM alunos WHERE matricula=?", (matricula,))
        notas = cursor.fetchone()
        if notas:
            media = sum(notas) / len(notas)
            print(f"A média do aluno {matricula} é: {media:.2f}")
        else:
            print("Aluno não encontrado.")
    except Exception as e:
        print("Erro ao calcular média:", e)
    finally:
        banco.close()


#--------------------------------------------------------------------------------------------------------



def menu():
    while True:
        print("\n Sistema de Cadastro de Alunos ")
        print("1 - Adicionar aluno")
        print("2 - Listar alunos")
        print("3 - Excluir aluno")
        print("4 - Calcular média")
        print("5 - Editar dados de aluno")
        print("0 - Sair")

        
        opcao = input("Escolha uma opção: ")
       

        if opcao == "1":
            nome = input("Nome do aluno: ")
            matricula = input("Matrícula: ")

            try:
                nota1 = float(input("Nota 1: "))
                nota2 = float(input("Nota 2: "))
                nota3 = float(input("Nota 3: "))
            except ValueError:
                print("Erro: Digite apenas números válidos para as notas.")
                continue

            adicionar_aluno(nome, matricula, nota1, nota2, nota3)

        elif opcao == "2":
            listar_alunos()

        elif opcao == "3":
            matricula = input("Matrícula do aluno: ")
            excluir_aluno(matricula)

        elif opcao == "4":
            matricula = input("Matrícula do aluno: ")
            calcular_media(matricula)

        elif opcao == "5":
            matricula = input("Matrícula do aluno a editar: ")

            novo_nome = input("Novo nome (ou deixe em branco para manter o atual): ")
            try:
                nota1 = input("Nova Nota 1 (ou deixe em branco): ")
                nota2 = input("Nova Nota 2 (ou deixe em branco): ")
                nota3 = input("Nova Nota 3 (ou deixe em branco): ")

                nova_nota1 = float(nota1) if nota1.strip() else None
                nova_nota2 = float(nota2) if nota2.strip() else None
                nova_nota3 = float(nota3) if nota3.strip() else None

            except ValueError:
                print("Erro: Digite apenas números válidos para as notas.")
                continue

            editar_aluno(matricula, novo_nome if novo_nome.strip() else None, nova_nota1, nova_nota2, nova_nota3)

        elif opcao == "0":
            print("Fechando o programa...")
            break

        


