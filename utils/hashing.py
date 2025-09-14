class Articulo:
    def __init__(self, titulo, autores, año, nombreArchivo):
        self.titulo = titulo
        self.autores = autores
        self.año = año
        self.nombreArchivo = nombreArchivo
        self.hash = self.calcularHash()

    def calcularHash(self):
        FNV_offset_basis = 2166136261
        FNV_prime = 16777619
        hash_value = FNV_offset_basis

        for byte in self.titulo.encode('utf-8'):
            hash_value ^= byte
            hash_value *= FNV_prime
            hash_value &= 0xffffffff

        return hash_value


class HashTable:
    def __init__(self, size=256):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, book):
        index = self._hash(book.hash)
        self.table[index].append(book)

    def find(self, titulo):
        for bucket in self.table:
            for book in bucket:
                if book.titulo == titulo:
                    return book
        return None

    def display(self):
        for bucket in self.table:
            for book in bucket:
                print(f"Hash: {book.hash}, titulo: {book.titulo}, Authors: {book.autores}, Year: {book.año}, Filename: {book.nombreArchivo}")