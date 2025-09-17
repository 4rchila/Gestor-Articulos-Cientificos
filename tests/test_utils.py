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

        if os.path.exists(self.nombreArchivo):
            with open(self.nombreArchivo, "rb") as f:
                data = f.read()
        else:
            data = self.titulo.encode('utf-8')

        for byte in data:
            hash_value ^= byte
            hash_value *= FNV_prime
            hash_value &= 0xFFFFFFFF 

        return hash_value


from test_hash_table import HashTable

if __name__ == "__main__":
    hash_table = HashTable()
    hash_table.cargarDesdeDB()

    book1 = Articulo("Cien años de soledad", "Gabriel García Márquez", 1967, "cien.txt")
    book2 = Articulo("1984", "George Orwell", 1949, "1984.txt")

    hash_table.insertar(book1)
    hash_table.insertar(book2)

    hash_table.escribirEnPantalla()

    print("\nBuscando por hash de 'Cien años de soledad':")
    resultado = hash_table.buscar(book1.hash)
    print(resultado if resultado else "No encontrado")

    hash_table.eliminar(book2.hash)