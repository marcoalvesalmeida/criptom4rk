from cryptography.fernet import Fernet
import os, sqlite3, getpass, platform
from keys import keys_programa
from fcript import criptografa, descriptografa, criar_usuario, apagar_usuario, ajuda, ver_usuarios, continuar

#chama a key principal do progama
key_programa = keys_programa()
#cria a cifra principal
cifra_principal = Fernet(key_programa)
#lista todo conteudo da pasta
pasta = os.listdir()
#pega qual sistema operacional
sistema = platform.system()
#diretorio do banco de dados
diretorio_bd = ""
#itens para construir o menu
menu = ["1-Criar novo usuario", "2-Verificar key", "3-Criptografa arquivo", "4-Descriptografa arquivo", "5-Apagar usuario", "6-Ajuda", "0-Sair"]

#verifica qual o SO e configura o sistema de arquivo
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

#configura as pastas e arquivos necessarios
if "criptom4rk" not in pasta_sistema:
	
	os.mkdir(diretorio_bd+"criptom4rk/")

diretorio_bd = diretorio_bd + "criptom4rk/"
#verifica se o bd ja foi criado
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
	
	#variavel para auteticação
	auth = False
	#variavel que armazena os usuarios
	usuarios = None
	#menu
	print("#"*80)
	print(f"{'CRIPTOM4RK':^79}")
	print("#"*80)
	for campo in menu:

		print(f"{campo:^79}")

	escolha = int(input("escolha uma opção: "))
	
	if escolha == 1:
		
		user = str(input("digite o nome de usuario: "))
		#transforma a string em bytes
		senha = bytes(getpass.getpass("digite uma senha: "), "utf-8")
		senha2 = bytes(getpass.getpass("confirme a senha: "), "utf-8")

		if senha == senha2:
			
			#criptografa a senha
			senha = cifra_principal.encrypt(senha)
			#gera uma key pro usuario
			key = Fernet.generate_key()
			#dados que serão passados pro bd
			dados = (user, senha.decode("utf-8"), key.decode("utf-8"))
			#chama função para criar usuario
			criar_usuario(dados, diretorio_bd, cifra_principal)
			senha2 = ""

		else:

			print("senha não são iguais")
			continuar()

	elif escolha == 2:

		user = str(input("nome de usuario: "))
		senha = bytes(getpass.getpass("senha: "), "utf-8")
		#abre o bd
		cript_db = open(diretorio_bd, "rb")
		#descriptografa o bd/
		db_cripto = cifra_principal.decrypt(cript_db.read())
		cript_db.close()

		cript_db = open(diretorio_bd, "wb")
		cript_db.write(db_cripto)
		cript_db.close()
		#/
		#abre o bd e procura o usuario passado
		db = sqlite3.connect(diretorio_bd)
		cursor = db.cursor()
		cursor.execute("""
				SELECT * FROM usuario
				WHERE user=?;
				""", (user,))
		key_usuario = cursor.fetchall()
		db.close()
		#criptografa o bd/
		cript_db = open(diretorio_bd, "rb")
		db_cripto = cifra_principal.encrypt(cript_db.read())
		cript_db.close()
		cript_db = open(diretorio_bd, "wb")
		cript_db.write(db_cripto)
		cript_db.close()
		#/
		
		if len(key_usuario) > 0:
			
			#verifica se a senha passada é a mesma do usuario/
			if senha == cifra_principal.decrypt(bytes(key_usuario[0][2], "utf-8")):

				print(f"sua key: {key_usuario[0][3]}")
				continuar()
				key_usuario = None
			#/

		else:

			print("nenhum usuario encontrado!")
			continuar()

	elif escolha == 3:
		
		#retorna os usuarios disponiveis
		usuarios = ver_usuarios(cifra_principal, diretorio_bd)

		if len(usuarios) > 0:

				for index, arq in enumerate(pasta):

					print(f"{index}|{arq}")

				print("\n")
				#escolha do arquivo
				escolha_arquivo = int(input("escolha o index do arquivo: "))
				#chave do usuario
				chave = str(input("cole sua chave aqui: ")).strip()

				if escolha_arquivo <= len(pasta)-1 and escolha_arquivo >= 0:
					#função para criptografa
					criptografa(str(pasta[escolha_arquivo]), chave, diretorio_bd, cifra_principal)
					print("criptografado com sucesso!!")
					continuar()

				else:

					print("sem arquivos com mesmo indice na pasta! mova os arquivos o mesmo diretorio do executavel")
					continuar()

		else:

			print("nenhum usuario criado!")
			continuar()
	
	elif escolha == 4:

		#retorna os usuarios disponiveis
		usuarios = ver_usuarios(cifra_principal, diretorio_bd)
		
		if len(usuarios) > 0:

				for index, arq in enumerate(pasta):

					print(f"{index}|{arq}")
				
				print("\n")
				#escolha do arquivo a descriptografa
				escolha_arquivo = int(input("digite o index do arquivo: "))
				#key do usuario
				key = str(input("cole sua key: ")).strip()
				
				if escolha_arquivo <= len(pasta)-1 and escolha_arquivo >= 0:
					#função para descriptografa
					descriptografa(pasta[escolha_arquivo], key, diretorio_bd, cifra_principal)
					print("arquivo descriptografado!!")
					continuar()

				else:

					print("sem arquivos de mesmo indice na pasta! mova o executavel ou os arquivos para a pasta")
					continuar()
		
		else:

			print("nenhum usuario criado!")
			continuar()

	elif escolha == 5:
		
		#retorna os usuarios disponiveis
		usuarios = ver_usuarios(cifra_principal, diretorio_bd)

		if len(usuarios) > 0:
			
			#nome de usuario
			user = str(input("digite seu nome de usuario: "))
			
			#procura se ha algum usuario com esse nome
			for usu in usuarios:

				if user == usu[1]:

					auth = True
					break

				else:

					usu = None
			#se sim, ele passa pra parte de atenticação da senha
			if auth:
				
				while True:

					auth = False
					#pega a senha do usuario
					senha = getpass.getpass("senha: ")
					#verifica a senha no bd
					senha_usu = bytes(usu[2], "utf-8")
					senha_usu = cifra_principal.decrypt(senha_usu).decode("utf-8")

					if senha == senha_usu:

						auth = True
						break

					else:

						print("senha incorreta!!")
						sair_ou_nao = int(input("digite 1 para sair e 0 para tentar novamente: "))

						if sair_ou_nao == 1:

							break

			if auth:
				
				#função para apagar usuarios
				apagar_usuario((usu[0], ), diretorio_bd, cifra_principal)
				print("usuario apagado!")

		else:

			print("sem usuarios registrados!!")
			continuar()
	
	elif escolha == 6:

		ajuda()

	elif escolha == 0:

		break

	if sistema == "Windows":

		os.system("cls")

	elif sistema == "Linux":

		os.system("clear")

