from tests.test_utils import Articulo
from tests.test_hash_table import HashTable
from tests.test_database import guardar_en_db, leer_db


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