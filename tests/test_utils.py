import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from hashing import Articulo, TablaHash

hash_table = TablaHash()

book1 = Articulo("Cien años de soledad", "Gabriel García Márquez", 1967, "articulos_db.txt")
book2 = Articulo("1984", "George Orwell", 1949, "articulos_db.txt")

hash_table.insert(book1)
hash_table.insert(book2)

hash_table.display()    