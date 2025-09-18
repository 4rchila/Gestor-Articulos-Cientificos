import os

DB_archivo = os.path.join('data', 'articulos_db.txt')

def guardar_en_db(articulo):
    os.makedirs('data', exist_ok=True)
    existentes = set()
    if os.path.exists(DB_archivo):
        with open(DB_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                hash_existente = linea.strip().split('|')[0]
                existentes.add(int(hash_existente))
    if articulo.hash in existentes:
        return
    with open(DB_archivo, 'a', encoding='utf-8') as f:
        f.write(f"{articulo.hash}|{articulo.titulo}|{articulo.autores}|{articulo.año}|{articulo.contenido}|{os.path.basename(articulo.nombreArchivo)}\n")

def leer_db():
    if not os.path.exists(DB_archivo):
        return []
    articulos = []
    with open(DB_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            partes = linea.strip().split('|')
            if len(partes) != 6:
                continue
            hash_val, titulo, autores, año, contenido, archivo = partes
            articulos.append({
                'hash': int(hash_val),
                'titulo': titulo,
                'autores': autores,
                'año': año,
                'contenido': contenido,
                'archivo': os.path.join("data", archivo)
            })
    return articulos

def sobrescribir_db(lista_articulos):
    with open(DB_archivo, 'w', encoding='utf-8') as f:
        for a in lista_articulos:
            f.write(f"{a['hash']}|{a['titulo']}|{a['autores']}|{a['año']}|{a['contenido']}|{os.path.basename(a['archivo'])}\n")

def eliminar_de_db(hash_key):
    articulos = leer_db()
    nuevos = []
    for a in articulos:
        if a['hash'] == hash_key:
            if os.path.exists(a['archivo']):
                os.remove(a['archivo'])
        else:
            nuevos.append(a)
    sobrescribir_db(nuevos)
