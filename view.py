# view.py
import tkinter as tk
from tkinter import ttk, filedialog

class LivretoView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.title("Gerador de Cadernos para Livros (Booklet)")
        self.geometry("600x650")
        self.resizable(False, False)
        
        self._criar_widgets()

    def _criar_widgets(self):
        # --- SEÇÃO 1: SELEÇÃO DE ARQUIVO ---
        frame_arquivo = ttk.LabelFrame(self, text=" 1. Selecione o Arquivo PDF ", padding=10)
        frame_arquivo.pack(fill="x", padx=15, pady=10)

        self.entry_caminho = ttk.Entry(frame_arquivo, width=50, state="readonly")
        self.entry_caminho.pack(side="left", padx=(0, 10))

        btn_procurar = ttk.Button(frame_arquivo, text="Procurar...", command=self.controller.selecionar_arquivo)
        btn_procurar.pack(side="left")

        # --- SEÇÃO 2: QUANTIDADE DE FOLHAS POR CADERNOS (RADIO BUTTONS) ---
        frame_folhas = ttk.LabelFrame(self, text=" 2. Folhas por Caderno (Signature) ", padding=10)
        frame_folhas.pack(fill="x", padx=15, pady=10)

        self.var_folhas = tk.IntVar(value=4) # Padrão recomendado
        
        opcoes = [
            ("2 folhas (8 páginas por caderno)", 2),
            ("4 folhas (16 páginas por caderno) - Recomendado", 4),
            ("8 folhas (32 páginas por caderno)", 8)
        ]

        for texto, valor in opcoes:
            rb = ttk.Radiobutton(frame_folhas, text=texto, value=valor, variable=self.var_folhas)
            rb.pack(anchor="w", pady=2)

        # --- SEÇÃO 3: BOTÃO DE EXECUÇÃO ---
        self.btn_gerar = ttk.Button(self, text="Gerar PDF Pronto para Impressão", command=self.controller.processar_pdf, state="disabled")
        self.btn_gerar.pack(pady=10)

        # --- SEÇÃO 4: COMO USAR E IMPRIMIR ---
        frame_instrucoes = ttk.LabelFrame(self, text=" Como Usar e Imprimir o Resultado ", padding=10)
        frame_instrucoes.pack(fill="both", expand=True, padx=15, pady=10)

        texto_instrucoes = (
            "• O script adiciona automaticamente páginas em branco se necessário para fechar os blocos.\n"
            "• O arquivo gerado será salvo na mesma pasta com o nome '_impresso.pdf'.\n\n"
            "Configurações na Impressora:\n"
            "1. Configure a impressão para **Frente e Verso (Duplex)**.\n"
            "2. Escolha **Virar na borda curta** (se paisagem) ou **borda longa** (se retrato).\n"
            "3. Dobre as folhas ao meio e encaixe-as como cadernos de livro tradicionais."
        )
        
        lbl_instrucoes = ttk.Label(frame_instrucoes, text=texto_instrucoes, justify="left", wraplength=540)
        lbl_instrucoes.pack(anchor="w")

    def atualizar_caminho(self, caminho):
        self.entry_caminho.config(state="normal")
        self.entry_caminho.delete(0, tk.END)
        self.entry_caminho.insert(0, caminho)
        self.entry_caminho.config(state="readonly")
        self.btn_gerar.config(state="normal")