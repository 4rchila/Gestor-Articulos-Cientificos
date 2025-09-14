import os

class Articulo:
    def __init__(self, titulo, autores, año, nombreArchivo):
        self.titulo = titulo
        self.autores = autores  
        self.año = año
        self.nombreArchivo = os.path.join('data', nombreArchivo)  
        self.hash = self.calcularHash()

    def guardarEnArchivo(self):
        os.makedirs(os.path.dirname(self.nombreArchivo), exist_ok=True)
        
        with open(self.nombreArchivo, 'a', encoding='utf-8') as f:
            f.write(f"{self.titulo}|{self.autores}|{self.año}\n")  
    
    def __str__(self):
        return f"'{self.titulo}' por {self.autores} ({self.año})"  

    def calcularHash(self):
        FNV_offset_basis = 0x811C9DC5  
        FNV_prime = 0x01000193         
        hash_value = FNV_offset_basis

        for byte in self.titulo.encode('utf-8'):
            hash_value ^= byte           
            hash_value *= FNV_prime      
            hash_value &= 0xFFFFFFFF     

        return hash_value

class TablaHash:
    def __init__(self, size=256):
        self.size = size
        self.table = [[] for _ in range(size)]

    def Hash(self, key):
        return key % self.size

    def insertar(self, book):
        index = self.Hash(book.hash)
        self.table[index].append(book)
        book.guardarEnArchivo()

    def encontrar(self, titulo):
        temp_article = Articulo(titulo, "", 0, "temp.txt")  
        index = self.Hash(temp_article.hash)
        
        for book in self.table[index]:
            if book.titulo == titulo:
                return book
        return None

    def escribirEnPantalla(self):
        for i, bucket in enumerate(self.table):
                print(f"\nBucket {i}:")
                for book in bucket:
                    print(f"  Hash: {book.hash}, Título: {book.titulo}, Autores: {book.autores}, Año: {book.año}")
