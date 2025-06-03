import sqlite3

def conectar():
    banco = sqlite3.connect("estaciobd.db")
    cursor = banco.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS alunos(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        matricula TEXT UNIQUE NOT NULL,
                        nota1 REAL,
                        nota2 REAL,
                        nota3 REAL)''')
    
    banco.commit()
    banco.close()

conectar()