from models import Articulo
from hash_table import HashTable
import os

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "articulos_db.txt")

def limpiar_todo():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            f.write("")
        print("Se limpió el contenido de articulos_db.txt")

    if os.path.exists(DATA_DIR):
        for archivo in os.listdir(DATA_DIR):
            ruta = os.path.join(DATA_DIR, archivo)
            if os.path.isfile(ruta) and archivo.endswith(".txt") and archivo != "articulos_db.txt":
                os.remove(ruta)
                print(f"Se eliminó {archivo}")

def menu():
    print("\n=== MENÚ ===")
    print("1. Insertar artículo")
    print("2. Buscar artículo por hash")
    print("3. Eliminar artículo por hash")
    print("4. Listar artículos en tabla hash")
    print("5. Salir y limpiar todo")
    return input("Elige una opción: ")

def main():
    tabla = HashTable(size=10)

    while True:
        opcion = menu()

        if opcion == "1":
            titulo = input("Título: ")
            autores = input("Autores: ")
            año = input("Año: ")
            nombre_archivo = input("Nombre del archivo (ej. libro.txt): ")
            contenido = input("Escribe una breve descripción o contenido: ")

            articulo = Articulo(titulo, autores, año, nombre_archivo, contenido)
            tabla.insertar(articulo)
            print(f"Artículo '{titulo}' insertado con hash {articulo.hash}")

        elif opcion == "2":
            try:
                hash_key = int(input("Ingresa el hash del artículo a buscar: "))
                encontrado = tabla.buscar(hash_key)
                if encontrado:
                    print("Artículo encontrado:", encontrado)
                else:
                    print("No se encontró el artículo")
            except ValueError:
                print("Ingresa un número válido.")

        elif opcion == "3":
            try:
                hash_key = int(input("Ingresa el hash del artículo a eliminar: "))
                tabla.eliminar(hash_key)
                print(f"Artículo con hash {hash_key} eliminado")
            except ValueError:
                print("Ingresa un número válido.")

        elif opcion == "4":
            tabla.escribirEnPantalla()

        elif opcion == "5":
            print("\n=== Saliendo del programa ===")
            limpiar_todo()
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
