import os

class Articulo:
    def __init__(self, titulo, autores, año, nombreArchivo):
        self.titulo = titulo
        self.autores = autores  
        self.año = año
        self.nombreArchivo = os.path.join('data', nombreArchivo)  
        self.hash = self.calcularHash()

    def guardar_en_archivo(self):
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

    def _hash(self, key):
        return key % self.size

    def insert(self, book):
        index = self._hash(book.hash)
        self.table[index].append(book)
        book.guardar_en_archivo()

    def find(self, titulo):
        temp_article = Articulo(titulo, "", 0, "temp.txt")  
        index = self._hash(temp_article.hash)
        
        for book in self.table[index]:
            if book.titulo == titulo:
                return book
        return None

    def display(self):
        for i, bucket in enumerate(self.table):
                print(f"\nBucket {i}:")
                for book in bucket:
                    print(f"  Hash: {book.hash}, Título: {book.titulo}, Autores: {book.autores}, Año: {book.año}")

if __name__ == "__main__":
    hash_table = TablaHash()

    book1 = Articulo("Cien años de soledad", "Gabriel García Márquez", 1967, "articulos_db.txt")
    book2 = Articulo("1984", "George Orwell", 1949, "articulos_db.txt")
    book3 = Articulo("El Quijote", "Miguel de Cervantes", 1605, "articulos_db.txt")

    hash_table.insert(book1)
    hash_table.insert(book2)
    hash_table.insert(book3)

    print("Contenido de la tabla hash:")
    hash_table.display()

    print("\nBuscando '1984':")
    encontrado = hash_table.find("1984")
    if encontrado:
        print(f"Encontrado: {encontrado}")
    else:
        print("No encontrado")

    print("\nContenido del archivo articulos_db.txt:")
    try:
        with open(os.path.join('data', 'articulos_db.txt'), 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print("El archivo aún no existe o está vacío")