class Musica:
    def __init__(self, titulo:str, artista:str):
        self.titulo = titulo
        self.artista = artista 
        self.views = 0

    def play(self):
        print(f" A música{self.titulo} está tocando!")
        self.views += 1
        print(self.views)

musica1 = Musica("Warpigs", "black sabbath")
musica2 = Musica("sozinho", "caetano Veloso")
musica1.play()
musica1.play()
musica1.play()


    