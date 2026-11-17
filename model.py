# model.py
import math
from pypdf import PdfReader, PdfWriter, PageObject

class LivretoModel:
    @staticmethod
    def criar_cadernos_livro(input_pdf_path, output_pdf_path, folhas_por_caderno):
        """
        Organiza um PDF em cadernos (signatures) para impressão em formato de livro (booklet).
        """
        reader = PdfReader(input_pdf_path)
        total_pag_originais = len(reader.pages)
        
        # Cada folha impressora frente e verso comporta 4 páginas de livro
        paginas_por_caderno = folhas_por_caderno * 4

        # Calcular quantas páginas totais precisamos para fechar múltiplos de cadernos
        num_cadernos = math.ceil(total_pag_originais / paginas_por_caderno)
        total_pag_alvo = num_cadernos * paginas_por_caderno
        paginas_em_branco = total_pag_alvo - total_pag_originais

        # Criar lista completa de páginas incluindo as brancas
        todas_as_paginas = list(reader.pages)
        
        # Obter dimensões da primeira página para criar páginas em branco idênticas
        primeira_pagina = reader.pages[0]
        largura = primeira_pagina.mediabox.width
        altura = primeira_pagina.mediabox.height

        # Adicionar as páginas em branco necessárias
        for _ in range(paginas_em_branco):
            pagina_vazia = PageObject.create_blank_page(width=largura, height=altura)
            todas_as_paginas.append(pagina_vazia)

        writer = PdfWriter()

        # Processar caderno por caderno na ordem correta de montagem (imposição)
        for c in range(num_cadernos):
            inicio = c * paginas_por_caderno
            fim = inicio + paginas_por_caderno
            bloco_paginas = todas_as_paginas[inicio:fim]
            
            num_folhas_caderno = len(bloco_paginas) // 4
            
            ordem_indices = []
            for i in range(num_folhas_caderno):
                frente_esquerda = (num_folhas_caderno * 2) - 1 - i
                frente_direita = i
                verso_esquerda = i + num_folhas_caderno
                verso_direita = (num_folhas_caderno * 3) - 1 - i
                
                ordem_indices.extend([frente_esquerda, frente_direita, verso_esquerda, verso_direita])

            caderno_imposto = [bloco_paginas[idx] for idx in ordem_indices]
            
            for p in caderno_imposto:
                writer.add_page(p)

        # Salvar o arquivo final pronto
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)
            
        return num_cadernos, paginas_em_branco