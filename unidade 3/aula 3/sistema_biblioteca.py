class Livro:
    def __init__(self, titulo:str, genero:list, autor:str, isbn:str, editora:str, estaDisponivel:bool):
        self.titulo = titulo
        self.genero = genero
        self.autor = autor
        self.isbn = isbn
        self.editora = editora
        self.estaDisponivel = estaDisponivel
        

    def alteraStatus(self):
        self.estaDisponivel = not self.estaDisponivel

class Usuario:
    def __init__(self, nome:str, senha:str, email:str):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.lista_livros = []
    
    def devolver_livro(self, livro):
        self.lista_livros.remove(livro)

    def receber_livro(self, livro):
        self.lista_livros.append(livro)

class Biblioteca:
    def __init__(self, nome):  
        self.nome = nome
        self.lista_livros = []
        self.lista_usuarios = []

    def cadastrar_livro(self, livro:Livro):
        self.lista_livros.append(livro)
        
    def cadastra_usuario(self, usuario:Usuario):
        self.lista_usuarios.append(usuario)

    def empresta_livros(self, livro:Livro, usuario:Usuario):
        if livro.estaDisponivel:
            livro.alteraStatus()
            usuario.receber_livro(livro)

    def devolve_livro(self, livro:Livro, usuario:Usuario):
        if not livro.estaDisponivel:
            livro.alteraStatus()
            usuario.devolver_livro(livro)

biblioteca = Biblioteca("Biblioteca senac")
livro1 = Livro("crônicas de nárnia" , ["ficção", "aventura"], "lewis", "123", "globo", True)
Usuario1 = Usuario("carlos","123456", "orekirt@gmail.com")
biblioteca.cadastrar_livro(livro1)
biblioteca.cadastra_usuario(Usuario1)
biblioteca.empresta_livros(livro1, Usuario1)
print(livro1.estaDisponivel)
print(Usuario1.lista_livros[0].titulo)

biblioteca.devolve_livro(livro1, Usuario1)
print(livro1.estaDisponivel)