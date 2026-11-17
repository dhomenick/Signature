# controller.py
from tkinter import filedialog, messagebox
from model import LivretoModel
from view import LivretoView

class LivretoController:
    def __init__(self):
        self.arquivo_selecionado = None
        self.view = LivretoView(self)

    def iniciar(self):
        self.view.mainloop()

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if caminho:
            self.arquivo_selecionado = caminho
            self.view.atualizar_caminho(caminho)

    def processar_pdf(self):
        if not self.arquivo_selecionado:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF primeiro.")
            return

        folhas = self.view.var_folhas.get()
        
        # Definir caminho do arquivo de saída (ex: nomeoriginal_impresso.pdf)
        output_path = self.arquivo_selecionado.rsplit(".", 1)[0] + "_impresso.pdf"

        try:
            num_cadernos, paginas_brancas = LivretoModel.criar_cadernos_livro(
                self.arquivo_selecionado, 
                output_path, 
                folhas_por_caderno=folhas
            )
            
            msg = (
                f"PDF gerado com sucesso!\n\n"
                f"• Salvo em: {output_path}\n"
                f"• Total de cadernos criados: {num_cadernos}\n"
                f"• Páginas em branco adicionadas: {paginas_brancas}"
            )
            messagebox.showinfo("Sucesso", msg)
            
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro ao processar o PDF:\n{str(e)}")

if __name__ == "__main__":
    app = LivretoController()
    app.iniciar()