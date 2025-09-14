import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Articulo
from hash_table import HashTable

hash_table = HashTable()

book1 = Articulo("Cien años de soledad", "Gabriel García Márquez", 1967, "cien.txt")
book2 = Articulo("1984", "George Orwell", 1949, "1984.txt")

hash_table.insertar(book1)
hash_table.insertar(book2)

hash_table.escribirEnPantalla()

print("\nBuscando por hash de 'Cien años de soledad':")
resultado = hash_table.buscar(book1.hash)
print(resultado if resultado else "No encontrado")
