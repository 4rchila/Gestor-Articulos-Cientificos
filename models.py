import os

class Articulo:
    def __init__(self, titulo, autores, año, nombreArchivo="", contenido=""):
        self.titulo = titulo
        self.autores = autores
        self.año = año
        self.contenido = contenido if contenido else "Sin contenido.\n"

        # Calcular hash con FNV-1a
        self.hash = self.calcularHash()

        # Si no se dio nombreArchivo, lo generamos con el hash
        self.nombreArchivo = nombreArchivo if nombreArchivo else f"{self.hash}.txt"

    def guardarEnArchivo(self):
        """Guarda el artículo como <hash>.txt dentro de data/articulos"""
        ruta = os.path.join("data", "articulos", self.nombreArchivo)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("=== Metadatos ===\n")
            f.write(f"Título: {self.titulo}\n")
            f.write(f"Autor(es): {self.autores}\n")
            f.write(f"Año: {self.año}\n\n")
            f.write("=== Contenido ===\n")
            f.write(self.contenido)

    def __str__(self):
        return f"'{self.titulo}' por {self.autores} ({self.año})"

    def calcularHash(self):
        """Calcula hash FNV-1a basado en los metadatos + contenido"""
        FNV_offset_basis = 0x811C9DC5
        FNV_prime = 0x01000193
        hash_value = FNV_offset_basis

        # Cadena con título, autores, año y contenido
        data = (self.titulo + self.autores + self.año + self.contenido).encode("utf-8")

        for byte in data:
            hash_value ^= byte
            hash_value *= FNV_prime
            hash_value &= 0xFFFFFFFF  # Limitar a 32 bits (unsigned int)

        return hash_value
