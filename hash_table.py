from models import Articulo

class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash(self, key):
        return hash(key) % self.size

    def insertar(self, book: Articulo):
        index = self.hash(book.hash)
        self.table[index].append((book.hash, book))
        book.guardarEnArchivo()  

    def buscar(self, hash_key):
        index = self.hash(hash_key)
        for k, v in self.table[index]:
            if k == hash_key:
                return v
        return None

    def eliminar(self, hash_key):
        index = self.hash(hash_key)
        self.table[index] = [(k, v) for (k, v) in self.table[index] if k != hash_key]

    def escribirEnPantalla(self):
        for i, bucket in enumerate(self.table):
            print(f"\nBucket {i}:")
            for k, book in bucket:
                print(f"  Hash: {book.hash}, Título: {book.titulo}, Autores: {book.autores}, Año: {book.año}")
