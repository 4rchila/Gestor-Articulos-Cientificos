# database.py - Versión mínima para pruebas

class Database:
    def __init__(self, filename):
        self.filename = filename
        print(f"[Database] Inicializando con archivo: {filename}")

    def save_article(self, article):
        print(f"[Database] Guardando artículo: {article}")

    def load_all_articles(self):
        print("[Database] Cargando artículos...")
        return []  # Devolver lista vacía para pruebas

    def delete_article(self, article_hash):
        print(f"[Database] Eliminando artículo con hash: {article_hash}")
