from cryptography.fernet import Fernet
import os, sqlite3, getpass, platform
from keys import keys_programa
from fcript import criptografa, descriptografa, criar_usuario, apagar_usuario, ajuda, ver_usuarios


key_programa = keys_programa()
cifra_principal = Fernet(key_programa)
pasta = os.listdir()
sistema = platform.system()
diretorio_bd = ""
menu = ["1-Criar novo usuario", "2-Verificar key", "3-Criptografa arquivo", "4-Descriptografa arquivo", "5-Apagar usuario", "6-Ajuda", "0-Sair"]

if sistema == "Linux":
	
	os.system("clear")
	pasta_sistema = os.path.abspath("").split("/")
	for c in range(0, 3):
		
		diretorio_bd += pasta_sistema[c] + "/"

	diretorio_bd += ".local/share/"
	pasta_sistema = os.listdir(diretorio_bd)

elif sistema == "Windows":
	
	os.system("cls")
	pasta_sistema = os.path.abspath("").split("\\")
	diretorio_bd += pasta_sistema[0] +  "\\\\"

	for c in range(1, 3):
		
		diretorio_bd += pasta_sistema[c] + "\\"

	pasta_sistema = os.listdir(diretorio_bd)
	
	if ".m4rk" not in pasta_sistema:
		
		os.mkdir(diretorio_bd + ".m4rk/")
	
	diretorio_bd += ".m4rk\\"
	pasta_sistema = os.listdir(diretorio_bd)


if "criptom4rk" not in pasta_sistema:
	
	os.mkdir(diretorio_bd+"criptom4rk/")

diretorio_bd = diretorio_bd + "criptom4rk/"

if "dados.db" not in os.listdir(diretorio_bd):
        
	db = sqlite3.connect(diretorio_bd + "dados.db")
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
	cript_db = open(diretorio_bd+"dados.db", "rb")
	db_cripto = cifra_principal.encrypt(cript_db.read())
	cript_db.close()
	cript_db = open(diretorio_bd+"dados.db", "wb")
	cript_db.write(db_cripto)
	cript_db.close()


diretorio_bd = diretorio_bd + "dados.db"

while True:
	
	auth = False
	usuarios = None
	print("#"*80)
	print(f"{'CRIPTOM4RK':^79}")
	print("#"*80)
	for campo in menu:

		print(f"{campo:^79}")

	escolha = int(input("escolha uma opção: "))
	
	if escolha == 1:
		
		user = str(input("digite o nome de usuario: "))
		senha = bytes(getpass.getpass("digite uma senha: "), "utf-8")
		senha2 = bytes(getpass.getpass("confirme a senha: "), "utf-8")

		if senha == senha2:

			senha = cifra_principal.encrypt(senha)
			key = Fernet.generate_key()
			dados = (user, senha.decode("utf-8"), key.decode("utf-8"))
			criar_usuario(dados, diretorio_bd, cifra_principal)
			senha2 = ""

		else:

			print("senha não são iguais")

	elif escolha == 2:

		user = str(input("nome de usuario: "))
		senha = bytes(getpass.getpass("senha: "), "utf-8")
		cript_db = open(diretorio_bd, "rb")
		db_cripto = cifra_principal.decrypt(cript_db.read())
		
		cript_db.close()

		cript_db = open(diretorio_bd, "wb")
		cript_db.write(db_cripto)
		cript_db.close()

		db = sqlite3.connect(diretorio_bd)
		cursor = db.cursor()
		cursor.execute("""
				SELECT * FROM usuario
				WHERE user=?;
				""", (user,))
		key_usuario = cursor.fetchall()
		db.close()

		cript_db = open(diretorio_bd, "rb")
		db_cripto = cifra_principal.encrypt(cript_db.read())
		cript_db.close()
		cript_db = open(diretorio_bd, "wb")
		cript_db.write(db_cripto)
		cript_db.close()
		
		if len(key_usuario) > 0:

			if senha == cifra_principal.decrypt(bytes(key_usuario[0][2], "utf-8")):

				print(f"sua key: {key_usuario[0][3]}")
				input("pressione enter para continuar!")
				key_usuario = None

		else:

			print("nenhum usuario encontrado!")
			input("pressione enter para continuar!")

	elif escolha == 3:
		
		usuarios = ver_usuarios(cifra_principal, diretorio_bd)

		if len(usuarios) > 0:

			for index, arq in enumerate(pasta):

				print(f"{index}|{arq}")

			print("\n")
			escolha_arquivo = int(input("escolha o index do arquivo: "))
			chave = str(input("cole sua chave aqui: ")).strip()
			criptografa(str(pasta[escolha_arquivo]), chave, diretorio_bd, cifra_principal)
			print("criptografado com sucesso!!")
			input("pressione enter para continuar!")

		
		else:

			print("nenhum usuario criado!")
			input("pressione enter para continuar!")

	
	elif escolha == 4:

		usuarios = ver_usuarios(cifra_principal, diretorio_bd)

		if len(usuarios) > 0:


			for index, arq in enumerate(pasta):

				print(f"{index}|{arq}")
			
			print("\n")
			escolha_arquivo = int(input("digite o index do arquivo: "))
			key = str(input("cole sua key: ")).strip()
			descriptografa(pasta[escolha_arquivo], key, diretorio_bd, cifra_principal)
			print("arquivo descriptografado!!")
			input("pressione enter para continuar!")
		
		else:

			print("nenhum usuario criado!")
			input("pressione enter para continuar!")

	elif escolha == 5:
		
		usuarios = ver_usuarios(cifra_principal, diretorio_bd)

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

				apagar_usuario((usu[0], ), diretorio_bd, cifra_principal)
				print("usuario apagado!")

		else:

			print("sem usuarios registrados!!")
			input("pressione enter para continuar!")
	
	elif escolha == 6:

		ajuda()

	elif escolha == 0:

		break

	if sistema == "Windows":

		os.system("cls")

	elif sistema == "Linux":

		os.system("clear")

