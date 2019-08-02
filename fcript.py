import sqlite3, os
from cryptography.fernet import Fernet

def criptografa(arq, key, diretorio_bd, cifra_principal):
	print(key)	
	key = bytes(key, "utf-8")
	arquivo = open(arq, "rb")
	cifra = Fernet(key)
	texto_cifrado = cifra.encrypt(arquivo.read())
	arquivo.close()
	arquivo = open(arq, "wb")
	arquivo.write(texto_cifrado)
	arquivo.close()

def descriptografa(arq, key, diretorio_bd, cifra_principal):


	key = bytes(key, "utf-8")
	cifra = Fernet(key)
	arquivo = open(arq, "rb")
	texto_plano = cifra.decrypt(arquivo.read())
	arquivo.close()
	arquivo = open(arq, "wb")
	arquivo.write(texto_plano)
	arquivo.close()

def criar_usuario(dados, diretorio_bd, cifra_principal):
	
	#descriptografa o bd
	cript_db = open(diretorio_bd, "rb")
	db_cripto = cifra_principal.decrypt(cript_db.read())
	cript_db.close()
	cript_db = open(diretorio_bd, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

	db = sqlite3.connect(diretorio_bd)
	cursor = db.cursor()
	cursor.execute("""
			INSERT INTO usuario(user, senha, key)
			VALUES(?,?,?)""", dados)
	db.commit()
	db.close()
	

	#criptografa o bd
	cript_db = open(diretorio_bd, "rb")
	db_cripto = cifra_principal.encrypt(cript_db.read())
	cript_db.close()
	cript_db = open(diretorio_bd, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

def apagar_usuario(dados, diretorio_bd, cifra_principal):
	
	#descriptografa o bd
	cript_db = open(diretorio_bd, "rb")
	db_cripto = cifra_principal.decrypt(cript_db.read())
	cript_db.close()
	cript_db = open(diretorio_bd, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

	db = sqlite3.connect(diretorio_bd)
	cursor = db.cursor()
	cursor.execute("""
			DELETE FROM usuario
			WHERE id=?
			""", dados)
	db.commit()
	db.close()
	#criptografa o bd
	cript_db = open(diretorio_bd, "rb")
	db_cripto = cifra_principal.encrypt(cript_db.read())
	cript_db.close()
	cript_db = open(diretorio_bd, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

def ajuda():

	print("""
[ajudas]

1-selecione a primeira opção e crie um usuario para criptografa seus dados

2-o programa consegue criptografa um arquivo que esta na mesma pasta onde ele esta sendo executado, então para pode criptografa um arquivo especifico mova o executavel para mesma pasta

3-selecione a segunda opção para pegar a key e usa-la para criptografa seus dados!

3-selecione a terceira opção para criptografa e a terceira para descriptografa
	""")

	input("pressione enter para continuar!")

def ver_usuarios(cifra_principal, diretorio_bd):


		#descriptografa o bd
		cript_db = open(diretorio_bd, "rb")
		db_cripto = cifra_principal.decrypt(cript_db.read())
		cript_db.close()
		cript_db = open(diretorio_bd, "wb")
		cript_db.write(db_cripto)
		cript_db.close()

		db = sqlite3.connect(diretorio_bd)
		pasta = os.listdir()
		cursor = db.cursor()
		cursor.execute("""
				SELECT * FROM usuario;
				""")
		usuarios = cursor.fetchall()
		db.close()
		#criptografa o bd
		cript_db = open(diretorio_bd, "rb")
		db_cripto = cifra_principal.encrypt(cript_db.read())
		cript_db.close()
		cript_db = open(diretorio_bd, "wb")
		cript_db.write(db_cripto)
		cript_db.close()

		return usuarios

def continuar():

	input("pressione enter para continuar!")

