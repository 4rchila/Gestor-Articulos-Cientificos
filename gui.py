# gui_integrated.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from models import Articulo
from hash_table import HashTable

class IntegratedScientificArticlesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Artículos Científicos")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')

        # Variables GUI
        self.selected_file_path = tk.StringVar()
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.sort_type = tk.StringVar(value="titulo")
        self.search_type = tk.StringVar(value="titulo")

        # Inicializar tabla hash
        self.tabla_hash = HashTable()

        # Configurar interfaz
        self.setup_ui()
        self.refresh_article_list()

    ##########################
    # CONFIGURACIÓN DE LA GUI
    ##########################
    def setup_ui(self):
        # Título
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="Sistema de Gestión de Artículos Científicos",
                 font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50').pack(expand=True)

        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Pestañas
        self.create_add_article_tab()
        self.create_search_tab()
        self.create_list_tab()

        # Barra de estado
        self.status_bar = tk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor='w', bg='#ecf0f1')
        self.status_bar.pack(side='bottom', fill='x')

    ##########################
    # PESTAÑA: AGREGAR ARTÍCULO
    ##########################
    def create_add_article_tab(self):
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="Agregar Artículo")
        main_frame = tk.Frame(add_frame, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Metadatos
        metadata_frame = tk.LabelFrame(main_frame, text="Metadatos del Artículo", font=('Arial', 12, 'bold'), bg='white')
        metadata_frame.pack(fill='x', pady=(0, 20))
        tk.Label(metadata_frame, text="Título:", font=('Arial', 10), bg='white').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(metadata_frame, textvariable=self.title_var, font=('Arial', 10), width=50).grid(row=0, column=1, sticky='w', padx=10, pady=5)

        tk.Label(metadata_frame, text="Autor(es):", font=('Arial', 10), bg='white').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(metadata_frame, textvariable=self.author_var, font=('Arial', 10), width=50).grid(row=1, column=1, sticky='w', padx=10, pady=5)

        tk.Label(metadata_frame, text="Año:", font=('Arial', 10), bg='white').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        tk.Entry(metadata_frame, textvariable=self.year_var, font=('Arial', 10), width=20).grid(row=2, column=1, sticky='w', padx=10, pady=5)

        metadata_frame.columnconfigure(1, weight=1)

        # Archivo
        file_frame = tk.LabelFrame(main_frame, text="Archivo del Artículo", font=('Arial', 12, 'bold'), bg='white')
        file_frame.pack(fill='x', pady=(0, 20))
        file_info_frame = tk.Frame(file_frame, bg='white')
        file_info_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(file_info_frame, text="Archivo seleccionado:", font=('Arial', 10), bg='white').pack(anchor='w')
        file_display_frame = tk.Frame(file_info_frame, bg='white')
        file_display_frame.pack(fill='x', pady=(5, 10))
        tk.Label(file_display_frame, textvariable=self.selected_file_path, font=('Arial', 9), bg='#ecf0f1',
                 relief='sunken', anchor='w').pack(side='left', fill='x', expand=True, padx=(0, 10))
        tk.Button(file_display_frame, text="Seleccionar Archivo", command=self.select_file,
                  bg='#3498db', fg='white', font=('Arial', 10), cursor='hand2').pack(side='right')

        # Botones
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill='x', pady=20)
        tk.Button(button_frame, text="Agregar Artículo", command=self.add_article,
                  bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), cursor='hand2', height=2).pack(side='left', padx=(0, 10))
        tk.Button(button_frame, text="Limpiar Campos", command=self.clear_fields,
                  bg='#95a5a6', fg='white', font=('Arial', 12), cursor='hand2', height=2).pack(side='left')

    ##########################
    # PESTAÑA: BUSCAR ARTÍCULO
    ##########################
    def create_search_tab(self):
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Buscar y Gestionar")
        main_frame = tk.Frame(search_frame, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        search_section = tk.LabelFrame(main_frame, text="Búsqueda de Artículos", font=('Arial', 12, 'bold'), bg='white')
        search_section.pack(fill='x', pady=(0, 20))
        search_controls = tk.Frame(search_section, bg='white')
        search_controls.pack(fill='x', padx=10, pady=10)
        tk.Label(search_controls, text="Buscar:", font=('Arial', 10), bg='white').pack(side='left')
        tk.Entry(search_controls, textvariable=self.search_var, font=('Arial', 10), width=30).pack(side='left', padx=(10, 5))
        ttk.Combobox(search_controls, textvariable=self.search_type,
                     values=["titulo", "autor", "año", "hash"], state="readonly", width=10).pack(side='left', padx=5)
        tk.Button(search_controls, text="Buscar", command=self.search_articles,
                  bg='#3498db', fg='white', font=('Arial', 10), cursor='hand2').pack(side='left', padx=5)

        # Resultados
        results_frame = tk.LabelFrame(main_frame, text="Resultados", font=('Arial', 12, 'bold'), bg='white')
        results_frame.pack(fill='both', expand=True)
        tree_frame = tk.Frame(results_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        columns = ('Hash', 'Título', 'Autor', 'Año')
        self.search_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        for col in columns:
            self.search_tree.heading(col, text=col)
        self.search_tree.column('Hash', width=100)
        self.search_tree.column('Título', width=300)
        self.search_tree.column('Autor', width=200)
        self.search_tree.column('Año', width=80)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.search_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.search_tree.xview)
        self.search_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.search_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')

    ##########################
    # PESTAÑA: LISTAR ARTÍCULOS
    ##########################
    def create_list_tab(self):
        list_frame = ttk.Frame(self.notebook)
        self.notebook.add(list_frame, text="Listar Artículos")
        main_frame = tk.Frame(list_frame, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        controls_frame = tk.Frame(main_frame, bg='white')
        controls_frame.pack(fill='x', pady=(0, 20))
        tk.Label(controls_frame, text="Ordenar por:", font=('Arial', 12, 'bold'), bg='white').pack(side='left')
        ttk.Combobox(controls_frame, textvariable=self.sort_type, values=["titulo", "autor", "año"], state="readonly", width=15).pack(side='left', padx=10)
        tk.Button(controls_frame, text="Actualizar Lista", command=self.refresh_article_list,
                  bg='#3498db', fg='white', font=('Arial', 10), cursor='hand2').pack(side='left', padx=10)

        # Lista
        list_section = tk.LabelFrame(main_frame, text="Todos los Artículos", font=('Arial', 12, 'bold'), bg='white')
        list_section.pack(fill='both', expand=True)
        tree_frame = tk.Frame(list_section, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        columns = ('Hash', 'Título', 'Autor', 'Año')
        self.list_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.list_tree.heading(col, text=col)
        self.list_tree.column('Hash', width=100)
        self.list_tree.column('Título', width=300)
        self.list_tree.column('Autor', width=200)
        self.list_tree.column('Año', width=80)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.list_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.list_tree.xview)
        self.list_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.list_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')

    ##########################
    # MÉTODOS DE ACCIÓN
    ##########################
    def select_file(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo PDF", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.selected_file_path.set(file_path)

    def add_article(self):
        # Crear objeto Articulo
        article = Articulo(
            titulo=self.title_var.get(),
            autores=self.author_var.get(),
            año=self.year_var.get(),
            archivo=self.selected_file_path.get()
        )
        # Insertar en tabla hash (integrado)
        self.tabla_hash.insertar(article)
        messagebox.showinfo("Éxito", "Artículo agregado correctamente")
        self.clear_fields()
        self.refresh_article_list()

    def clear_fields(self):
        self.title_var.set("")
        self.author_var.set("")
        self.year_var.set("")
        self.selected_file_path.set("")

    def search_articles(self):
        self.search_tree.delete(*self.search_tree.get_children())
        query = self.search_var.get().lower()
        search_type = self.search_type.get()
        # Buscar en tabla hash
        results = []
        if search_type == "hash":
            found = self.tabla_hash.buscar(query)
            if found:
                results.append(found)
        else:
            # Buscar en todos los buckets
            for bucket in self.tabla_hash.table:
                for _, art in bucket:
                    if query in getattr(art, search_type).lower():
                        results.append(art)
        # Mostrar resultados
        for art in results:
            self.search_tree.insert('', 'end', values=(art.hash, art.titulo, art.autores, art.año))
        self.status_bar.config(text=f"{len(results)} artículos encontrados")

    def refresh_article_list(self):
        self.list_tree.delete(*self.list_tree.get_children())
        all_articles = []
        for bucket in self.tabla_hash.table:
            for _, art in bucket:
                all_articles.append(art)
        sort_attr = self.sort_type.get()
        all_articles.sort(key=lambda x: getattr(x, sort_attr).lower())
        for art in all_articles:
            self.list_tree.insert('', 'end', values=(art.hash, art.titulo, art.autores, art.año))
        self.status_bar.config(text=f"{len(all_articles)} artículos en el sistema")
