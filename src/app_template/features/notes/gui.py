from __future__ import annotations

from typing import TYPE_CHECKING

from app_template.features.notes.use_cases import add_note, list_notes, remove_note

if TYPE_CHECKING:
    import tkinter as tk
    from tkinter import ttk


def create_notes_panel(parent: tk.Misc) -> ttk.Frame:
    import tkinter as tk
    from tkinter import messagebox, ttk

    panel = ttk.Frame(parent, padding=16)

    # Frame para adicionar nota
    add_frame = ttk.Frame(panel)
    add_frame.pack(fill="x", pady=(0, 16))

    ttk.Label(add_frame, text="Nova nota:").pack(side="left", padx=(0, 8))
    title_var = tk.StringVar(master=add_frame)
    entry = ttk.Entry(add_frame, textvariable=title_var)
    entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

    # Treeview para listar notas
    list_frame = ttk.Frame(panel)
    list_frame.pack(fill="both", expand=True)

    columns = ("id", "title", "date")
    tree = ttk.Treeview(list_frame, columns=columns, show="headings")
    tree.heading("id", text="ID")
    tree.heading("title", text="Título")
    tree.heading("date", text="Data")

    tree.column("id", width=250)
    tree.column("title", width=300)
    tree.column("date", width=150)

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_list() -> None:
        for item in tree.get_children():
            tree.delete(item)
        notes = list_notes()
        if not notes:
            # Não é possível adicionar placeholder no meio do treeview de forma simples no ttk,
            # apenas deixamos vazio
            pass
        else:
            for n in notes:
                tree.insert("", "end", values=(n.id, n.title, n.created_at))

    def on_add() -> None:
        title = title_var.get()
        try:
            add_note(title)
            title_var.set("")
            refresh_list()
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))

    def on_remove() -> None:
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma nota para remover.")
            return

        for item in selected:
            note_id = tree.item(item, "values")[0]
            remove_note(note_id)

        refresh_list()

    ttk.Button(add_frame, text="Adicionar", command=on_add).pack(side="left")

    btn_frame = ttk.Frame(panel)
    btn_frame.pack(fill="x", pady=(16, 0))
    ttk.Button(btn_frame, text="Remover Selecionada", command=on_remove).pack(side="right")

    refresh_list()

    return panel
