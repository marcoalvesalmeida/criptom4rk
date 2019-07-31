from cryptography.fernet import Fernet
import os, sqlite3, getpass, platform
from keys import keys_programa


def criptografa(arq, key):
	
	key =bytes(key, "utf-8")
	arquivo = open(arq, "rb")
	cifra = Fernet(key)
	texto_cifrado = cifra.encrypt(arquivo.read())
	arquivo.close()
	arquivo = open(arq, "wb")
	arquivo.write(texto_cifrado)
	arquivo.close()

def descriptografa(arq, key):


	key = bytes(key, "utf-8")
	cifra = Fernet(key)
	arquivo = open(arq, "rb")
	texto_plano = cifra.decrypt(arquivo.read())
	arquivo.close()
	arquivo = open(arq, "wb")
	arquivo.write(texto_plano)
	arquivo.close()

def criar_usuario(dados):
	
	#descriptografa o bd
	cript_db = open(temp, "rb")
	db_cripto = cifra_principal.decrypt(cript_db.read())
	cript_db.close()
	cript_db = open(temp, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

	db = sqlite3.connect(temp)
	cursor = db.cursor()
	cursor.execute("""
			INSERT INTO usuario(user, senha, key)
			VALUES(?,?,?)""", dados)
	db.commit()
	db.close()
	

	#criptografa o bd
	cript_db = open(temp, "rb")
	db_cripto = cifra_principal.encrypt(cript_db.read())
	cript_db.close()
	cript_db = open(temp, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

def apagar_usuario(dados):
	
	#descriptografa o bd
	cript_db = open(temp, "rb")
	db_cripto = cifra_principal.decrypt(cript_db.read())
	cript_db.close()
	cript_db = open(temp, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

	db = sqlite3.connect(temp)
	cursor = db.cursor()
	cursor.execute("""
			DELETE FROM usuario
			WHERE id=?
			""", dados)
	db.commit()
	db.close()
	#criptografa o bd
	cript_db = open(temp, "rb")
	db_cripto = cifra_principal.encrypt(cript_db.read())
	cript_db.close()
	cript_db = open(temp, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

def ajuda():

	print("""
[ajudas]

1-selecione a primeira opção e crie um usuario para criptografa seus dados

2-o programa consegue criptografa um arquivo que esta na mesma pasta onde ele esta sendo executado, então para pode criptografa um arquivo especifico mova o executavel para mesma pasta

3-selecione a segunda opção para criptografa e a terceira para descriptografa
	""")


key_programa = keys_programa()
cifra_principal = Fernet(key_programa)
pasta = os.listdir()
sistema = platform.system()
temp = ""

if sistema == "Linux":

	pasta_sistema = os.path.abspath("").split("/")
	for c in range(0, 3):
		
		temp += pasta_sistema[c] + "/"

	temp += ".local/share/"
	pasta_sistema = os.listdir(temp)

elif sistema == "Windows":
	
	pasta_sistema = os.path.abspath("").split("\\")
	temp += pasta_sistema[0] +  "\\\\"

	for c in range(1, 3):
		
		temp += pasta_sistema[c] + "\\"

	pasta_sistema = os.listdir(temp)
	
	if ".m4rk" not in pasta_sistema:
		
		os.mkdir(temp + ".m4rk/")
	
	temp += ".m4rk\\"
	pasta_sistema = os.listdir(temp)


if "criptom4rk" not in pasta_sistema:
	
	os.mkdir(temp+"criptom4rk/")

temp = temp + "criptom4rk/"

if "dados.db" not in os.listdir(temp):
        
	db = sqlite3.connect(temp + "dados.db")
	cursor = db.cursor()
	cursor.execute("""
			CREATE TABLE usuario(
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			user VARCHAR(200) NOT NULL,
			senha TEXT NOT NULL,
			key TEXT NOT NULL);
			""")
	db.close()
	#criptografa o bd
	cript_db = open(temp+"dados.db", "rb")
	db_cripto = cifra_principal.encrypt(cript_db.read())
	cript_db.close()
	cript_db = open(temp+"dados.db", "wb")
	cript_db.write(db_cripto)
	cript_db.close()


temp = temp + "dados.db"

while True:

	auth = False
	#descriptografa o bd
	cript_db = open(temp, "rb")
	db_cripto = cifra_principal.decrypt(cript_db.read())
	cript_db.close()
	cript_db = open(temp, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

	db = sqlite3.connect(temp)
	pasta = os.listdir()
	cursor = db.cursor()
	cursor.execute("""
			SELECT * FROM usuario;
			""")
	usuarios =cursor.fetchall()
	db.close()
	#criptografa o bd
	cript_db = open(temp, "rb")
	db_cripto = cifra_principal.encrypt(cript_db.read())
	cript_db.close()
	cript_db = open(temp, "wb")
	cript_db.write(db_cripto)
	cript_db.close()

	print("""
1-Criar novo usuario
2-criptografa arquivos
3-descriptografa
4-apagar usuario
5-ajuda
0-sair
			""")

	escolha = int(input("escolha uma opção: "))
	
	if escolha == 1:
		
		user = str(input("digite o nome de usuario: "))
		senha = bytes(getpass.getpass("digite uma senha: "), "utf-8")
		senha2 = bytes(getpass.getpass("confirme a senha: "), "utf-8")

		if senha == senha2:

			senha = cifra_principal.encrypt(senha)
			key = Fernet.generate_key()
			dados = (user, senha.decode("utf-8"), key.decode("utf-8"))
			criar_usuario(dados)
			senha2 = ""

		else:

			print("senha não são iguais")

	elif escolha == 2:

		if len(usuarios) > 0:

			for index, arq in enumerate(pasta):

				print(f"{index}|{arq}")

			print("\n")
			escolha_arquivo = int(input("escolha o index do arquivo: "))

			if escolha_arquivo < len(pasta):
				
				print("\n")
				user = str(input("digite seu nome de usuario: "))
				for usu in usuarios:
					if user in usu:

						auth = True
						break

					else:

						print("usuario não encontrado")

				if auth:
					
					while True:
						
						auth = False
						senha = getpass.getpass("digite sua senha: ")
						senha_usu = usu[2]
						senha_usu = bytes(senha_usu, "utf-8")
						senha_usu = cifra_principal.decrypt(senha_usu).decode("utf-8")
						if senha == senha_usu:

							auth = True

							break

						else:

							print("senha incorreta\n")
				
				if auth:
					
					auth = False
					criptografa(str(pasta[escolha_arquivo]), usu[3])
					print("criptografado com sucesso!!")

		
		else:

			print("nenhum usuario criado!")

	
	elif escolha == 3:

		if len(usuarios) > 0:


			for index, arq in enumerate(pasta):

				print(f"{index}|{arq}")
			
			print("\n")
			escolha_arquivo = int(input("digite o index do arquivo: "))
			
			if escolha_arquivo < len(pasta):

				print("\n")
				user = str(input("digite seu nome de usuario: "))

				for usu in usuarios:

					if user in usu:

						auth = True
						break

			if auth:
				
				while True:

					auth = False
					senha = getpass.getpass("senha: ")
					senha_usu = bytes(usu[2], "utf-8")
					senha_usu = cifra_principal.decrypt(senha_usu).decode("utf-8")
					if senha == senha_usu:

						auth = True
						break

					else:

						print("senha incorreta!")

			if auth:
				
				descriptografa(pasta[escolha_arquivo], usu[3])
				print("arquivo descriptografado!!")
		
		else:

			print("nenhum usuario criado!")

	elif escolha == 4:
		
		if len(usuarios) > 0:

			user = str(input("digite seu nome de usuario: "))
			
			for usu in usuarios:

				if user == usu[1]:

					auth = True
					break

				else:

					usu = None

			if auth:
				
				while True:

					auth = False
					senha = getpass.getpass("senha: ")
					senha_usu = bytes(usu[2], "utf-8")
					senha_usu = cifra_principal.decrypt(senha_usu).decode("utf-8")

					if senha == senha_usu:

						auth = True
						break

					else:

						print("senha incorreta!!")

			if auth:

				apagar_usuario((usu[0], ))
				print("usuario apagado!")

		else:

			print("sem usuarios registrados!!")
	
	elif escolha == 5:

		ajuda()

	elif escolha == 0:

		break

	print("\n\n")


